import streamlit as st
import json
from datetime import datetime
import sys
import os

# ---------------- DATA ----------------
version_float = 1.1

questions = [
    {"q": "How consistent is your wake-up time on weekdays?",
     "opts": [("Always consistent",0),("Mostly consistent",1),("Sometimes varies",2),("Often varies",3),("Completely irregular",4)]},

    {"q": "How refreshed do you feel upon waking up?",
     "opts": [("Fully refreshed",0),("Mostly refreshed",1),("Neutral",2),("Slightly tired",3),("Very exhausted",4)]},

    {"q": "How often do you delay getting out of bed after waking up?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "Do you follow a planned sequence of morning activities?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How much time do you dedicate to your morning routine?",
     "opts": [("More than 60 minutes",0),("45–60 minutes",1),("30–45 minutes",2),("15–30 minutes",3),("Less than 15 minutes",4)]},

    {"q": "How often do you include physical activity?",
     "opts": [("Daily",0),("Frequently",1),("Occasionally",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you skip breakfast?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How quickly do you check your phone after waking up?",
     "opts": [("After 1+ hour",0),("After 30–60 min",1),("After 15–30 min",2),("Within 15 min",3),("Immediately",4)]},

    {"q": "How much time do you spend on your phone in the morning?",
     "opts": [("None",0),("Less than 15 min",1),("15–30 min",2),("30–60 min",3),("More than 1 hour",4)]},

    {"q": "How prepared do you feel before starting classes?",
     "opts": [("Fully prepared",0),("Mostly prepared",1),("Somewhat prepared",2),("Slightly unprepared",3),("Not prepared at all",4)]},

    {"q": "How often are you late or rushed in the morning?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How well can you concentrate during your first class?",
     "opts": [("Excellent",0),("Good",1),("Average",2),("Poor",3),("Very poor",4)]},

    {"q": "What is your typical mood in the morning?",
     "opts": [("Very positive",0),("Positive",1),("Neutral",2),("Negative",3),("Very negative",4)]},

    {"q": "How motivated do you feel at the start of the day?",
     "opts": [("Highly motivated",0),("Motivated",1),("Neutral",2),("Low motivation",3),("No motivation",4)]},

    {"q": "How often do you feel mentally alert in the morning?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How organized is your morning preparation?",
     "opts": [("Fully organized",0),("Mostly organized",1),("Somewhat organized",2),("Disorganized",3),("Completely chaotic",4)]},

    {"q": "Do you prepare for the next day the night before?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "Do you include calm activities (reading, journaling)?",
     "opts": [("Daily",0),("Frequently",1),("Occasionally",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you feel stressed in the morning?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How balanced does your morning feel overall?",
     "opts": [("Very balanced",0),("Balanced",1),("Neutral",2),("Unbalanced",3),("Very chaotic",4)]},
]

# -------- STATES --------
psych_states = {
    "Excellent Routine — Highly effective start": (0, 15),
    "Good Routine — Minor improvements needed": (16, 30),
    "Moderate Routine — Inconsistent habits": (31, 45),
    "Poor Routine — Affects academic performance": (46, 60),
    "Very Poor Routine — High disruption": (61, 70),
    "Critical Routine — Immediate lifestyle changes needed": (71, 80),
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Student Psychological Survey")
st.title("📝 Student Psychological Survey")
if "started" not in st.session_state:
    st.session_state.started = False

st.info("Please fill out your details and answer all questions honestly.")

# --- User Info ---
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

# --- Start Survey ---
if st.button("Start Survey"):

    # Validate inputs
    errors = []
    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
    if not sid.isdigit():
        errors.append("Student ID must be digits only.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed to answer the questions below.")

        total_score = 0
        answers = []

        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
            score = next(score for label, score in q["opts"] if label == choice)
            total_score += score
            answers.append({
                "question": q["q"],
                "selected_option": choice,
                "score": score
            })

        status = interpret_score(total_score)

        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"**Total Score:** {total_score}")

        # Save results to JSON
        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": status,
            "answers": answers,
            "version": version_float
        }

        json_filename = f"{sid}_result.json"
        save_json(json_filename, record)

        st.success(f"Your results are saved as {json_filename}")
        st.download_button("Download your result JSON", json.dumps(record, indent=2), file_name=json_filename)
