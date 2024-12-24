from pyModbusTCP.client import ModbusClient
import logging
import time
from typing import List, Optional
from config import ModbusConfig

logger = logging.getLogger(__name__)


class ModbusClientHandler:
    def __init__(self, config: ModbusConfig):
        self.config = config
        self.client = ModbusClient(
            host=config.host,
            port=config.port,
            timeout=config.timeout,
            auto_open=True,
            auto_close=True
        )

    def read_registers(self, address: int, count: int) -> Optional[List[int]]:
        """Read holding registers with retry logic."""
        for attempt in range(self.config.retries):
            try:
                registers = self.client.read_holding_registers(address, count)
                if registers is not None:
                    return registers
                logger.warning(f"Read attempt {attempt + 1} failed")
            except Exception as e:
                logger.error(f"Error reading registers: {str(e)}")
            time.sleep(0.1)
        return None

    def write_register(self, address: int, value: int) -> bool:
        """Write to a single register with validation."""
        if not (0 <= value <= 65535):
            logger.error(f"Invalid value {value} for Modbus register")
            return False

        for attempt in range(self.config.retries):
            try:
                if self.client.write_single_register(address, value):
                    return True
                logger.warning(f"Write attempt {attempt + 1} failed")
            except Exception as e:
                logger.error(f"Error writing register: {str(e)}")
            time.sleep(0.1)
        return False