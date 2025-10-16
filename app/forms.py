from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, NumberRange

# ---------------- LOST & FOUND ----------------
class LostFoundForm(FlaskForm):
    item_name = StringField("Item Name", validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=5, max=300)])
    location = StringField("Location", validators=[DataRequired(), Length(min=2, max=100)])
    status = SelectField("Status", choices=[("Lost", "Lost"), ("Found", "Found")], validators=[DataRequired()])
    contact_info = StringField("Contact Info", validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField("Submit")

# ---------------- MENTAL HEALTH ----------------
class MentalHealthForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    mood = SelectField("Mood", choices=[
        ("Happy", "😊 Happy"),
        ("Neutral", "😐 Neutral"),
        ("Sad", "😢 Sad"),
        ("Stressed", "😫 Stressed"),
        ("Angry", "😠 Angry")
    ], validators=[DataRequired()])
    stress_level = SelectField("Stress Level", choices=[
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High")
    ], validators=[DataRequired()])
    message = TextAreaField("Message", validators=[Length(max=300)])
    submit = SubmitField("Submit")

# ---------------- QUEUE SYSTEM ----------------
class QueueUpdateForm(FlaskForm):
    location = SelectField("Location", choices=[
        ("Library", "Library"),
        ("Canteen", "Canteen"),
        ("Stationery Shop", "Stationery Shop"),
        ("Admin Office", "Admin Office")
    ], validators=[DataRequired()])
    wait_time = IntegerField("Estimated Wait Time (in minutes)", validators=[DataRequired(), NumberRange(min=0, max=300)])
    submit = SubmitField("Update Queue")

# ---------------- CLUB EVENTS ----------------
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length

class EventForm(FlaskForm):
    club = SelectField(
        "Select Club",
        choices=[
            ("eesa", "EESA (Electronics Students' Association)"),
            ("etsa", "ETSA (Electronics & Telecommunications Students' Association)"),
            ("itsa", "ITSA (Information Technology Students' Association)"),
            ("bmsa", "BMSA (Bio-Medical Students' Association)"),
            ("cesa", "CESA (Computer Education Students' Association)"),
            ("csi", "Computer Society of India (CSI) - VIT Mumbai Chapter)"),
            ("ieee", "IEEE VIT Student Branch"),
            ("gdsc", "Google Developer Student Clubs (GDSC) VIT, Mumbai)"),
            ("hobby", "Hobby Club Committee"),
            ("nss", "National Service Scheme (NSS)"),
            ("pec", "Personality Enrichment Committee"),
            ("vidyalankar_volunteer", "Vidyalankar Volunteer Committee")
        ],
        validators=[DataRequired()]
    )
    title = StringField("Event Title", validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField("Event Description", validators=[DataRequired(), Length(min=5, max=300)])
    location = StringField("Event Location", validators=[DataRequired(), Length(min=2, max=100)])
    date = DateField("Event Date", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("Add Event")