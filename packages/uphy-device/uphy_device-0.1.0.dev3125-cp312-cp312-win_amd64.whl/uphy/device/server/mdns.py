from contextlib import contextmanager
from threading import Thread
import upgen.model.uphy as config
import upgen.model.runtime as runtime
from uphy.device import DeviceError, Protocol
import logging
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
from zeroconf import ServiceInfo, Zeroconf
import socket
import psutil

LOGGER = logging.getLogger(__name__)


def _model_to_runtime(model: config.Root, device: config.Device) -> runtime.Root:
    def _get_signal(signal: config.Signal):
        return runtime.Signal(
            name=signal.name,
            datatype=signal.datatype,
            is_array=signal.is_array,
            array_length=signal.array_length,
        )

    def _get_parameter(param: config.Parameter):
        return runtime.Parameter(
            name=param.name,
            datatype=param.datatype,
            default=param.default,
            min=param.min,
            max=param.max,
            permissions=param.permissions,
            profinet=param.profinet,
        )

    def _get_slot(root: config.Root, slot: config.Slot):
        module = root.get_module(slot.module)
        return runtime.Slot(
            name=slot.name,
            inputs=[_get_signal(signal) for signal in module.inputs],
            outputs=[_get_signal(signal) for signal in module.outputs],
            parameters=[_get_parameter(param) for param in module.parameters],
        )

    def _get_device(device: config.Device):
        return runtime.Device(
            name=device.name, slots=[_get_slot(model, slot) for slot in device.slots]
        )

    return runtime.Root(device=_get_device(device))


@contextmanager
def _model_server(model: config.Root, device: config.Device, address: str):
    print(address)

    path = "/model.json"
    runtime_model = _model_to_runtime(model, device)

    class ModelHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == path:
                self.send_response(200)
                self.send_header("Content-type", "text/json")
                self.end_headers()
                self.wfile.write(runtime_model.json().encode())
            else:
                self.send_error(404, "File Not Found: %s" % self.path)

    class BasicServer(TCPServer):
        def server_bind(self):
            TCPServer.server_bind(self)
            host, port = self.server_address[:2]
            self.server_host = host
            self.server_port = port

    LOGGER.debug("Starting model server")
    server = BasicServer((address, 0), ModelHandler, bind_and_activate=True)

    def _run():
        LOGGER.info("Serving model on port %s and path %s", server.server_port, path)
        server.serve_forever()

    runner = Thread(
        target=_run,
        name="Model server",
        daemon=True,
    )
    runner.start()

    try:
        yield server.server_port, path
    finally:
        server.shutdown()


@contextmanager
def run(model: config.Root, device: config.Device, interface: str, protocol: Protocol):
    if protocol != Protocol.MODBUS:
        yield
        return

    interfaces = psutil.net_if_addrs()
    if not (interface_data := interfaces.get(interface, None)):
        raise DeviceError(f"Interface '{interface}' not found in {interfaces}")

    ips = [entry.address for entry in interface_data if entry.family == socket.AF_INET]
    addresses = [socket.inet_aton(ip) for ip in ips]

    with _model_server(model, device, ips[0]) as (model_port, model_path):
        info = ServiceInfo(
            "_modbus._tcp.local.",
            f"{device.name} ({addresses})._modbus._tcp.local.",
            int(device.modbus.port, 0) if device.modbus else 502,
            addresses=addresses,
            properties={
                "model-port": model_port,
                "model-path": model_path,
                "device-id": device.id,
            },
        )
        zeroconf = Zeroconf()
        try:
            zeroconf.register_service(info)
            yield
        finally:
            zeroconf.close()
