from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class Blacklist(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    app_uuid = db.Column(db.String(50))
    blocked_reason = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    user_ip = db.Column(db.String(50))


class BlacklistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
        include_relationships = True
        load_instance = True
