from datetime import datetime
from .models import *
from .database import db

class AnalyticsService:
    def __init__(self, config):
        self.__config = config

    ### CREATION METHODS FOR SNAPSHOTS ###
    def create_training_images_snapshot(self, is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed, source,
    count):

        # get timestamp for the snapshot
        date = self.__today()

        # check today's snapshot hasn't yet been posted
        if self.__training_image_snapshot_exists_for_date(date):
            raise Exception("Prediction snapshot has already been posted for date: " + str(date))

        # get the dimensions for the snapshot
        dim_date = self.__create_or_get_date(date)
        dim_label = self.__create_or_get_label(is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed)
        dim_source = self.__create_or_get_training_image_source(source)

        # add the snapshot
        snapshot = FactTrainingImagesDailySnapshot(
            date = dim_date,
            label = dim_label,
            source = dim_source,
            count=count
        )
        db.session.add(snapshot)
        db.session.commit()

    def create_predictions_snapshot(self, is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed,
    user_review_status, admin_review_status, count):
        # get the timestamp for the snapshot
        date = self.__today()

        # check today's snapshot hasn't yet been posted
        if self.__predictions_snapshot_exists_for_date(date):
            raise Exception("Prediction snapshot has already been posted for date: " + str(date))

        # get the dimensions for the snapshot
        dim_date = self.__create_or_get_date(date)
        dim_label = self.__create_or_get_label(is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed)
        dim_user_review_status = self.__create_or_get_prediction_review_status(user_review_status)
        dim_admin_review_status = self.__create_or_get_prediction_review_status(admin_review_status)

        # add the snapshot
        snapshot = FactPredictionsDailySnapshot(
            date=dim_date,
            label=dim_label,
            user_review_status=dim_user_review_status,
            admin_review_status=dim_admin_review_status,
            count=count
        )
        db.session.add(snapshot)
        db.session.commit()

    def create_models_snapshot(self, training_started, training_ended, min_acc, max_acc, avg_acc, min_loss,
    max_loss, avg_loss):
        # get timestamp for the snapshot
        date = self.__today()

        # check today's snapshot hasn't yet been posted
        if self.__models_snapshot_exists_for_date(date):
            raise Exception("Model snapshot has already been posted for date: " + str(date))

        # get dimensions for the snapshot
        dim_date = self.__create_or_get_date(date)
        dim_training_started_date = self.__create_or_get_date(training_started)
        dim_training_ended_date = self.__create_or_get_date(training_ended)

        # create the snapshot
        snapshot = FactModelsDailySnapshot(
            date=dim_date,
            training_started=dim_training_started_date,
            training_ended=dim_training_ended_date,
            min_accuracy=min_acc,
            max_accuracy=max_acc,
            avg_accuracy=avg_acc,
            min_loss=min_loss,
            max_loss=max_loss,
            avg_loss=avg_loss
        )
        db.session.add(snapshot)
        db.session.commit()

    ### ANALYTICS METHODS ###
    # retrieve a statistical breakdown of the training set size by date
    def get_training_set_size_by_date(self, start_date=None, end_date=None, is_cat=None, colour=None,
        is_tabby=None, pattern=None, is_pointed=None, source=None):
        pass

    # retrieve a statistic breakdown of the training set size by label
    def get_training_set_size_by_label(self, start_date=None, end_date=None, is_cat=None, colour=None,
        is_tabby=None, pattern=None, is_pointed=None, source=None):
        pass

    # retrieve a statistical breakdown of model accuracy and loss by date
    def get_model_performance_by_date(self, start_date=None, end_date=None):
        pass

    # retrieve a statistical breakdown of prediction accuracy over time
    def get_prediction_accuracy_by_date(self, start_date=None, end_date=None, is_cat=None, colour=None,
        is_tabby=None, pattern=None, is_pointed=None, user_review_status=None, admin_review_status=None):
        pass

    # retrieve a statistical breakdown of prediction accuracy by date and review status
    def get_prediction_accuracy_by_date_and_review_status(self, start_date=None, end_date=None, is_cat=None,
        colour=None, is_tabby=None, pattern=None, is_pointed=None):
        pass

    # retrieve a statistical breakdown of prediction acceptance over time
    def get_prediction_acceptance_comparison(self, start_date=None, end_date=None, is_cat=None, colour=None,
        is_tabby=None, pattern=None, is_pointed=None):
        pass

    ### HELPER METHODS ###
    # get a date without the time
    def __today(self):
        return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    def __strip_date(self, date):
        return date.replace(hour=0, minute=0, second=0, microsecond=0)

    # create_or_get methods for each dimension will create a dimensional record if it doesn't exist
    # or otherwise find the matching dimensional record, and in either case return a model object

    # create or get a date
    def __create_or_get_date(self, date):
        # if the date is not none, remove timestamp from it
        if not date is None:
            date = self.__strip_date(date)

        if self.__date_exists_in_dimension(date):
            # if the date exists, retrieve it
            dim_date = DimDate.query.filter_by(date=date).first()
        else:
            #otherwise, create it and then fetch by id
            id = self.__add_date_to_dimension(date)
            dim_date = DimDate.query.filter_by(id=id).first()
        return dim_date

    # create or get a label
    def __create_or_get_label(self, is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed):
        if self.__label_exists_in_dimension(is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed):
            dim_label = DimLabel.query.filter_by(
                is_unlabelled=is_unlabelled,
                is_cat=is_cat,
                colour=colour,
                is_tabby=is_tabby,
                pattern=pattern,
                is_pointed=is_pointed
            ).first()
        else:
            id = self.__add_label_to_dimension(is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed)
            dim_label = DimLabel.query.filter_by(id=id).first()
        return dim_label

    # create or get a review status
    def __create_or_get_prediction_review_status(self, status):
        if self.__prediction_review_status_exists_in_dimension(status):
            dim_status = DimPredictionReviewStatus.query.filter_by(status=status).first()
        else:
            id = self.__add_prediction_review_status_to_dimension(status)
            dim_status = DimPredictionReviewStatus.query.filter_by(id=id).first()
        return dim_status

    # create or get a training image source
    def __create_or_get_training_image_source(self, source):
        if self.__training_image_source_exists_in_dimension(source):
            dim_source = DimTrainingImageSource.query.filter_by(source=source).first()
        else:
            id = self.__add_training_image_source_to_dimension(source)
            dim_source = DimTrainingImageSource.query.filter_by(id=id).first()
        return dim_source

    # list the label filter based on specified filters
    def __list_labels(self, is_unlabelled=None, is_cat=None, colour=None, is_tabby=None, pattern=None, is_pointed=None):
        query = {}

        if not is_unlabelled is None:
            query["is_unlabelled"] = is_unlabelled

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

    # list the date dimension based on specified filters
    def __list_dates(self, start_date=None, end_date=None):
        if start_date is None and end_date is None:
            return DimDate.query.all()
        elif not start_date is None and not end_date is None:
            return DimDate.query.filter(DimDate.date >= start_date, DimDate.date <= end_date).all()
        elif not start_date is None:
            return DimDate.query.filter(DimDate.date >= start_date).all()
        elif not end_date is None:
            return DimDate.query.filter(DimDate.date <= end_date).all()

    # list the review status dimension based on specified filters
    def __list_prediction_review_statuses(self, status=None):
        if status is None:
            return DimPredictionReviewStatus.query.all()
        else:
            return DimPredictionReviewStatus.query.filter_by(status=status).all()

    # list the source dimension based on specified filters
    def __list_training_image_sources(self, source=None):
        if source is None:
            return DimTrainingImageSource.query.all()
        else:
            return DimTrainingImageSource.query.filter_by(source=source).all()

    # add a new date to the dimension
    def __add_date_to_dimension(self, date):
        if self.__date_exists_in_dimension(date):
            raise Exception("Attempted to add duplicate date: " + str(date))

        if date is None:
            day_of_month = None
            month = None
            month_name = None
            year = None
        
        else:

            months = [
                "January", "February", "March", "April", "May", "June", "July", "August",
                "September", "October", "November", "December"
            ]

            day_of_month = date.day
            month = date.month
            month_name = months[date.month - 1]
            year = date.year

        dim_date = DimDate(
            date=date,
            day_of_month=day_of_month,
            month=month,
            month_name=month_name,
            year=year
        )
        db.session.add(dim_date)
        db.session.commit()
        return dim_date.id

    # check if a date exists in the dimension
    def __date_exists_in_dimension(self, date):
        matching_dates = DimDate.query.filter_by(date=date)
        if matching_dates.count() > 1:
            raise Exception("Duplicate date identified: " + repr(matching_dates[0]))

        return matching_dates.count() == 1

    # add a new label to the dimension if it doesn't already exist
    def __add_label_to_dimension(self, is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed):
        if is_unlabelled:
            if not is_cat == False or not colour is None or not is_tabby == False or not pattern is None or not is_pointed == False:
                raise Exception("Label attributes set for unlabelled label")

        label = DimLabel(
            is_unlabelled=is_unlabelled,
            is_cat=is_cat,
            colour=colour,
            is_tabby=is_tabby,
            pattern=pattern,
            is_pointed=is_pointed
        )

        if self.__label_exists_in_dimension(is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed):
            raise Exception("Attempt to add duplicate label: " + repr(label))

        db.session.add(label)
        db.session.commit()

        return label.id

    # check if a specified label exists in the label dimension
    def __label_exists_in_dimension(self, is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed):
        matching_labels = self.__list_labels(is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed)
        if len(matching_labels) > 1:
            raise Exception("Duplicate label identified: " + repr(matching_labels[0]))

        return len(matching_labels) == 1

    # add a prediction review status to the dimension if it doesn't exist
    def __add_prediction_review_status_to_dimension(self, status):
        if self.__prediction_review_status_exists_in_dimension(status):
            raise Exception("Attempt to add duplicate status: " + status)

        dim_status = DimPredictionReviewStatus(status=status)
        db.session.add(dim_status)
        db.session.commit()
        return dim_status.id

    # check if a prediction review status exists
    def __prediction_review_status_exists_in_dimension(self, status):
        matching_statuses = self.__list_prediction_review_statuses(status)
        if len(matching_statuses) > 1:
            raise Exception("Duplicate status identified: " + repr(matching_statuses[0]))

        return len(matching_statuses) == 1

    # add a training image source to the dimension if it doesn't exist
    def __add_training_image_source_to_dimension(self, source):
        if self.__training_image_source_exists_in_dimension(source):
            raise Exception("Attempt to add duplicate training image source: " + source)

        dim_source = DimTrainingImageSource(source=source)
        db.session.add(dim_source)
        db.session.commit()
        return dim_source.id

    # check if a training image source exists in the dimension
    def __training_image_source_exists_in_dimension(self, source):
        matching_sources = self.__list_training_image_sources(source)
        if len(matching_sources) > 1:
            raise Exception("Duplicate source identified: " + repr(matching_sources[0]))
        
        return len(matching_sources) == 1

    # check if a training image snapshot already exists for the given date
    def __training_image_snapshot_exists_for_date(self, date):
        if not self.__date_exists_in_dimension(date):
            return False

        dim_date = DimDate.query.filter_by(date=date).first()
        
        if len(dim_date.training_image_snapshots) > 0:
            return True
        
    # check if a predictions snapshot already exists for the given date
    def __predictions_snapshot_exists_for_date(self, date):
        if not self.__date_exists_in_dimension(date):
            return False

        dim_date = DimDate.query.filter_by(date=date).first()
        
        if len(dim_date.prediction_snapshots) > 0:
            return True

    # check if a model snapshot already exists for the given date
    def __models_snapshot_exists_for_date(self, date):
        if not self.__date_exists_in_dimension(date):
            return False

        dim_date = DimDate.query.filter_by(date=date).first()
        
        if len(dim_date.model_snapshots) > 0:
            return True