from .database import db

#dimension models
class DimDate(db.Model):
    #schema for the date dimension model
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    day_of_month = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    month_name = db.Column(db.String(25), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    #relationships
    prediction_snapshots = db.relationship(
            "FactPredictionsDailySnapshot",
            backref="date",
            cascade="all, delete",
            lazy=True
        )

    training_image_snapshots = db.relationship(
            "FactTrainingImagesDailySnapshot",
            backref="date",
            cascade="all, delete",
            lazy=True
        )

    model_snapshots = db.relationship(
            "FactModelsDailySnapshot",
            backref="date",
            foreign_keys="FactModelsDailySnapshot.date_id",
            cascade="all, delete",
            lazy=True
        )

    model_started_training_snapshots = db.relationship(
            "FactModelsDailySnapshot",
            backref="training_started",
            foreign_keys="FactModelsDailySnapshot.training_started_date_id",
            cascade="all, delete",
            lazy=True
        )

    model_ended_training_snapshots = db.relationship(
            "FactModelsDailySnapshot",
            backref="training_ended",
            foreign_keys="FactModelsDailySnapshot.training_ended_date_id",
            cascade="all, delete",
            lazy=True
        )

    def __repr__(self):
        return "{} {} {}".format(self.day_of_month, self.month_name, self.year)

class DimLabel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_unlabelled = db.Column(db.Boolean)
    is_cat = db.Column(db.Boolean)
    colour = db.Column(db.String(25))
    is_tabby = db.Column(db.Boolean)
    pattern = db.Column(db.String(25))
    is_pointed = db.Column(db.Boolean)

    #relationships for the dim label model
    prediction_snapshots = db.relationship(
            "FactPredictionsDailySnapshot",
            backref="label",
            cascade="all, delete",
            lazy=True
        )

    training_image_snapshots = db.relationship(
            "FactTrainingImagesDailySnapshot",
            backref="label",
            cascade="all, delete",
            lazy=True
        )

    def __repr__(self):
        if self.is_unlabelled:
            return "Unlabelled"

        if not self.is_cat:
            return "Not a cat"

        label = self.colour

        if self.is_tabby:
            label += " tabby"

        if not self.pattern.lower() == "self":
            label += " " + self.pattern.lower()

        if self.is_pointed:
            label += " point"
        
        return label

class DimPredictionReviewStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(25), unique=True, nullable=False)

    user_reviewed_prediction_snapshots = db.relationship(
            "FactPredictionsDailySnapshot",
            backref="user_review_status",
            foreign_keys="FactPredictionsDailySnapshot.user_review_status_id",
            cascade="all, delete",
            lazy=True
        )

    admin_reviewed_prediction_snapshots = db.relationship(
            "FactPredictionsDailySnapshot",
            backref="admin_review_status",
            foreign_keys="FactPredictionsDailySnapshot.admin_review_status_id",
            cascade="all, delete",
            lazy=True
        )

    def __repr__(self):
        return self.status

class DimTrainingImageSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(25), unique=True, nullable=False)

    training_image_snapshots = db.relationship(
            "FactTrainingImagesDailySnapshot",
            backref="source",
            cascade="all, delete",
            lazy=True
        )

    def __repr__(self):
        return self.source

#fact models
class FactPredictionsDailySnapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_id = db.Column(db.Integer, db.ForeignKey("dim_date.id", ondelete="CASCADE"), nullable=False)
    label_id = db.Column(db.Integer, db.ForeignKey("dim_label.id", ondelete="CASCADE"), nullable=False)
    user_review_status_id = db.Column(
            db.Integer,
            db.ForeignKey("dim_prediction_review_status.id", ondelete="CASCADE"),
            nullable=False
        )
    admin_review_status_id = db.Column(
            db.Integer,
            db.ForeignKey("dim_prediction_review_status.id", ondelete="CASCADE"),
            nullable=False
        )
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        summary = "Predictions snapshot taken on {} ".format(repr(self.date))
        summary += "for predictions with outcome ['{}'], ".format(repr(self.label))
        summary += "user review status of {} and ".format(repr(self.user_review_status))
        summary += "admin review status of {}".format(repr(self.admin_review_status))
        return summary

class FactTrainingImagesDailySnapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_id = db.Column(db.Integer, db.ForeignKey("dim_date.id", ondelete="CASCADE"), nullable=False)
    label_id = db.Column(db.Integer, db.ForeignKey("dim_label.id", ondelete="CASCADE"), nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey("dim_training_image_source.id", ondelete="CASCADE"), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        summary = "Training images snapshot taken on {} ".format(repr(self.date))
        summary += "for training images with label ['{}'], ".format(repr(self.label))
        summary += "and source of {}".format(repr(self.source))
        return summary

class FactModelsDailySnapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_id = db.Column(db.Integer, db.ForeignKey("dim_date.id", ondelete="CASCADE"), nullable=False)
    training_started_date_id = db.Column(db.Integer, db.ForeignKey("dim_date.id", ondelete="CASCADE"), nullable=False)
    training_ended_date_id = db.Column(db.Integer, db.ForeignKey("dim_date.id", ondelete="CASCADE"), nullable=False)
    min_accuracy = db.Column(db.Float, nullable=False)
    max_accuracy = db.Column(db.Float, nullable=False)
    avg_accuracy = db.Column(db.Float, nullable=False)
    min_loss = db.Column(db.Float, nullable=False)
    max_loss = db.Column(db.Float, nullable=False)
    avg_loss = db.Column(db.Float, nullable=False)

    def __repr__(self):
        summary = "Prediction models snapshot for models with "
        summary += "a training start date of {} ".format(repr(self.training_started))
        summary += "and a training end date of {}".format(repr(self.training_ended))
        return summary