from re import M


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

    #create method to check that label contains enough information for training 
    def is_sufficient_for_training(self):
        #use the 'in' keyword to validate both colour and pattern are set to valid values
        #and that they are not 'none'
        return not self.get_colour() == None and self.get_colour() in self.__valid_colours and not self.get_pattern() == None and self.get_pattern() in self.__valid_patterns

    #create method to convert training image labels into numerical data for ML model 
    def get_numeric_label(self):
        #create new array
        numeric_label = []
        #for each attribute of the label, convert the value to a number and add to the list 
        numeric_label.append(int(self.get_is_cat() == True))

        #Add a label for each valid colour which indicates whether this label matches that colour
        for colour in self.__valid_colours:
            if not colour is None:
                numeric_label.append(int(self.get_colour() == colour))
        
        numeric_label.append(int(self.get_is_tabby() == True))

        #Add a label for each valid pattern which indicates whether this label matches that pattern
        for pattern in self.__valid_patterns:
            if not pattern is None:
                numeric_label.append(int(self.get_pattern() == pattern))

        numeric_label.append(int(self.get_is_pointed() == True))
        return numeric_label

    def serialize(self):
        return {
            "is_cat": self.get_is_cat(),
            "colour": self.get_colour(),
            "is_tabby": self.get_is_tabby(),
            "pattern": self.get_pattern(),
            "is_pointed": self.get_is_pointed()
        }