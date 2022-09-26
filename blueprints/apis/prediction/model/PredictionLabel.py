from blueprints.apis.prediction.model.Prediction import Prediction


class PredictionLabel:
    def __init__(self, is_cat = False, colour = None, is_tabby = False, pattern = None, is_pointed=False):
        self.__valid_colours = PredictionLabel.get_valid_colours()
        self.__valid_patterns = PredictionLabel.get_valid_patterns()

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

    @staticmethod
    def get_valid_colours():
        return [None, 'Black', 'Blue', 'Chocolate', 'Lilac', 'Cinnamon', 'Fawn']

    @staticmethod
    def get_valid_patterns():
        return [None, 'Self', 'Bicolour', 'Van']

    @staticmethod
    def from_prediction_output(prediction):
        #Output label order is:
        #is_cat [0], colour [1-6], is_tabby [7], pattern [8-10], is_pointed [11]
        #For boolean labels, >0.5 is true, otherwise false
        is_cat = prediction[0] > 0.5
        is_tabby = prediction[7] > 0.5
        is_pointed = prediction[11] > 0.5

        #colour and pattern were one-hot encoded, so have to be
        #decoded
        #this works by figuring out which colour scored the
        #highest probability
        colour_pred = prediction[1:6]
        colour_index = PredictionLabel.__find_best_scoring_index(colour_pred)
        #now look up the value in the list of valid colours, which includes
        #none as an extra value that doesn't appear in the prediction array
        colour = PredictionLabel.get_valid_colours()[colour_index + 1]

        pattern_pred = prediction[8:10]
        pattern_index = PredictionLabel.__find_best_scoring_index(pattern_pred)
        pattern = PredictionLabel.get_valid_patterns()[pattern_index + 1]

        return PredictionLabel(
            is_cat=is_cat,
            colour=colour,
            is_tabby=is_tabby,
            pattern=pattern,
            is_pointed=is_pointed
        )

    @staticmethod
    def __find_best_scoring_index(lst):
        #return the index of the max value in the list
        #will only return the first instance
        return lst.index(max(lst))