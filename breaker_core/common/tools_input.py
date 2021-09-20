class ToolsInput:

    @staticmethod
    def promt_option(promt, list_option, allow_quit=True):
        if '' in list_option:
            raise Exception("'' not allowed as option")

        dict_option = {}
        for index_option, option in enumerate(list_option):
            str_index_option = str(index_option + 1)
            dict_option[str_index_option] = option
            print('(' + str_index_option + ') ' + option)
        if allow_quit:
            dict_option['q'] = 'quit'
        prompt = ''
        print(promt)
        while prompt not in dict_option:
            prompt = input()
        if allow_quit and dict_option[prompt] == 'quit':
            exit()
        return dict_option[prompt]

    @staticmethod
    def match(list_text, text_match):
        for text in list_text:
            if text_match in text:
                return True
        return False
        