from requests import post

#This class provides a wrapper around the Predictions API
#It is used to post trained models to the prediction API
#so that the Prediction API can use these for prediction-making
class PredictionAPIClient:
    def __init__(self, config):
        self.__base_url = config["API_BASE_URL"]

    def post_trained_model(self, serialised_model):
        headers = {
            "Content-Type": "application/json"
        }
        response = post(
            url=self.__base_url + "/model",
            headers=headers,
            json=serialised_model
        )
        return response.ok