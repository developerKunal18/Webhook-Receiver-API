from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)

# ---------- Config ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///webhooks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------- Model ----------
class WebhookEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(100))
    payload = db.Column(db.Text)
    created_at = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# ---------- Receive Webhook ----------
@app.route("/webhook", methods=["POST"])
def receive_webhook():

    data = request.get_json()

    event = WebhookEvent(
        event_type=data.get(
            "event_type",
            "unknown"
        ),
        payload=json.dumps(data),
        created_at=str(datetime.now())
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({
        "message": "Webhook received"
    })

# ---------- View Events ----------
@app.route("/events")
def events():

    all_events = WebhookEvent.query.all()

    return jsonify([
        {
            "id": e.id,
            "event_type": e.event_type,
            "payload": e.payload,
            "created_at": e.created_at
        }
        for e in all_events
    ])

# ---------- Event Count ----------
@app.route("/stats")
def stats():

    return jsonify({
        "total_events":
        WebhookEvent.query.count()
    })

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
