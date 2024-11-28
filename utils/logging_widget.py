import logging
import sys
from PyQt6.QtWidgets import QTextBrowser

class QTextBrowserHandler(logging.Handler):
    def __init__(self, text_browser):
        super().__init__()
        self.text_browser = text_browser
        # Use same formatter as console handler
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        self.text_browser.append(msg)

# Dual logger setup (console and QTextBrowser)
def setup_logger(text_browser=None, name='pyqt_app' , level=logging.DEBUG, is_console=True):
    # Root logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear existing handlers to prevent duplicates
    logger.handlers.clear()

    # Console Handler (keeps console output)
    if is_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_handler)

    # QTextBrowser Handler (if provided)
    if text_browser:
        text_browser_handler = QTextBrowserHandler(text_browser)
        text_browser_handler.setLevel(level)
        logger.addHandler(text_browser_handler)

    return logger
