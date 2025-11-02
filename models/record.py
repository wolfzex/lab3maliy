from models import db

class RecordModel(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel", back_populates="records")
