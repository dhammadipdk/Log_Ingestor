# backend/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    resourceId = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    traceId = db.Column(db.String(50), nullable=True)
    spanId = db.Column(db.String(50), nullable=True)
    commit = db.Column(db.String(50), nullable=True)
    parentResourceId = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'message': self.message,
            'resourceId': self.resourceId,
            'timestamp': self.timestamp.isoformat(),
            'traceId': self.traceId,
            'spanId': self.spanId,
            'commit': self.commit,
            'parentResourceId': self.parentResourceId
        }
