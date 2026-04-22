import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    if score < 35:
        return "Low"
    elif score < 65:
        return "Medium"
    else:
        return "High"

df["fatigue_level"] = df["fatigue_score"].apply(label_fatigue)

print(df.head())
print("\nFatigue Level Distribution:")
print(df["fatigue_level"].value_counts())

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Features and target
X = df[["sleep_hours", "screen_time", "physical_activity",
        "work_study_hours", "water_intake", "diet_quality", "sleep_time"]]
y = df["fatigue_level"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Train all 3 models
models = {
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}

print("\n===== Model Comparison =====")
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"{name}: {acc*100:.2f}% accuracy")

    import matplotlib.pyplot as plt

# Feature Importance from Random Forest
rf_model = models["Random Forest"]
features = X.columns
importances = rf_model.feature_importances_

# Sort by importance
indices = np.argsort(importances)[::-1]

print("\n===== Feature Importance =====")
for i in range(len(features)):
    print(f"{features[indices[i]]}: {importances[indices[i]]*100:.1f}%")

print("\n✅ Feature Importance done! Moving to Wellness Bot...")

import json
import os
import random
from datetime import datetime

# ─── Session Memory ───
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

# ─── Rule-Based Suggestions ───
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

# ─── Daily Challenges ───
challenges = {
    "High":   ["No screens after 10PM tonight 📵",
               "Sleep before 11PM 😴",
               "Drink 3L of water today 💧"],
    "Medium": ["Take a 15-min walk 🚶",
               "No social media for 2 hours 📱",
               "Eat one healthy meal today 🥗"],
    "Low":    ["Maintain your sleep schedule ⏰",
               "Do 20 mins of exercise 🏃",
               "Read for 30 minutes 📖"]
}

# ─── Main Bot ───
def wellness_bot():
    print("\n" + "="*45)
    print("   🤖 COGNITIVE FATIGUE WELLNESS BOT")
    print("="*45)

    # Check past sessions
    memory = load_memory()
    if memory:
        print(f"\n📋 You have {len(memory)} previous session(s).")
        last = memory[-1]
        print(f"   Last session: {last['date']} → Fatigue was {last['level']}")
        if len(memory) >= 3:
            recent = [m["level"] for m in memory[-3:]]
            if recent.count("High") >= 2:
                print("   ⚠️  Warning: High fatigue detected 2+ times recently!")

    print("\n📝 Enter your lifestyle details:\n")

    user_data = {
        "sleep_hours":       float(input("  Sleep hours last night (e.g. 6.5): ")),
        "screen_time":       float(input("  Screen time today in hours (e.g. 5): ")),
        "physical_activity": float(input("  Physical activity in hours (e.g. 0.5): ")),
        "work_study_hours":  float(input("  Work/Study hours today (e.g. 8): ")),
        "water_intake":      float(input("  Water intake in litres (e.g. 2): ")),
        "diet_quality":      int(input(  "  Diet quality 1-5 (5=best): ")),
        "sleep_time":        float(input("  What time did you sleep? (e.g. 23=11PM, 25=1AM): "))
    }

    # Predict using best model (KNN)
    knn = models["KNN"]
    input_df = pd.DataFrame([user_data])
    predicted_level = knn.predict(input_df)[0]

    # Fatigue score
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

    print(f"\n{'='*45}")
    print(f"  🧠 Fatigue Level  : {predicted_level}")
    print(f"  📊 Fatigue Score  : {score:.1f}/100")
    print(f"{'='*45}")

    print("\n💡 Personalized Suggestions:")
    for s in get_suggestions(predicted_level, user_data):
        print(f"   {s}")

    print(f"\n🎯 Today's Challenge:")
    print(f"   → {random.choice(challenges[predicted_level])}")

    # Save session
    save_memory({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "level": predicted_level,
        "score": round(score, 1)
    })
    print("\n✅ Session saved to memory!")
    print("="*45)

# ─── Student Mode ───
def student_mode():
    print("\n" + "="*45)
    print("   🎓 STUDENT MODE ACTIVATED")
    print("="*45)

    print("\n📝 Enter your student-specific details:\n")

    exam_stress = int(input("  Exam stress level 1-10 (10=highest): "))
    days_to_exam = int(input("  Days until next exam (0 if no exam): "))
    assignments_pending = int(input("  Number of pending assignments: "))
    study_hours = float(input("  Hours studied today: "))
    sleep_hours = float(input("  Sleep hours last night: "))
    screen_time = float(input("  Screen time in hours: "))
    water_intake = float(input("  Water intake in litres: "))
    diet_quality = int(input("  Diet quality 1-5 (5=best): "))
    physical_activity = float(input("  Physical activity in hours: "))
    sleep_time = float(input("  Sleep time (23=11PM, 25=1AM): "))

    # Calculate student fatigue score
    student_score = (
        exam_stress * 3 +
        (10 - days_to_exam) * 1.5 if days_to_exam <= 10 else 0 +
        assignments_pending * 2 +
        (9 - sleep_hours) * 5 +
        screen_time * 2 +
        (2 - physical_activity) * 5 +
        (4 - water_intake) * 3 +
        (5 - diet_quality) * 2 +
        (sleep_time - 23) * 2
    )
    student_score = max(0, min(100, student_score))

    # Predict using KNN
    user_data = {
        "sleep_hours": sleep_hours,
        "screen_time": screen_time,
        "physical_activity": physical_activity,
        "work_study_hours": study_hours,
        "water_intake": water_intake,
        "diet_quality": diet_quality,
        "sleep_time": sleep_time
    }
    input_df = pd.DataFrame([user_data])
    predicted_level = models["KNN"].predict(input_df)[0]

    print(f"\n{'='*45}")
    print(f"  🎓 Student Fatigue Level : {predicted_level}")
    print(f"  📊 Student Fatigue Score : {student_score:.1f}/100")
    print(f"{'='*45}")

    # Student specific suggestions
    print("\n💡 Student Suggestions:")
    if exam_stress >= 7:
        print("   😰 High exam stress! Try the Pomodoro technique.")
        print("   📖 Study in 25-min focused sessions with 5-min breaks.")
    if days_to_exam <= 3 and days_to_exam > 0:
        print(f"   ⏰ Exam in {days_to_exam} day(s)! Prioritize revision over new topics.")
    if assignments_pending >= 3:
        print(f"   📋 {assignments_pending} assignments pending — make a priority list now!")
    if sleep_hours < 6:
        print("   😴 Don't sacrifice sleep before exams — memory needs rest!")
    if student_score > 60:
        print("   🧘 Take a 10-min break RIGHT NOW before continuing.")

    # Daily challenge for students
    student_challenges = [
        "Complete 1 pending assignment today 📝",
        "Study using Pomodoro: 25min on, 5min off ⏱️",
        "No phone for first 2 hours of study 📵",
        "Sleep before midnight tonight 🌙",
        "Drink water every hour during study 💧"
    ]
    print(f"\n🎯 Student Challenge:")
    print(f"   → {random.choice(student_challenges)}")

    save_memory({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "level": predicted_level,
        "score": round(student_score, 1),
        "mode": "student"
    })
    print("\n✅ Student session saved!")
    print("="*45)
    
import time

# ─── Guided Breathing ───
def guided_breathing():
    print("\n" + "="*45)
    print("   🌬️  GUIDED BREATHING EXERCISE")
    print("="*45)
    print("  This will take 2 minutes. Follow along...\n")
    
    for cycle in range(1, 4):
        print(f"  Cycle {cycle}/3:")
        print("  👃 Breathe IN...", end="", flush=True)
        time.sleep(4)
        print(" Hold...", end="", flush=True)
        time.sleep(4)
        print(" 😮 Breathe OUT...")
        time.sleep(6)
        print()
    
    print("  ✅ Great! You should feel calmer now.\n")

# ─── Pomodoro Timer ───
def pomodoro_timer():
    print("\n" + "="*45)
    print("   ⏱️  POMODORO FOCUS TIMER")
    print("="*45)
    print("  25 min focus → 5 min break\n")

    sessions = int(input("  How many Pomodoro sessions? (e.g. 2): "))

    for i in range(1, sessions + 1):
        print(f"\n  🍅 Session {i}/{sessions} — FOCUS TIME!")
        print("  Stay off social media. Focus on your task.")
        print("  ⏳ 25 minutes starting now...\n")

        # Show countdown every 5 mins
        for remaining in [20, 15, 10, 5]:
            time.sleep(300)  # 5 min
            print(f"  ⏰ {remaining} minutes remaining...")

        time.sleep(300)
        print(f"\n  ✅ Session {i} complete! Take a 5-min break.")

        if i < sessions:
            print("  💤 Break starting...")
            time.sleep(300)
            print("  🔔 Break over! Get ready for next session.")

    print("\n  🎉 All Pomodoro sessions complete! Great work!")
    print("="*45)

    # ─── Mood Trend Chart ───
def mood_trend():
    memory = load_memory()
    if len(memory) < 2:
        print("\n⚠️ Not enough sessions yet! Run the bot a few times first.")
        return

    print("\n📊 Your Fatigue History:")
    dates = []
    scores = []

    for entry in memory:
        print(f"  {entry['date']} → {entry['level']} ({entry['score']})")
        dates.append(entry['date'])
        scores.append(entry['score'])

    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(range(len(scores)), scores, marker='o', 
            color='steelblue', linewidth=2, markersize=8)
    
    # Color zones
    ax.axhspan(0,  35, alpha=0.1, color='green',  label='Low')
    ax.axhspan(35, 65, alpha=0.1, color='orange', label='Medium')
    ax.axhspan(65, 100, alpha=0.1, color='red',   label='High')

    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels(
        [d[:10] for d in dates], rotation=45, fontsize=8)
    ax.set_ylabel("Fatigue Score")
    ax.set_title("🧠 Your Cognitive Fatigue Trend")
    ax.set_ylim(0, 100)
    ax.legend()
    fig.tight_layout()
    fig.savefig("mood_trend.png")
    print("\n✅ Trend chart saved as mood_trend.png!")
    print("📁 Check your project folder to view it.")

print("\n🌟 Select Mode:")
print("  1 - Normal Mode")
print("  2 - Student Mode")
print("  3 - Pomodoro Timer")
print("  4 - Guided Breathing")
print("  5 - View Mood Trend Chart")
mode = input("Enter 1/2/3/4/5: ")

if mode == "2":
    student_mode()
elif mode == "3":
    pomodoro_timer()
elif mode == "4":
    guided_breathing()
elif mode == "5":
    mood_trend()
else:
    wellness_bot()