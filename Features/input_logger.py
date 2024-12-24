import logging
import datetime

class InputLogger:
    def __init__(self, log_file="user_interactions.log"):
        logging.basicConfig(filename=log_file, level=logging.INFO)

    def log_action(self, action: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{timestamp} - {action}")

# Example Usage
if __name__ == "__main__":
    logger = InputLogger()
    logger.log_action("Started Modbus server")
    logger.log_action("Analyzed EM signals")
