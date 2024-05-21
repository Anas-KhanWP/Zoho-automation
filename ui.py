import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QSpinBox, QMessageBox
from PyQt5.QtGui import QFont, QColor
from functions.helper_functions import main

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Zoho Surcharge Automation')
        self.setStyleSheet("font-family: 'Segoe UI', sans-serif;")

        layout = QVBoxLayout()

        # Title label
        title_label = QLabel('Zoho Surcharge Automation', self)
        title_font = QFont('Segoe UI', 34, QFont.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # Function name input
        self.label_function_name = QLabel('Enter Function Name:', self)
        self.label_function_name.setFont(QFont('Segoe UI', 13, QFont.Bold))
        layout.addWidget(self.label_function_name)
        self.input_function_name = QLineEdit(self)
        self.input_function_name.setStyleSheet("color: #fff;")
        self.input_function_name.setFont(QFont('Segoe UI', 12))
        layout.addWidget(self.input_function_name)

        # Number of tabs input
        self.label_num_tabs = QLabel('Number of Tabs to Open:', self)
        self.label_num_tabs.setFont(QFont('Segoe UI', 13, QFont.Bold))
        layout.addWidget(self.label_num_tabs)
        self.input_num_tabs = QSpinBox(self)
        self.input_num_tabs.setMinimum(1)
        self.input_num_tabs.setMaximum(999)
        self.input_num_tabs.setFont(QFont('Segoe UI', 12))
        self.input_num_tabs.setStyleSheet("color: #fff;")
        layout.addWidget(self.input_num_tabs)
        
        # Run button
        self.run_button = QPushButton('Run Automation', self)
        run_button_font = QFont('Segoe UI', 12, QFont.Bold)
        self.run_button.setFont(run_button_font)
        self.run_button.setStyleSheet("background-color: #4B8BBE; color: #FFFFFF;")
        self.run_button.clicked.connect(self.run_script)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def run_script(self):
        function_name = self.input_function_name.text().strip()
        num_tabs = self.input_num_tabs.value()
        if function_name:
            main(function_name, num_tabs)
        else:
            QMessageBox.critical(self, 'Error', 'Please enter a function name.', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Set custom Fusion style
    app_palette = app.palette()
    app_palette.setColor(app_palette.Window, QColor("#333"))  # Dark background
    app_palette.setColor(app_palette.WindowText, QColor("#f0f0f0"))  # Light text color
    app_palette.setColor(app_palette.Base, QColor("#666"))  # Darker base color
    app_palette.setColor(app_palette.Button, QColor("#4B8BBE"))  # Blue button color
    app_palette.setColor(app_palette.ButtonText, QColor("#FFFFFF"))  # White text on buttons
    app.setPalette(app_palette)

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
