# This project was inspired by the research detailed in:
# "Fuzzing for Power Grids: A Comparative Study of Existing Frameworks and a New Method for Detecting Silent Crashes in Control Devices"
# Authors: Marie Louise Uwibambe, Yanjun Pan, Qinghua Li
# Email: {uwibambe, yanjunp, qinghual} @uark.edu
# Published in: University of Arkansas

from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

import sys


def main():
    app = QApplication(sys.argv)

    app.setStyle("Fusion")
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()