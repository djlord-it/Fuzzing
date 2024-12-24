from PyQt6.QtWidgets import QFileDialog

class GUIFeatures:
    @staticmethod
    def save_config(config, filename="config.yml"):
        """Save the current configuration to a file."""
        with open(filename, 'w') as file:
            yaml.dump(config, file)
        print(f"Configuration saved to {filename}")

    @staticmethod
    def load_config():
        """Load configuration from a file."""
        file_path, _ = QFileDialog.getOpenFileName(None, "Load Configuration", "", "YAML Files (*.yml)")
        if file_path:
            with open(file_path, 'r') as file:
                config = yaml.safe_load(file)
            print(f"Configuration loaded from {file_path}")
            return config
