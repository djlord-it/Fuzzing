from pyModbusTCP.server import DataBank
from pyModbusTCP.client import ModbusClient
import threading
import time

class ModbusMonitor:
    def __init__(self, host: str, port: int):
        self.client = ModbusClient(host=host, port=port, auto_open=True, auto_close=True)

    def monitor_registers(self, addresses, interval):
        """Monitor specific Modbus registers at regular intervals."""
        while True:
            for address in addresses:
                value = self.client.read_holding_registers(address, 1)
                print(f"Address {address}: {value}")
            time.sleep(interval)

# Example Usage
if __name__ == "__main__":
    monitor = ModbusMonitor(host="127.0.0.1", port=5020)
    threading.Thread(target=monitor.monitor_registers, args=([0, 1, 2], 1)).start()
