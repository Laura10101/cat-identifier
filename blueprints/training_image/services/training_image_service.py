from ..model import TrainingImage, TrainingImageLabel
from ..data import TrainingImageRepository

class TrainingImageService:
    def __init__(self):
        pass

    def create_training_image(self, image):
        image = TrainingImage(image=image, source='Admin', label=TrainingImageLabel(), is_labelled=False)
        repo = TrainingImageRepository()
        return repo.create_one(image)