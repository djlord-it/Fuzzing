import yaml
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class ModbusConfig:
    host: str
    port: int
    timeout: int = 3
    retries: int = 3


@dataclass
class SignalConfig:
    sample_rate: int
    duration: float
    trigger_threshold: float
    noise_threshold: float


def load_config(config_path: str = 'config.yml') -> Tuple[ModbusConfig, SignalConfig]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    modbus_config = ModbusConfig(**config['modbus'])
    signal_config = SignalConfig(**config['signal'])
    return modbus_config, signal_config