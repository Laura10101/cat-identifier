#Represents a single entry to the model training log
class TrainingLogEntry:
    def __init__(self, timestamp, message):
        self.__timestamp = timestamp
        self.__message = message

    def get_timestamp(self):
        return self.__timestamp

    def get_message(self):
        return self.__message

    def as_string(self):
        return "[" + self.__timestamp + "] " + self.__message

    def serialize(self):
        return {
            "timestamp": self.get_timestamp(),
            "message": self.get_message()
        }
