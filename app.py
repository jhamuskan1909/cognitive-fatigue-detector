from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import json
import os
import random
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# ─── Train Models on startup ───
np.random.seed(42)
n = 500
data = {
    "sleep_hours": np.random.uniform(3, 9, n),
    "screen_time": np.random.uniform(1, 12, n),
    "physical_activity": np.random.uniform(0, 2, n),
    "work_study_hours": np.random.uniform(2, 12, n),
    "water_intake": np.random.uniform(1, 4, n),
    "diet_quality": np.random.randint(1, 6, n),
    "sleep_time": np.random.uniform(21, 27, n),
}
df = pd.DataFrame(data)
df["fatigue_score"] = (
    (9 - df["sleep_hours"]) * 5 +
    df["screen_time"] * 2 +
    (2 - df["physical_activity"]) * 5 +
    df["work_study_hours"] * 2 +
    (4 - df["water_intake"]) * 3 +
    (5 - df["diet_quality"]) * 2 +
    (df["sleep_time"] - 23) * 2
).clip(0, 100)

def label_fatigue(score):
    if score < 35: return "Low"
    elif score < 65: return "Medium"
    else: return "High"

df["fatigue_level"] = df["fatigue_score"].apply(label_fatigue)
X = df[["sleep_hours","screen_time","physical_activity","work_study_hours","water_intake","diet_quality","sleep_time"]]
y = df["fatigue_level"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}
for name, model in models.items():
    model.fit(X_train, y_train)

rf_model = models["Random Forest"]
feature_importances = dict(zip(X.columns, (rf_model.feature_importances_ * 100).round(1)))

# ─── Memory ───
MEMORY_FILE = "session_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(entry):
    memory = load_memory()
    memory.append(entry)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# ─── Suggestions ───
def get_suggestions(level, data):
    suggestions = []
    if level == "High":
        suggestions.append("🚨 Your fatigue is HIGH. Please rest immediately.")
        if data["sleep_hours"] < 6:
            suggestions.append("😴 You're sleeping less than 6hrs — aim for 7-8hrs tonight.")
        if data["screen_time"] > 6:
            suggestions.append("📵 Reduce screen time. Take a 20-min no-screen break now.")
        if data["physical_activity"] < 0.5:
            suggestions.append("🚶 Even a 10-min walk can reduce fatigue significantly.")
        if data["water_intake"] < 2:
            suggestions.append("💧 Drink at least 2 more glasses of water today.")
    elif level == "Medium":
        suggestions.append("⚠️ Moderate fatigue detected. Take preventive steps.")
        if data["work_study_hours"] > 8:
            suggestions.append("📚 You've been studying/working too long — take a 15-min break.")
        if data["diet_quality"] < 3:
            suggestions.append("🥗 Improve your diet — eat fruits or a proper meal.")
        suggestions.append("🧘 Try 5 minutes of deep breathing to reset focus.")
    else:
        suggestions.append("✅ Your fatigue is LOW. Great job maintaining your health!")
        suggestions.append("💪 Keep up your current routine — you're doing well.")
    return suggestions

challenges = {
    "High":   ["No screens after 10PM tonight 📵", "Sleep before 11PM 😴", "Drink 3L of water today 💧"],
    "Medium": ["Take a 15-min walk 🚶", "No social media for 2 hours 📱", "Eat one healthy meal today 🥗"],
    "Low":    ["Maintain your sleep schedule ⏰", "Do 20 mins of exercise 🏃", "Read for 30 minutes 📖"]
}

# ─── Routes ───
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    d = request.json
    user_data = {
        "sleep_hours": float(d["sleep_hours"]),
        "screen_time": float(d["screen_time"]),
        "physical_activity": float(d["physical_activity"]),
        "work_study_hours": float(d["work_study_hours"]),
        "water_intake": float(d["water_intake"]),
        "diet_quality": int(d["diet_quality"]),
        "sleep_time": float(d["sleep_time"]),
    }
    input_df = pd.DataFrame([user_data])
    predicted_level = models["KNN"].predict(input_df)[0]
    score = (
        (9 - user_data["sleep_hours"]) * 5 +
        user_data["screen_time"] * 2 +
        (2 - user_data["physical_activity"]) * 5 +
        user_data["work_study_hours"] * 2 +
        (4 - user_data["water_intake"]) * 3 +
        (5 - user_data["diet_quality"]) * 2 +
        (user_data["sleep_time"] - 23) * 2
    )
    score = max(0, min(100, score))

    save_memory({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "level": predicted_level,
        "score": round(score, 1)
    })

    return jsonify({
        "level": predicted_level,
        "score": round(score, 1),
        "suggestions": get_suggestions(predicted_level, user_data),
        "challenge": random.choice(challenges[predicted_level])
    })

@app.route("/api/student", methods=["POST"])
def student():
    d = request.json
    exam_stress = int(d["exam_stress"])
    days_to_exam = int(d["days_to_exam"])
    assignments_pending = int(d["assignments_pending"])
    sleep_hours = float(d["sleep_hours"])
    screen_time = float(d["screen_time"])
    water_intake = float(d["water_intake"])
    diet_quality = int(d["diet_quality"])
    physical_activity = float(d["physical_activity"])
    sleep_time = float(d["sleep_time"])
    study_hours = float(d["study_hours"])

    student_score = (
        exam_stress * 3 +
        ((10 - days_to_exam) * 1.5 if days_to_exam <= 10 else 0) +
        assignments_pending * 2 +
        (9 - sleep_hours) * 5 +
        screen_time * 2 +
        (2 - physical_activity) * 5 +
        (4 - water_intake) * 3 +
        (5 - diet_quality) * 2 +
        (sleep_time - 23) * 2
    )
    student_score = max(0, min(100, student_score))

    user_data = {"sleep_hours": sleep_hours, "screen_time": screen_time,
                 "physical_activity": physical_activity, "work_study_hours": study_hours,
                 "water_intake": water_intake, "diet_quality": diet_quality, "sleep_time": sleep_time}
    predicted_level = models["KNN"].predict(pd.DataFrame([user_data]))[0]

    tips = []
    if exam_stress >= 7:
        tips.append("😰 High exam stress! Try the Pomodoro technique.")
        tips.append("📖 Study in 25-min focused sessions with 5-min breaks.")
    if days_to_exam <= 3 and days_to_exam > 0:
        tips.append(f"⏰ Exam in {days_to_exam} day(s)! Prioritize revision over new topics.")
    if assignments_pending >= 3:
        tips.append(f"📋 {assignments_pending} assignments pending — make a priority list now!")
    if sleep_hours < 6:
        tips.append("😴 Don't sacrifice sleep before exams — memory needs rest!")
    if student_score > 60:
        tips.append("🧘 Take a 10-min break RIGHT NOW before continuing.")

    student_challenges = [
        "Complete 1 pending assignment today 📝",
        "Study using Pomodoro: 25min on, 5min off ⏱️",
        "No phone for first 2 hours of study 📵",
        "Sleep before midnight tonight 🌙",
        "Drink water every hour during study 💧"
    ]

    save_memory({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "level": predicted_level,
        "score": round(student_score, 1),
        "mode": "student"
    })

    return jsonify({
        "level": predicted_level,
        "score": round(student_score, 1),
        "tips": tips,
        "challenge": random.choice(student_challenges)
    })

@app.route("/api/history")
def history():
    memory = load_memory()
    return jsonify(memory)

@app.route("/api/features")
def features():
    return jsonify(feature_importances)

if __name__ == "__main__":
    app.run(debug=True)
    