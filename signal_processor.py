import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
import logging
from typing import Tuple, Optional
from config import SignalConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SignalAnalysis:
    positive_mean: float
    negative_mean: float
    peak_to_peak: float
    rms: float
    snr: float


class EMSignalProcessor:
    def __init__(self, config: SignalConfig):
        self.config = config
        self.time = np.linspace(0, config.duration,
                                int(config.duration * config.sample_rate))

    def generate_normal_signal(self) -> np.ndarray:
        """Generate a normal operation signal."""
        return np.sin(2 * np.pi * 10 * self.time)

    def generate_crash_signal(self) -> np.ndarray:
        """Generate a simulated crash signal."""
        normal = self.generate_normal_signal()
        noise = np.random.normal(0, self.config.noise_threshold,
                                 size=self.time.shape)
        return normal * 0.5 + noise

    def analyze_signal(self, signal: np.ndarray) -> SignalAnalysis:
        """Perform comprehensive signal analysis."""
        try:
            positive, negative = self._segment_signal(signal)
            rms = np.sqrt(np.mean(signal ** 2))
            peak_to_peak = np.max(signal) - np.min(signal)
            signal_power = np.mean(signal ** 2)
            noise_power = self.config.noise_threshold ** 2
            snr = 10 * np.log10(signal_power / noise_power)

            return SignalAnalysis(
                positive_mean=np.mean(positive),
                negative_mean=np.mean(negative),
                peak_to_peak=peak_to_peak,
                rms=rms,
                snr=snr
            )
        except Exception as e:
            logger.error(f"Error analyzing signal: {str(e)}")
            raise

    def _segment_signal(self, signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Segment signal into positive and negative components."""
        positive = signal[signal > self.config.trigger_threshold]
        negative = signal[signal < -self.config.trigger_threshold]
        return positive, negative

    def visualize_signals(self, normal: np.ndarray, crash: np.ndarray,
                          save_path: Optional[str] = None):
        """Visualize and optionally save signal comparison."""
        plt.figure(figsize=(12, 6))
        plt.plot(self.time, normal, label="Normal Signal", alpha=0.8)
        plt.plot(self.time, crash, label="Crash Signal", alpha=0.8)
        plt.grid(True)
        plt.legend()
        plt.title("EM Signal Comparison")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")

        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()