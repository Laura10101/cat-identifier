from datetime import datetime
from multiprocessing import synchronize
from .models import *
from .database import db

class AnalyticsService:
    def __init__(self, config):
        self.__config = config

    # check whether snapshot has been posted today
    def snapshot_posted_today(self):
        date = self.__today()
        images_snapshot_created = self.__training_image_snapshot_exists_for_date(date)
        predictions_snapshot_created = self.__predictions_snapshot_exists_for_date(date)
        models_snapshot_created = self.__models_snapshot_exists_for_date(date)
        return images_snapshot_created or predictions_snapshot_created or models_snapshot_created

    ### DELETE METHODS FOR SNAPSHOTS ###
    def clear_training_images_snapshots(self):
        FactTrainingImagesDailySnapshot.query.delete()
        db.session.commit()

    def clear_predictions_snapshots(self):
        FactPredictionsDailySnapshot.query.delete()
        db.session.commit()

    def clear_models_snapshots(self):
        FactModelsDailySnapshot.query.delete()
        db.session.commit()

    ### CREATION METHODS FOR SNAPSHOTS ###
    def create_training_images_snapshot(self, snapshot):

        # get date dimension for the new snapshots
        date = self.__today()

        # check today's snapshot hasn't yet been posted
        if self.__training_image_snapshot_exists_for_date(date):
            raise Exception("Training images snapshot has already been posted for date: " + str(date))
        dim_date = self.__create_or_get_date(date)

        # create a snapshot record for each summary
        for summary in snapshot: 
            is_unlabelled = summary["is_unlabelled"]
            is_cat = summary["is_cat"]
            colour = summary["colour"]
            is_tabby = summary["is_tabby"]
            pattern = summary["pattern"]
            is_pointed = summary["is_pointed"]
            source = summary["source"]
            count = summary["count"]

            # get the dimensions for the snapshot
            dim_label = self.__create_or_get_label(is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed)
            dim_source = self.__create_or_get_training_image_source(source)

            # add the snapshot
            fact_training_images = FactTrainingImagesDailySnapshot(
                date = dim_date,
                label = dim_label,
                source = dim_source,
                count=count
            )
            db.session.add(fact_training_images)
        db.session.commit()

    def create_predictions_snapshot(self, snapshot):
        # get the timestamp for the snapshot
        date = self.__today()

        # check today's snapshot hasn't yet been posted
        if self.__predictions_snapshot_exists_for_date(date):
            raise Exception("Prediction snapshot has already been posted for date: " + str(date))

        dim_date = self.__create_or_get_date(date)

        for summary in snapshot:
            is_unlabelled = summary["is_unlabelled"]
            is_cat = summary["is_cat"]
            colour = summary["colour"]
            is_tabby = summary["is_tabby"]
            pattern = summary["pattern"]
            is_pointed = summary["is_pointed"]
            user_review_status = summary["user_review_status"]
            admin_review_status = summary["admin_review_status"]
            count = summary["count"]

            # get the dimensions for the snapshot
            dim_label = self.__create_or_get_label(is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed)
            dim_user_review_status = self.__create_or_get_prediction_review_status(user_review_status)
            dim_admin_review_status = self.__create_or_get_prediction_review_status(admin_review_status)

            # add the snapshot
            fact_predictions = FactPredictionsDailySnapshot(
                date=dim_date,
                label=dim_label,
                user_review_status=dim_user_review_status,
                admin_review_status=dim_admin_review_status,
                count=count
            )
            db.session.add(fact_predictions)
        db.session.commit()

    def create_models_snapshot(self, snapshot):
        # get timestamp for the snapshot
        date = self.__today()

        # check today's snapshot hasn't yet been posted
        if self.__models_snapshot_exists_for_date(date):
            raise Exception("Model snapshot has already been posted for date: " + str(date))

        dim_date = self.__create_or_get_date(date)

        for summary in snapshot:
            training_started = summary["training_started"]
            training_ended = summary["training_ended"]
            min_acc = summary["min_accuracy"]
            max_acc = summary["max_accuracy"]
            avg_acc = summary["avg_accuracy"]
            min_loss = summary["min_loss"]
            max_loss = summary["max_loss"]
            avg_loss = summary["avg_loss"]
            # get dimensions for the snapshot
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
    # retrieve a statistical breakdown of the training sets by date, label, and source
    def get_training_set_stats(self, start_date=None, end_date=None, is_unlabelled=None, is_cat=None,
    colour=None, is_tabby=None, pattern=None, is_pointed=None, source=None):

        # get all date ids in the given range
        dim_dates = self.__list_dates(start_date, end_date)
        date_ids = [d.id for d in dim_dates]

        # get all the label ids matching the specified criteria
        dim_labels = self.__list_labels(is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed)
        label_ids = [l.id for l in dim_labels]

        # get all the source ids matching the specified criteria
        dim_sources = self.__list_training_image_sources(source)
        source_ids = [s.id for s in dim_sources]

        # if any of the dimension filters returns an empty list
        # then no dimensional value can be found to match the filters
        # so no matching fact can exist. an empty dataset should be returned.
        if len(date_ids) == 0 or len(label_ids) == 0 or len(source_ids) == 0:
            return []

        # get the fact records
        facts = FactTrainingImagesDailySnapshot.query.filter(
            FactTrainingImagesDailySnapshot.date_id.in_(date_ids),
            FactTrainingImagesDailySnapshot.label_id.in_(label_ids),
            FactTrainingImagesDailySnapshot.source_id.in_(source_ids)
        ).all()

        # flatten the facts into a tabular structure
        results = []
        for fact in facts:
            results.append({
                "date": fact.date.date,
                "label_id": fact.label_id,
                "is_unlabelled": fact.label.is_unlabelled,
                "is_cat": fact.label.is_cat,
                "colour": fact.label.colour,
                "is_tabby": fact.label.is_tabby,
                "pattern": fact.label.pattern,
                "is_pointed": fact.label.is_pointed,
                "source": fact.source.source,
                "count": fact.count
            })

        return results

    # retrieve a statistical breakdown of model accuracy and loss by date, training start date
    # and training end date
    def get_model_stats(self, start_date=None, end_date=None, training_started_after=None,
        training_started_before=None, training_ended_after=None, training_ended_before=None):

        # get date ids for the snapshot, training start, and training ended date ranges
        dim_snapshot_dates = self.__list_dates(start_date, end_date)
        snapshot_date_ids = [d.id for d in dim_snapshot_dates]

        dim_training_started_dates = self.__list_dates(training_started_after, training_started_before)
        training_started_date_ids = [d.id for d in dim_training_started_dates]

        dim_training_ended_dates = self.__list_dates(training_ended_after, training_ended_before)
        training_ended_date_ids = [d.id for d in dim_training_ended_dates]

        # check to ensure that all dimensions contain ids
        if len(snapshot_date_ids) == 0 or len(training_started_date_ids) == 0 or len(training_ended_date_ids) == 0:
            return []

        # retrieve fact records based on given filters
        facts = FactModelsDailySnapshot.query.filter(
            FactModelsDailySnapshot.date_id.in_(snapshot_date_ids),
            FactModelsDailySnapshot.training_started_date_id.in_(training_started_date_ids),
            FactModelsDailySnapshot.training_ended_date_id.in_(training_ended_date_ids)
        ).all()

        # flatten the facts into a tabular structure
        results = []
        for fact in facts:
            results.append({
                "snapshot_date": fact.date.date,
                "training_started": fact.training_started.date,
                "training_ended": fact.training_ended.date,
                "min_accuracy": fact.min_accuracy,
                "max_accuracy": fact.max_accuracy,
                "avg_accuracy": fact.avg_accuracy,
                "min_loss": fact.min_loss,
                "max_loss": fact.max_loss,
                "avg_loss": fact.avg_loss
            })

        return results

    # retrieve a statistical breakdown of predictions over time
    def get_prediction_stats(self, start_date=None, end_date=None, is_unlabelled=None, is_cat=None, colour=None,
        is_tabby=None, pattern=None, is_pointed=None, user_review_status=None, admin_review_status=None):

        # get all date ids in the given range
        dim_dates = self.__list_dates(start_date, end_date)
        date_ids = [d.id for d in dim_dates]

        # get all the label ids matching the specified criteria
        dim_labels = self.__list_labels(is_unlabelled, is_cat, colour, is_tabby, pattern, is_pointed)
        label_ids = [l.id for l in dim_labels]

        # get all review statuses matching specified user review status
        dim_user_review_status = self.__list_prediction_review_statuses(user_review_status)
        user_review_status_ids = [s.id for s in dim_user_review_status]

        # get all review statuses matching specified admin review status
        dim_admin_review_status = self.__list_prediction_review_statuses(admin_review_status)
        admin_review_status_ids = [s.id for s in dim_admin_review_status]

        # check no filtered dimensions are empty
        if len(date_ids) == 0 or len(label_ids) == 0:
            return []
        elif len(user_review_status_ids) == 0 or len(admin_review_status_ids) == 0:
            return []

        # retrieve the filtered list of facts
        facts = FactPredictionsDailySnapshot.query.filter(
            FactPredictionsDailySnapshot.date_id.in_(date_ids),
            FactPredictionsDailySnapshot.label_id.in_(label_ids),
            FactPredictionsDailySnapshot.user_review_status_id.in_(user_review_status_ids),
            FactPredictionsDailySnapshot.admin_review_status_id.in_(admin_review_status_ids)
        ).all()

        # flatten into a set of records
        results = []
        for fact in facts:
            results.append({
                "date": fact.date.date,
                "label_id": fact.label_id,
                "is_unlabelled": fact.label.is_unlabelled,
                "is_cat": fact.label.is_cat,
                "colour": fact.label.colour,
                "is_tabby": fact.label.is_tabby,
                "pattern": fact.label.pattern,
                "is_pointed": fact.label.is_pointed,
                "user_review_status": fact.user_review_status.status,
                "admin_review_status": fact.admin_review_status.status,
                "count": fact.count
            })

        return results


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
