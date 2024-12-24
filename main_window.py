from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QSpinBox, QDoubleSpinBox,
                             QStatusBar, QFileDialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from signal_processor import EMSignalProcessor
from modbus_server import ModbusServerHandler
from config import SignalConfig, ModbusConfig


class ModernButton(QPushButton):
    """Custom styled button with modern appearance"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0051FF;
            }
            QPushButton:pressed {
                background-color: #0040FF;
            }
            QPushButton:disabled {
                background-color: #B4B4B4;
            }
        """)


class ParameterWidget(QWidget):
    """Widget for parameter inputs with modern styling"""

    def __init__(self, label, min_val, max_val, default_val, step, is_float=False):
        super().__init__()
        layout = QHBoxLayout()

        label = QLabel(label)
        label.setStyleSheet("font-size: 14px; color: #333333;")

        if is_float:
            self.spinner = QDoubleSpinBox()
            self.spinner.setDecimals(2)
        else:
            self.spinner = QSpinBox()

        self.spinner.setStyleSheet("""
            QSpinBox, QDoubleSpinBox {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px;
                min-width: 100px;
            }
        """)

        self.spinner.setRange(min_val, max_val)
        self.spinner.setValue(default_val)
        self.spinner.setSingleStep(step)

        layout.addWidget(label)
        layout.addWidget(self.spinner)
        self.setLayout(layout)

    def value(self):
        return self.spinner.value()


class SignalPlotWidget(QWidget):
    """Widget for displaying signal plots"""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_signals(self, time, normal_signal, crash_signal):
        self.ax.clear()
        self.ax.plot(time, normal_signal, label="Normal Signal", alpha=0.8)
        self.ax.plot(time, crash_signal, label="Crash Signal", alpha=0.8)
        self.ax.grid(True)
        self.ax.legend()
        self.ax.set_title("EM Signal Comparison")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.figure.tight_layout()
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EM Signal Analyzer")
        self.setMinimumSize(1000, 600)

        # Initialize central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Create side panel for controls
        control_panel = QWidget()
        control_panel.setMaximumWidth(300)
        control_layout = QVBoxLayout(control_panel)
        control_layout.setSpacing(20)

        # Add title
        title = QLabel("Signal Parameters")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #333333;
            margin: 10px 0;
        """)
        control_layout.addWidget(title)

        # Add parameter inputs
        self.sample_rate = ParameterWidget("Sample Rate (Hz)", 100, 10000, 1000, 100)
        self.duration = ParameterWidget("Duration (s)", 0.1, 10.0, 1.0, 0.1, True)
        self.trigger = ParameterWidget("Trigger Threshold", 0.1, 1.0, 0.3, 0.1, True)
        self.noise = ParameterWidget("Noise Threshold", 0.01, 0.5, 0.1, 0.01, True)

        for widget in [self.sample_rate, self.duration, self.trigger, self.noise]:
            control_layout.addWidget(widget)

        # Add Modbus settings
        modbus_title = QLabel("Modbus Settings")
        modbus_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #333333;
            margin: 10px 0;
        """)
        control_layout.addWidget(modbus_title)

        self.port = ParameterWidget("Port", 1024, 65535, 5020, 1)
        control_layout.addWidget(self.port)

        # Add control buttons
        self.analyze_button = ModernButton("Analyze Signals")
        self.analyze_button.clicked.connect(self.analyze_signals)

        self.start_server_button = ModernButton("Start Modbus Server")
        self.start_server_button.clicked.connect(self.toggle_server)

        self.save_button = ModernButton("Save Results")
        self.save_button.clicked.connect(self.save_results)

        for button in [self.analyze_button, self.start_server_button, self.save_button]:
            control_layout.addWidget(button)

        control_layout.addStretch()

        # Create main content area
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)

        # Add plot widget
        self.plot_widget = SignalPlotWidget()
        content_layout.addWidget(self.plot_widget)

        # Add results display
        self.results_label = QLabel()
        self.results_label.setStyleSheet("""
            font-size: 14px;
            color: #333333;
            padding: 10px;
            background-color: #F5F5F5;
            border-radius: 4px;
        """)
        content_layout.addWidget(self.results_label)

        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Add panels to main layout
        main_layout.addWidget(control_panel)
        main_layout.addWidget(content_area, stretch=1)

        # Initialize server state
        self.server_handler = None
        self.server_running = False

    def analyze_signals(self):
        """Analyze signals with current parameters"""
        try:
            # Create configuration
            signal_config = SignalConfig(
                sample_rate=self.sample_rate.value(),
                duration=self.duration.value(),
                trigger_threshold=self.trigger.value(),
                noise_threshold=self.noise.value()
            )

            # Initialize processor
            processor = EMSignalProcessor(signal_config)

            # Generate signals
            normal_signal = processor.generate_normal_signal()
            crash_signal = processor.generate_crash_signal()

            # Analyze signals
            normal_analysis = processor.analyze_signal(normal_signal)
            crash_analysis = processor.analyze_signal(crash_signal)

            # Update plot
            self.plot_widget.plot_signals(processor.time, normal_signal, crash_signal)

            # Update results display
            results_text = f"""
            Normal Signal Analysis:
            - RMS: {normal_analysis.rms:.3f}
            - SNR: {normal_analysis.snr:.3f} dB
            - Peak-to-Peak: {normal_analysis.peak_to_peak:.3f}

            Crash Signal Analysis:
            - RMS: {crash_analysis.rms:.3f}
            - SNR: {crash_analysis.snr:.3f} dB
            - Peak-to-Peak: {crash_analysis.peak_to_peak:.3f}
            """
            self.results_label.setText(results_text)

            self.status_bar.showMessage("Analysis completed successfully", 3000)

        except Exception as e:
            self.status_bar.showMessage(f"Error: {str(e)}", 5000)

    def toggle_server(self):
        """Start or stop the Modbus server"""
        if not self.server_running:
            try:
                modbus_config = ModbusConfig(
                    host="127.0.0.1",
                    port=self.port.value(),
                    timeout=3,
                    retries=3
                )

                self.server_handler = ModbusServerHandler(modbus_config)
                self.server_handler.start()

                self.server_running = True
                self.start_server_button.setText("Stop Modbus Server")
                self.start_server_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FF3B30;
                    }
                    QPushButton:hover {
                        background-color: #FF2D20;
                    }
                """)
                self.status_bar.showMessage("Modbus server started", 3000)

            except Exception as e:
                self.status_bar.showMessage(f"Server error: {str(e)}", 5000)
        else:
            try:
                if self.server_handler:
                    self.server_handler.stop()
                self.server_running = False
                self.start_server_button.setText("Start Modbus Server")
                self.start_server_button.setStyleSheet("")
                self.status_bar.showMessage("Modbus server stopped", 3000)
            except Exception as e:
                self.status_bar.showMessage(f"Error stopping server: {str(e)}", 5000)

    def save_results(self):
        """Save plot and results to file"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Results",
                "",
                "PNG Files (*.png);;All Files (*)"
            )

            if file_path:
                self.plot_widget.figure.savefig(file_path)
                self.status_bar.showMessage(f"Results saved to {file_path}", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Error saving results: {str(e)}", 5000)

    def closeEvent(self, event):
        """Clean up when closing the application"""
        if self.server_handler:
            self.server_handler.stop()
        event.accept()