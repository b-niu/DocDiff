import sys
from PySide6.QtWidgets import QApplication
from docdiff.gui.main_window import DocDiffWindow

def main():
    app = QApplication(sys.argv)
    
    # Enable smooth scaling
    app.setApplicationName("DocDiff")
    app.setOrganizationName("DocDiff")

    window = DocDiffWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
