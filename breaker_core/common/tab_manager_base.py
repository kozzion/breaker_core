import time
from pynput.keyboard import Key, Controller
from selenium.webdriver.common.by import By

class TabManagerBase:
    
    def __init__(self) -> None:
        self.window_handle = None

    def make_active(self):
        if not self.webdriver.current_window_handle == self.window_handle:
            self.webdriver.switch_to.window(str(self.window_handle))
            time.sleep(0.1)


    def upload_file(self, element_button, path_file_upload):
        element_button.click()
        time.sleep(1)
        keyboard = Controller()
        keyboard.type(path_file_upload)
        keyboard.press(Key.enter)
        time.sleep(1)

    def find_elements_by_inner_html_contains(self, element_source, type_find, query_find, inner_html_contains):
        list_element = element_source.find_elements(type_find, query_find)
        list_element_selected = []
        for element in list_element:
            if inner_html_contains in element.get_attribute("innerHTML"):
                list_element_selected.append(element)
        return list_element_selected
        
    def find_elements_by_inner_html_equals(self, element_source, type_find, query_find, inner_html_equals):
        list_element = element_source.find_elements(type_find, query_find)
        list_element_selected = []
        for element in list_element:
            if element.get_attribute("innerHTML").strip() == inner_html_equals:
                list_element_selected.append(element)

        return list_element_selected

    def find_parent(self, element_source):
        return element_source.find_element_by_xpath('..')

    def find_descibing_list_text(self, element_source, recursion_limit=5):
        element_current = element_source
        for i in range(recursion_limit):
            list_element = element_current.find_elements(By.TAG_NAME, 'span')
            if len(list_element) == 0:
                element_current = self.find_parent(element_current)
            else:
                return [element.get_attribute("innerHTML") for element in list_element]
