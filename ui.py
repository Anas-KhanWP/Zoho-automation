import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QSpinBox, QMessageBox, QTextEdit, QProgressBar
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from functions.helper_functions import main, login
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from datetime import datetime
import logging

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Zoho Surcharge Automation')
        self.setStyleSheet("font-family: 'Segoe UI', sans-serif; background-color: #282c34; color: #f0f0f0;")
        self.setWindowIcon(QIcon('zoho.png'))

        layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        # Title label
        title_label = QLabel('Zoho Surcharge Automation', self)
        title_font = QFont('Segoe UI', 34, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Function name input
        self.label_function_name = QLabel('Enter Function Name:', self)
        self.label_function_name.setFont(QFont('Segoe UI', 13, QFont.Bold))
        layout.addWidget(self.label_function_name)
        self.input_function_name = QLineEdit(self)
        self.input_function_name.setStyleSheet("background-color: #444; color: #fff; padding: 5px;")
        self.input_function_name.setFont(QFont('Segoe UI', 12))
        layout.addWidget(self.input_function_name)

        # Minimum Number of tabs input
        self.label_num_tabs = QLabel('Min Functions:', self)
        self.label_num_tabs.setFont(QFont('Segoe UI', 13, QFont.Bold))
        h_layout.addWidget(self.label_num_tabs)
        self.min_input_num_tabs = QSpinBox(self)
        self.min_input_num_tabs.setMinimum(1)
        self.min_input_num_tabs.setMaximum(999)
        self.min_input_num_tabs.setFont(QFont('Segoe UI', 12))
        self.min_input_num_tabs.setStyleSheet("background-color: #444; color: #fff; padding: 5px;")
        h_layout.addWidget(self.min_input_num_tabs)
        
        # Maximum Number of functions input
        self.label_max_num_tabs = QLabel('Max Functions:', self)
        self.label_max_num_tabs.setFont(QFont('Segoe UI', 13, QFont.Bold))
        h_layout.addWidget(self.label_max_num_tabs)
        self.max_input_num_tabs = QSpinBox(self)
        self.max_input_num_tabs.setMinimum(1)
        self.max_input_num_tabs.setMaximum(999)
        self.max_input_num_tabs.setFont(QFont('Segoe UI', 12))
        self.max_input_num_tabs.setStyleSheet("background-color: #444; color: #fff; padding: 5px;")
        h_layout.addWidget(self.max_input_num_tabs)
        
        layout.addLayout(h_layout)
        
        # Run button
        self.run_button = QPushButton('Run Automation', self)
        run_button_font = QFont('Segoe UI', 12, QFont.Bold)
        self.run_button.setFont(run_button_font)
        self.run_button.setStyleSheet("background-color: #4B8BBE; color: #FFFFFF; padding: 10px;")
        self.run_button.clicked.connect(self.run_script)
        layout.addWidget(self.run_button)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Error log
        self.error_log = QTextEdit(self)
        self.error_log.setReadOnly(True)
        self.error_log.setFont(QFont('Segoe UI', 10))
        self.error_log.setStyleSheet("background-color: #444; color: #f0f0f0; padding: 5px;")
        layout.addWidget(self.error_log)

        self.setLayout(layout)

    def run_script(self):
        function_name = self.input_function_name.text().strip()
        min_num_tabs = self.min_input_num_tabs.value()
        max_num_tabs = self.max_input_num_tabs.value()

        if function_name:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress bar

            # Append "Working..." in bold to the error log
            self.error_log.append('<span style="font-weight: bold;">Working...</span>')

            # Start a thread to run the script
            self.worker = WorkerThread(function_name, min_num_tabs, max_num_tabs)
            self.worker.finished.connect(self.on_finished)
            self.worker.error.connect(self.on_error)
            self.worker.start()
        else:
            QMessageBox.critical(self, 'Error', 'Please enter a function name.', QMessageBox.Ok)

    def on_finished(self, data):
        self.progress_bar.setVisible(False)
        successful_functions = "<br>".join(data.get("successful_functions", []))
        status = data.get("status", "Unknown")
        self.error_log.append(f'<h2 style="font-size: 13px; font-weight: bold;">Status:</h2> <h2 style="font-size: 13px; font-weight: bold; color: green;">{status}</h2>\n\n<h2 style="font-size: 13px; font-weight: bold;">Successful Functions:</h2>\n<span style="font-size: 12px;">{successful_functions}</span>')
        QMessageBox.information(self, 'Success', 'Run Successful.', QMessageBox.Ok)

    def on_error(self, error):
        self.progress_bar.setVisible(False)
        self.error_log.append(f"Error: {error}")
        QMessageBox.critical(self, 'Error', f'An error occurred: {str(error)}', QMessageBox.Ok)

class WorkerThread(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, function_name, min_num_tabs, max_num_tabs):
        super().__init__()
        self.function_name = function_name
        self.min_num_tabs = min_num_tabs
        self.max_num_tabs = max_num_tabs

    def run(self):
        successful_functions = []
        status = "Success"

        current_min = self.min_num_tabs
        current_max = min(current_min + 19, self.max_num_tabs)
        
        # Setup logging
        today_date = datetime.now().strftime("%Y-%m-%d")
        log_filename = f"log_{today_date}.log"
        logging.basicConfig(
            filename=log_filename, 
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(__name__)
        
        # Setup Chrome options to prevent bot detection
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize the undetected Chrome WebDriver with options
        driver = uc.Chrome(options=chrome_options)
        
        wait = WebDriverWait(driver, 30)
        result_wait = WebDriverWait(driver, 500)
        actions = ActionChains(driver)

        should_login = True
        open_tabs = True
        try:
            while current_min <= self.max_num_tabs:
                print(f"Current Min: {current_min} | Current Max: {current_max}")
                data = main(
                    self.function_name,
                    current_min,
                    current_max,
                    driver=driver,
                    logger=logger,
                    wait=wait,
                    result_wait=result_wait,
                    actions=actions,
                    should_login=should_login,
                    open_tabs=open_tabs
                )
                
                if "successful_functions" in data:
                    successful_functions.extend(data["successful_functions"])
                else:
                    status = "Partial Success"
                
                # Update for the next batch
                current_min = current_max + 1
                current_max = min(current_min + 19, self.max_num_tabs)
                
                should_login = False
                open_tabs = False

            result = {"successful_functions": successful_functions, "status": status}
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Set custom Fusion style
    app_palette = app.palette()
    app_palette.setColor(app_palette.Window, QColor("#282c34"))  # Dark background
    app_palette.setColor(app_palette.WindowText, QColor("#f0f0f0"))  # Light text color
    app_palette.setColor(app_palette.Base, QColor("#444"))  # Darker base color
    app_palette.setColor(app_palette.Button, QColor("#4B8BBE"))  # Blue button color
    app_palette.setColor(app_palette.ButtonText, QColor("#FFFFFF"))  # White text on buttons
    app.setPalette(app_palette)

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
