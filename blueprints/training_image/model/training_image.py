from .training_image_label import TrainingImageLabel

class TrainingImage:
    def __init__(self, id = None, image = None, source = None, label = None, is_labelled = False):
        self.__valid_sources = [None, 'Google', 'Admin', 'User']
        self._id = id
        self._image = image

        if source not in self.__valid_sources:
            raise Exception("Training image source not recognised: ", source)
        self._source = source

        if not label == None:
            if not isinstance(label, TrainingImageLabel):
                raise Exception("Label is not a valid training image label: ", label)
        self._label = label

        self._is_labelled = is_labelled

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_image(self):
        return self._image

    def set_image(self, image):
        self._image = image

    def get_source(self):
        return self._source

    def set_source(self, source):
        if source not in self.__valid_sources:
            raise Exception("Training image source not recognised: ", source)
        self._source = source

    def get_label(self):
        return self._label

    def set_label(self, label):
        if not label == None:
            if not isinstance(label, TrainingImageLabel):
                raise Exception("Label is not a valid training image label: ", label)
        self._label = label

    def get_is_labelled(self):
        return self._is_labelled

    def set_is_labelled(self, is_labelled):
        self._is_labelled = is_labelled