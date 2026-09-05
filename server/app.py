from flask import Flask, jsonify
from models import db, Event, Session, Speaker, Bio
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "app.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# ---------- Event Endpoints ----------

@app.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    return jsonify([
        {"id": e.id, "name": e.name, "location": e.location}
        for e in events
    ]), 200


@app.route("/events/<int:id>/sessions", methods=["GET"])
def get_event_sessions(id):
    event = Event.query.filter_by(id=id).first()
    if not event:
        return jsonify({"error": "Event not found"}), 404

    sessions = [
        {
            "id": s.id,
            "title": s.title,
            "start_time": s.start_time.isoformat(),
        }
        for s in event.sessions
    ]
    return jsonify(sessions), 200


# ---------- Speaker Endpoints ----------

@app.route("/speakers", methods=["GET"])
def get_speakers():
    speakers = Speaker.query.all()
    return jsonify([
        {"id": sp.id, "name": sp.name}
        for sp in speakers
    ]), 200


@app.route("/speakers/<int:id>", methods=["GET"])
def get_speaker(id):
    speaker = Speaker.query.filter_by(id=id).first()
    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404

    bio_text = speaker.bio.bio_text if speaker.bio else "No bio available"
    return jsonify({
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": bio_text,
    }), 200


# ---------- Session Endpoints ----------

@app.route("/sessions/<int:id>/speakers", methods=["GET"])
def get_session_speakers(id):
    session = Session.query.filter_by(id=id).first()
    if not session:
        return jsonify({"error": "Session not found"}), 404

    speakers = [
        {
            "id": sp.id,
            "name": sp.name,
            "bio_text": sp.bio.bio_text if sp.bio else "No bio available",
        }
        for sp in session.speakers
    ]
    return jsonify(speakers), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
