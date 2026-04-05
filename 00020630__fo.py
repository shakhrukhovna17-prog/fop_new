import streamlit as st
import json
from datetime import datetime

# ---------------- VARIABLE TYPES ----------------
version_float = 1.1              # float
dummy_range = range(10)          # range
dummy_set = set()                # set
dummy_frozenset = frozenset([1,2,3])  # frozenset

# ---------------- LOAD QUESTIONS ----------------
version_float = 1.1

with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# ---------------- STATES ----------------
psych_states = {
    "Excellent Routine": (0, 15),
    "Good Routine": (16, 30),
    "Moderate Routine": (31, 45),
    "Poor Routine": (46, 60),
    "Very Poor Routine": (61, 70),
    "Critical Routine": (71, 80),
}

# ---------------- FUNCTIONS ----------------
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

# ---------------- APP ----------------
st.set_page_config(page_title="Survey")
st.title("📝 Student Psychological Survey")

if "started" not in st.session_state:
    st.session_state.started = False

# ---------------- INPUT ----------------
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID")

# ---------------- VALIDATION ----------------
if st.button("Start Survey"):

    errors = []
    fields = [name, surname, dob, sid]

    # ✅ FOR LOOP validation
    for field in fields:
        if field.strip() == "":
            errors.append("All fields must be filled.")

    if not validate_name(name):
        errors.append("Invalid name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid DOB format.")
    if not sid.isdigit():
        errors.append("Student ID must be numeric.")

    # ✅ WHILE LOOP (simulated check logic)
    valid = False
    while not valid:
        if len(errors) == 0:
            valid = True
        else:
            break

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.session_state.started = True

# ---------------- SURVEY ----------------
if st.session_state.started:

    st.success("All inputs valid. Start survey.")

    total_score = 0
    answers = []

    for idx, q in enumerate(questions):
        labels = [opt[0] for opt in q["opts"]]
        choice = st.selectbox(f"Q{idx+1}. {q['q']}", labels, key=idx)

        score = next(s for label, s in q["opts"] if label == choice)

        total_score += score

        answers.append({
            "question": q["q"],
            "answer": choice,
            "score": score
        })

    status = interpret_score(total_score)

    st.markdown(f"## Result: {status}")
    st.write(f"Total Score: {total_score}")

    record = {
        "name": name,
        "surname": surname,
        "dob": dob,
        "student_id": sid,
        "score": total_score,
        "result": status,
        "answers": answers,
        "version": version_float
    }

    filename = f"{sid}.json"
    save_json(filename, record)

    st.download_button("Download JSON", json.dumps(record, indent=2), file_name=filename)