import sys
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

    @staticmethod
    def find_parent(element):
        return element.find_element(By.XPATH, '..')

    @staticmethod
    def find_children(element):
        return element.find_elements(By.XPATH, './/*')

    @staticmethod
    def strip_tags(element):
        html = element.get_attribute("innerHTML")
        list_string = []
        index_current = 0
        level_open = 0
        while True:
            index_open = html.find('<', index_current)
            index_close = html.find('>', index_current)
            if index_open == -1 and index_close == -1:
                if level_open == 0:
                    string = html[index_current:].strip()
                    if 0 < len(string):
                        list_string.append(string)
                return list_string
            elif index_open == -1:
                level_open -= 1
                index_current = index_close + 1
            elif index_close == -1:
                if level_open == 0:
                    string = html[index_current:index_open].strip()
                    if 0 < len(string):
                        list_string.append(string)
                level_open += 1
                index_current = index_open + 1
            elif index_open < index_close:
                if level_open == 0:
                    string = html[index_current:index_open].strip()
                    if 0 < len(string):
                        list_string.append(string)
                level_open += 1
                index_current = index_open + 1
            else: 
                level_open -= 1
                index_current = index_close + 1

    def find_descibing_list_text(self, element_source, recursion_limit=5):
        element_current = element_source
        for i in range(recursion_limit):
            list_text = []
            list_text.extend(TabManagerBase.strip_tags(element_current))
            if 0 < len(list_text):
                return list_text
            else:
                list_element = []
                list_element.extend(element_current.find_elements(By.TAG_NAME, 'span'))
                list_element.extend(element_current.find_elements(By.TAG_NAME, 'label'))
                for element in list_element:
                    list_text.extend(TabManagerBase.strip_tags(element))
                
                if 0 < len(list_text):
                    return list_text
                element_current = self.find_parent(element_current)
        return []


