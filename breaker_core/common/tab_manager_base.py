import time

class TabManagerBase:
    
    def __init__(self) -> None:
        self.window_handle = None

    def make_active(self):
        if not self.webdriver.current_window_handle == self.window_handle:
            self.webdriver.switch_to.window(str(self.window_handle))
            time.sleep(0.1)