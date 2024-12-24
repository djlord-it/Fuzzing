from pyModbusTCP.server import DataBank, ModbusServer
import threading
import time
import logging
from config import ModbusConfig

logger = logging.getLogger(__name__)


class ModbusServerHandler:
    def __init__(self, config: ModbusConfig):
        self.config = config
        self.server = ModbusServer(
            host=config.host,
            port=config.port,
            no_block=True
        )
        self._running = False
        self._thread = None

    def start(self):
        """Start the Modbus server in a separate thread."""
        if self._running:
            logger.warning("Server already running")
            return

        self._running = True
        self._thread = threading.Thread(target=self._run_server)
        self._thread.daemon = True
        self._thread.start()
        logger.info("Modbus server started")

    def stop(self):
        """Stop the Modbus server gracefully."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5.0)
        self.server.stop()
        logger.info("Modbus server stopped")

    def _run_server(self):
        """Main server loop."""
        self.server.start()
        while self._running:
            try:
                # Update registers with some example data
                DataBank.set_words(0, [123, 456])
                time.sleep(1.0)
            except Exception as e:
                logger.error(f"Server error: {str(e)}")
                break
        self.server.stop()
