from pyModbusTCP.client import ModbusClient
import logging
import numpy as np

class ProtocolTester:
    def __init__(self, host: str, port: int):
        self.client = ModbusClient(host=host, port=port, auto_open=True, auto_close=True)
        logging.basicConfig(level=logging.INFO)

    def fuzz_test_registers(self, start_address: int, end_address: int, iterations: int):
        """Perform fuzz testing on Modbus registers."""
        for _ in range(iterations):
            address = np.random.randint(start_address, end_address + 1)
            value = np.random.randint(0, 65536)
            success = self.client.write_single_register(address, value)
            if success:
                logging.info(f"Successfully wrote value {value} to address {address}")
            else:
                logging.error(f"Failed to write value {value} to address {address}")

# Example Usage
if __name__ == "__main__":
    tester = ProtocolTester(host="127.0.0.1", port=5020)
    tester.fuzz_test_registers(0, 10, 20)
