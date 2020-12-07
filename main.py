from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow
import sys

def main():
    Application = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(Application.exec_())

if __name__ == "__main__":
    main()
