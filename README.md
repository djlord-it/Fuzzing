# EM Signal Analyzer with Modbus Integration

## Overview
This project is inspired by the research paper:

**"Fuzzing for Power Grids: A Comparative Study of Existing Frameworks and a New Method for Detecting Silent Crashes in Control Devices"**

- **Authors**: Marie Louise Uwibambe, Yanjun Pan, Qinghua Li
- **Affiliation**: Department of Electrical Engineering and Computer Science, University of Arkansas
- **Contact**: {uwibambe, yanjunp, qinghual}@uark.edu
- **Published By**: University of Arkansas

The program implements an **Electromagnetic (EM) Signal Analysis** tool with a **Modbus server-client interface** to analyze, visualize, and detect silent crashes in control systems, aligning with the research paper's objectives.

---

## Features
1. **EM Signal Analysis**:
   - Generate normal operation signals.
   - Simulate crash signals with noise.
   - Analyze signals for characteristics like RMS, peak-to-peak amplitude, and SNR.
   - Visualize normal and crash signals side-by-side.

2. **Modbus Protocol Integration**:
   - Start and stop a Modbus TCP server.
   - Simulate client-server interactions with register reading/writing.

3. **Interactive GUI**:
   - Configure signal analysis parameters (sample rate, duration, thresholds, etc.).
   - Visualize results and save outputs.
   - Manage Modbus server settings from the GUI.

4. **Crash Detection Simulation**:
   - Demonstrate signal deviation under crash conditions.

---

## File Structure

### 1. Configuration Files
- `config.py`: Defines the structure for signal and Modbus configuration. Loads settings from `config.yml`.
- `config.yml`: YAML configuration file specifying Modbus and signal parameters.

### 2. Core Modules
- `main.py`: Entry point for the application.
- `main_window.py`: Implements the GUI for signal analysis and Modbus server management.
- `modbus_client.py`: Handles Modbus client operations (read/write registers).
- `modbus_server.py`: Implements a Modbus server with simulated register data.
- `signal_processor.py`: Processes and analyzes EM signals, simulates normal and crash signals.

### 3. Research Reference
This project aligns with the methods and concepts presented in the referenced paper, particularly the use of EM waves to monitor silent crashes in control devices.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/djlord-it/Fuzzing.git
   cd Fuzzing
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

---

## Usage

### Configuring Parameters
1. Edit the `config.yml` file to set default Modbus and signal parameters.
2. Alternatively, use the GUI to modify parameters dynamically.

### Signal Analysis
1. Set signal parameters (sample rate, duration, thresholds) in the GUI.
2. Click "Analyze Signals" to generate and analyze normal and crash signals.
3. View results in the plot and text output section.
4. Save results by clicking "Save Results."

### Modbus Server
1. Set the desired port for the Modbus server.
2. Start the server using the "Start Modbus Server" button.
3. Stop the server using the same button.

### Modbus Client
1. Interact with the server using Modbus read/write commands.
2. Simulate crashes or abnormal register values to observe system responses.

---

## Signal Analysis Details
- **Normal Signal**: A sinusoidal wave representing regular operation.
- **Crash Signal**: A combination of attenuated normal signals and Gaussian noise to simulate abnormal conditions.
- **Analysis Metrics**:
  - **RMS (Root Mean Square)**: Measures signal power.
  - **Peak-to-Peak Amplitude**: Indicates signal range.
  - **SNR (Signal-to-Noise Ratio)**: Quantifies signal clarity.

---

## Dependencies
- Python 3.8+
- PyQt6
- numpy
- matplotlib
- pyModbusTCP
- pyyaml

---

## Credits
This project is heavily inspired by the research work "Fuzzing for Power Grids" and incorporates concepts from the study into a practical implementation. Special thanks to the authors for their valuable contributions to the field.

---

## Future Work
- Integrate real EM signal acquisition using hardware probes.
- Expand crash scenarios for more robust detection.
- Implement machine learning models for anomaly detection.
- Benchmark performance against existing fuzzing frameworks.

---

## License
This project is released under the MIT License. See the LICENSE file for details.
