from .models import *

class AnalyticsService:
    def __init__(self, config):
        self.__config = config

    ### CREATION METHODS FOR SNAPSHOTS ###
    def create_training_images_snapshot(self, data):
        pass

    def create_predictions_snapshot(self, data):
        pass

    def create_models_snapshot(self, data):
        pass

    ### ANALYTICS METHODS ###
    def get_training_set_size_by_date(self, start_date=None, end_date=None, is_cat=None, colour=None,
        is_tabby=None, pattern=None, is_pointed=None, source=None):
        pass

    def get_training_set_size_by_label(self, start_date=None, end_date=None, is_cat=None, colour=None,
        is_tabby=None, pattern=None, is_pointed=None, source=None):
        pass

    def get_model_performance_by_date(self, start_date=None, end_date=None):
        pass

    def get_prediction_accuracy_by_date(self, start_date=None, end_date=None, is_cat=None, colour=None,
        is_tabby=None, pattern=None, is_pointed=None, user_review_status=None, admin_review_status=None):
        pass

    def get_prediction_accuracy_by_date_and_review_status(self, start_date=None, end_date=None, is_cat=None,
        colour=None, is_tabby=None, pattern=None, is_pointed=None):
        pass

    def get_prediction_acceptance_comparison(self, self, start_date=None, end_date=None, is_cat=None, colour=None,
        is_tabby=None, pattern=None, is_pointed=None):
        pass

    ### HELPER METHODS ###
    def __get_in_scope_dimension_ids(self, start_date=None, end_date=None, is_cat=None, colour=None, is_tabby=None,
        pattern=None, is_pointed=None, user_review_status=None, admin_review_status=None, source=None):
        pass

    def __list_labels(self, is_cat=None, colour=None, is_tabby=None, pattern=None, is_pointed=None):
        query = {}

        if not is_cat is None:
            query["is_cat"] = is_cat

        if not colour is None:
            query["colour"] = colour

        if not is_tabby is None:
            query["is_tabby"] = is_tabby

        if not pattern is None:
            query["pattern"] = pattern

        if not is_pointed is None:
            query["is_pointed"] = is_pointed

        return DimLabel.query.filter_by(**query).all()

    def __list_dates(self, start_date=None, end_date=None):
        if start_date is None and end_date is None:
            return DimDate.query.all()
        elif not start_date is None and not end_date is None:
            return DimDate.query.filter_by(DimDate.date >= start_date, DimDate.date <= end_date).all()
        elif not start_date is None:
            return DimDate.query.filter_by(DimDate.date >= start_date).all()
        elif not end_date is None:
            return DimDate.query.filter_by(DimDate.date <= end_date).all()

    def __list_prediction_review_statuses(self, status=None):
        if status is None:
            return DimPredictionReviewStatus.query.all()
        else:
            return DimPredictionReviewStatus.query.filter_by(DimPredictionReviewStatus.status==status)

    def __list_training_image_sources(self, source=None):
        if source is None:
            return DimTrainingImageSource.query.all()
        else:
            return DimTrainingImageSource.query.filter_by(DimTrainingImageSource.source==source)

    def __add_date_to_dimension(self, date):
        pass

    def __date_exists_in_dimension(self, date):
        matching_dates = DimDate.query.filter_by(DimDate.date == date)
        if len(matching_dates) > 1:
            raise Exception("Duplicate date identified: " + repr(matching_dates[0]))

        return len(matching_dates) == 1

    def __add_label_to_dimension(self, is_cat, colour, is_tabby, pattern, is_pointed):
        pass

    def __label_exists_in_dimension(self, is_cat, colour, is_tabby, pattern, is_pointed):
        matching_labels = self.__list_labels(is_cat, colour, is_tabby, pattern, is_pointed)
        if len(matching_labels) > 1:
            raise Exception("Duplicate label identified: " + repr(matching_labels[0]))

        return len(matching_labels) == 1

    def __add_prediction_review_status_to_dimension(self, status):
        pass

    def __prediction_review_status_exists_in_dimension(self, status):
        matching_statuses = self.__list_prediction_review_statuses(status)
        if len(matching_statuses) > 1:
            raise Exception("Duplicate status identified: " + repr(matching_statuses[0]))

        return len(matching_statuses) == 1

    def __add_training_image_source_to_dimension(self, source):
        pass

    def __training_image_source_exists_in_dimension(self, source):
        matching_sources = self.__list_training_image_sources(source)
        if len(matching_sources) > 1:
            raise Exception("Duplicate source identified: " + repr(matching_sources[0]))
        
        return len(matching_sources) == 1

    def __training_image_snapshot_exists_for_date(self, date):
        if not self.__date_exists_in_dimension(date):
            return False

        dim_date = DimDate.query.filter_by(DimDate.date == date).first()
        
        if len(dim_date.training_image_snapshots) > 1:
            raise Exception("Multiple training image snapshots found for date: " + repr(dim_date))

        return len(dim_date.training_image_snapshots) == 1
        

    def __predictions_snapshot_exists_for_date(self, date):
        if not self.__date_exists_in_dimension(date):
            return False

        dim_date = DimDate.query.filter_by(DimDate.date == date).first()
        
        if len(dim_date.prediction_snapshots) > 1:
            raise Exception("Multiple prediction snapshots found for date: " + repr(dim_date))

        return len(dim_date.prediction_snapshots) == 1

    def __models_snapshot_exists_for_date(self, date):
        if not self.__date_exists_in_dimension(date):
            return False

        dim_date = DimDate.query.filter_by(DimDate.date == date).first()
        
        if len(dim_date.model_snapshots) > 1:
            raise Exception("Multiple model snapshots found for date: " + repr(dim_date))

        return len(dim_date.model_snapshots) == 1