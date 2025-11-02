from models import db

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)

    categories = db.relationship("CategoryModel", back_populates="user", cascade="all, delete-orphan")
    records = db.relationship("RecordModel", back_populates="user", cascade="all, delete-orphan")
