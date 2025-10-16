from flask import render_template, redirect, url_for, flash, request, jsonify
from app import app, csrf, db_ref
from app.forms import LostFoundForm, MentalHealthForm, QueueUpdateForm, EventForm
from openai import OpenAI
import datetime
import os
from dotenv import load_dotenv

# -------------------- Load OpenAI --------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env")
client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------- INDEX --------------------
@app.route("/")
def index():
    return render_template("index.html")

# -------------------- LOST & FOUND --------------------
@app.route("/lost_found", methods=["GET", "POST"])
def lostfound():
    form = LostFoundForm()
    if form.validate_on_submit():
        item = {
            "name": form.item_name.data,
            "description": form.description.data,
            "location": form.location.data,
            "status": form.status.data,
            "reporter": form.contact_info.data,
            "timestamp": datetime.datetime.now().isoformat()
        }
        db_ref.child("lost_found").push(item)
        flash("Item successfully submitted!", "success")
        return redirect(url_for("lostfound"))

    lost_items = db_ref.child("lost_found").get() or {}
    return render_template("lost_found.html", form=form, lost_items=lost_items)

@app.route('/delete_item/<string:item_id>', methods=['POST'])
@csrf.exempt
def delete_item(item_id):
    try:
        db_ref.child("lost_found").child(item_id).delete()
        flash("Item marked as found and removed successfully!", "success")
    except Exception as e:
        flash(f"Error removing item: {e}", "danger")
    return redirect(url_for('lostfound'))

# -------------------- MENTAL HEALTH --------------------
@app.route("/mental_health", methods=["GET", "POST"])
def mental_health():
    form = MentalHealthForm()
    tips = [
        {"title": "Take a Break", "content": "Step away for 5 minutes to relax."},
        {"title": "Stay Hydrated", "content": "Drink water regularly."},
        {"title": "Talk to Someone", "content": "Share how you feel with a friend."},
    ]
    if form.validate_on_submit():
        entry = {
            "name": form.name.data,
            "email": form.email.data,
            "mood": form.mood.data,
            "stress_level": form.stress_level.data,
            "message": form.message.data,
            "timestamp": datetime.datetime.now().isoformat()
        }
        db_ref.child("mental_health").push(entry)
        flash("Thank you for sharing. Your entry has been saved.", "success")
        return redirect(url_for("mental_health"))

    return render_template("mental_health.html", form=form, tips=tips)

# -------------------- QUEUE SYSTEM --------------------
@app.route("/queue_status", methods=["GET", "POST"])
def queue_status():
    form = QueueUpdateForm()
    queue_data = {}

    if form.validate_on_submit():
        location = form.location.data
        wait_time = form.wait_time.data
        timestamp = datetime.datetime.now().isoformat()

        db_ref.child("queue_status").child(location).set({
            "location": location,
            "wait_time": wait_time,
            "timestamp": timestamp
        })
        flash(f"Queue updated for {location}!", "success")
        return redirect(url_for("queue_status"))

    # Fetch queue data
    data = db_ref.child("queue_status").get() or {}
    now = datetime.datetime.now()

    # Filter out expired queues
    for key, value in list(data.items()):
        try:
            entry_time = datetime.datetime.fromisoformat(value["timestamp"])
            expiry_time = entry_time + datetime.timedelta(minutes=int(value["wait_time"]))
            if now > expiry_time:
                # Delete expired entry
                db_ref.child("queue_status").child(key).delete()
            else:
                queue_data[key] = value
        except Exception as e:
            print(f"Error checking expiry for {key}: {e}")

    return render_template("queue_status.html", form=form, queue_data=queue_data)


# -------------------- CLUBS & EVENTS --------------------
# -------------------- CLUBS & EVENTS --------------------
@app.route("/clubs", methods=["GET", "POST"])
def clubs():
    form = EventForm()

    # Hardcoded club list
    clubs_list = {
        "eesa": "EESA (Electronics Students' Association)",
        "etsa": "ETSA (Electronics & Telecommunications Students' Association)",
        "itsa": "ITSA (Information Technology Students' Association)",
        "bmsa": "BMSA (Bio-Medical Students' Association)",
        "cesa": "CESA (Computer Education Students' Association)",
        "csi": "Computer Society of India (CSI) - VIT Mumbai Chapter",
        "ieee": "IEEE VIT Student Branch",
        "gdsc": "Google Developer Student Clubs (GDSC) VIT, Mumbai)",
        "hobby": "Hobby Club Committee",
        "nss": "National Service Scheme (NSS)",
        "pec": "Personality Enrichment Committee",
        "vidyalankar_volunteer": "Vidyalankar Volunteer Committee"
    }

    # Populate dropdown choices
    form.club.choices = [(club_id, name) for club_id, name in clubs_list.items()]

    # Handle form submission
    if form.validate_on_submit():
        event = {
            "title": form.title.data,
            "description": form.description.data,
            "location": form.location.data,
            "date": form.date.data.isoformat(),
            "timestamp": datetime.datetime.now().isoformat()
        }
        db_ref.child("clubs").child(form.club.data).child("events").push(event)
        flash("Event added successfully!", "success")
        return redirect(url_for("clubs"))

    # Fetch events and remove past events
    all_events = {}
    today = datetime.date.today()

    for club_id, club_name in clubs_list.items():
        events = db_ref.child("clubs").child(club_id).child("events").get() or {}
        upcoming_events = {}
        for event_id, event in list(events.items()):
            event_date = datetime.date.fromisoformat(event["date"])
            if event_date >= today:
                upcoming_events[event_id] = event
            else:
                # Delete past event
                db_ref.child("clubs").child(club_id).child("events").child(event_id).delete()
        all_events[club_name] = upcoming_events  # even if empty, keep the club

    return render_template("clubs.html", form=form, clubs=all_events)
# -------------------- CHATBOT --------------------
@app.route("/chatbot_reply", methods=["POST"])
@csrf.exempt
def chatbot_reply():
    try:
        user_msg = request.json.get("message", "")
        if not user_msg:
            return jsonify({"reply": "Please enter a message."})

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a kind and empathetic mental health support assistant. Give short, caring, and comforting responses."},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=150,
            temperature=0.8
        )

        reply = completion.choices[0].message.content.strip()

    except Exception as e:
        reply = f"Sorry, something went wrong! ({e})"

    return jsonify({"reply": reply})
