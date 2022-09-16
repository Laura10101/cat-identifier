class TrainingImageLabel:
    def __init__(self, is_cat = False, colour = None, is_tabby = False, pattern = None, is_pointed=False):
        self.__valid_colours = [None, 'Black', 'Blue', 'Chocolate', 'Lilac', 'Cinnamon', 'Fawn']
        self.__valid_patterns = [None, 'Self', 'Bicolour', 'Van']

        self._is_cat = is_cat

        if not colour in self.__valid_colours:
            raise Exception("Cat colour is not valid: ", colour)
        self._colour = colour

        self._is_tabby = is_tabby

        if not pattern in self.__valid_patterns:
            raise Exception("Cat pattern is not valid: ", pattern)
        self._pattern = pattern

        self._is_pointed = is_pointed

    def get_is_cat(self):
        return self._is_cat

    def set_is_cat(self, is_cat):
        self._is_cat = is_cat

    def get_colour(self):
        return self._colour

    def set_colour(self, colour):
        if not colour in self.__valid_colours:
            raise Exception("Cat colour is not valid: ", colour)
        self._colour = colour

    def get_is_tabby(self):
        return self._is_tabby

    def set_is_tabby(self, is_tabby):
        self._is_tabby = is_tabby

    def get_pattern(self):
        return self._pattern

    def set_pattern(self, pattern):
        if not pattern in self.__valid_patterns:
            raise Exception("Cat pattern is not valid: ", pattern)
        self._pattern = pattern

    def get_is_pointed(self):
        return self._is_pointed

    def set_is_pointed(self, is_pointed):
        self._is_pointed = is_pointed

    def serialize(self):
        return {
            "is_cat": self.get_is_cat(),
            "colour": self.get_colour(),
            "is_tabby": self.get_is_tabby(),
            "pattern": self.get_pattern(),
            "is_pointed": self.get_is_pointed()
        }