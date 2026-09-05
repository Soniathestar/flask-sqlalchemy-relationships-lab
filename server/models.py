from datetime import datetime

from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

# Association table for the many-to-many relationship between Session and Speaker
session_speakers = db.Table(
    "session_speakers",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("session_id", db.Integer, db.ForeignKey("sessions.id"), nullable=False),
    db.Column("speaker_id", db.Integer, db.ForeignKey("speakers.id"), nullable=False),
)


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String)

    # One-to-many: Event has many Sessions; delete sessions when event is deleted
    sessions = db.relationship(
        "Session",
        back_populates="event",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Event {self.id}: {self.name}, {self.location}>"


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    # Many-to-one: Session belongs to Event
    event = db.relationship("Event", back_populates="sessions")

    # Many-to-many: Session has many Speakers through session_speakers
    speakers = db.relationship(
        "Speaker",
        secondary=session_speakers,
        back_populates="sessions",
    )

    def __repr__(self):
        return f"<Session {self.id}: {self.title}, {self.start_time}>"


class Speaker(db.Model):
    __tablename__ = "speakers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # One-to-one: Speaker has one Bio; delete bio when speaker is deleted
    bio = db.relationship(
        "Bio",
        back_populates="speaker",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # Many-to-many: Speaker has many Sessions through session_speakers
    sessions = db.relationship(
        "Session",
        secondary=session_speakers,
        back_populates="speakers",
    )

    def __repr__(self):
        return f"<Speaker {self.id}: {self.name}>"


class Bio(db.Model):
    __tablename__ = "bios"

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.String)
    speaker_id = db.Column(db.Integer, db.ForeignKey("speakers.id"), nullable=False, unique=True)

    # One-to-one: Bio belongs to Speaker
    speaker = db.relationship("Speaker", back_populates="bio")

    def __repr__(self):
        return f"<Bio {self.id}: for Speaker {self.speaker_id}>"
