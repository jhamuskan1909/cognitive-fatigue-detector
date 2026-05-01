# Cognitive Fatigue Detector

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?style=for-the-badge&logo=mongodb)
![Gemini AI](https://img.shields.io/badge/Gemini-2.5_Flash-orange?style=for-the-badge&logo=google)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-red?style=for-the-badge&logo=scikit-learn)
![Render](https://img.shields.io/badge/Deployed-Render-purple?style=for-the-badge)

**An AI-powered wellness web app that detects cognitive fatigue using lifestyle inputs, machine learning, and a Gemini-powered AI companion.**

[Live Demo](https://cognitive-fatigue-detector.onrender.com) · [Report Bug](https://github.com/jhamuskan1909/cognitive-fatigue-detector/issues) · [Request Feature](https://github.com/jhamuskan1909/cognitive-fatigue-detector/issues)

</div>

---

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [ML Models](#ml-models)

---

## About the Project

Cognitive fatigue is a silent productivity killer — most people don't realize how their daily habits (sleep, screen time, diet, hydration) are quietly burning them out.

**Cognitive Fatigue Detector** takes your daily lifestyle inputs and uses machine learning (Decision Tree, Random Forest, KNN) to predict your fatigue level as **Low / Medium / High**. It then gives personalized suggestions, a daily wellness challenge, and access to **Muskmoon** — a Gemini 2.5 Flash-powered AI companion for mental wellness conversations.

A dedicated **Student Mode** factors in exam stress, pending assignments, and days until exams for more targeted advice.

---

## Features

| Feature | Description |
|---|---|
| **Auth System** | Register/Login with hashed passwords stored in MongoDB |
| **Fatigue Prediction** | KNN model predicts Low / Medium / High fatigue from 7 lifestyle inputs |
| **Student Mode** | Extended scoring with exam stress, pending assignments & days to exam |
| **Smart Suggestions** | Rule-based personalized wellness tips based on your specific inputs |
| **Daily Challenges** | One actionable wellness challenge assigned per session |
| **Session History** | All past fatigue sessions stored and viewable per user |
| **Muskmoon AI Chat** | Gemini 2.5 Flash-powered empathetic AI companion for mental wellness |
| **Feature Importance** | Random Forest feature importance scores exposed via API |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, Flask |
| **ML Models** | scikit-learn (KNN, Random Forest, Decision Tree) |
| **Database** | MongoDB Atlas via PyMongo |
| **AI Companion** | Google Gemini 2.5 Flash API |
| **Frontend** | HTML, CSS, JavaScript (Jinja2 templates) |
| **Deployment** | Render (Gunicorn WSGI) |

---

## Project Structure

```
cognitive-fatigue-detector/
│
├── app.py                  # Main Flask app — routes, ML models, MongoDB
├── fatigue_detector.py     # Standalone CLI version of the detector
├── requirements.txt        # Python dependencies
├── Procfile                # Render/Gunicorn deployment config
├── session_memory.json     # Local fallback session storage (CLI mode)
│
├── templates/
│   └── index.html          # Main frontend (single-page app)
│
└── .env.example            # Environment variable template
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account (free tier works)
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/cognitive-fatigue-detector.git
cd cognitive-fatigue-detector
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install python-dotenv
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
MONGO_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/cogni_fatigue
GEMINI_API_KEY=your_gemini_api_key_here
```

Add these two lines to the top of `app.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 5. Run the app

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `MONGO_URI` | MongoDB Atlas connection string | Yes |
| `GEMINI_API_KEY` | Google Gemini API key for Muskmoon chat | Yes |
| `PORT` | Port to run Flask on (default: 5000) | Optional |

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/register` | ❌ | Register a new user |
| `POST` | `/api/login` | ❌ | Login and start session |
| `POST` | `/api/logout` | ❌ | Clear session |
| `GET` | `/api/me` | ❌ | Get logged-in user info |
| `POST` | `/api/predict` | ✅ | Predict fatigue from lifestyle inputs |
| `POST` | `/api/student` | ✅ | Predict fatigue in student mode |
| `GET` | `/api/history` | ✅ | Get user's past sessions |
| `GET` | `/api/features` | ❌ | Get ML feature importances |
| `POST` | `/api/chat` | ❌ | Chat with Muskmoon (Gemini AI) |

### Example `/api/predict` payload

```json
{
  "sleep_hours": 6.5,
  "screen_time": 5,
  "physical_activity": 0.5,
  "work_study_hours": 8,
  "water_intake": 2,
  "diet_quality": 3,
  "sleep_time": 23.5
}
```

### Example response

```json
{
  "level": "Medium",
  "score": 54.5,
  "suggestions": [
    "⚠️ Moderate fatigue detected. Take preventive steps.",
    "📚 You've been studying/working too long — take a 15-min break.",
    "🧘 Try 5 minutes of deep breathing to reset focus."
  ],
  "challenge": "Take a 15-min walk 🚶"
}
```

---

## ML Models

Three models trained on a synthetic dataset of 500 samples with 7 lifestyle features:

| Model | Notes |
|---|---|
| **Decision Tree** | Fast, interpretable baseline |
| **Random Forest** | Used for feature importance scores |
| **KNN (k=5)** | Used for all live predictions |

**Input features:** `sleep_hours`, `screen_time`, `physical_activity`, `work_study_hours`, `water_intake`, `diet_quality`, `sleep_time`

**Output classes:** `Low` (score < 35), `Medium` (35–65), `High` (> 65)

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Acknowledgements

- [Google Gemini API](https://aistudio.google.com/) — powering Muskmoon AI
- [scikit-learn](https://scikit-learn.org/) — ML model training
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) — cloud database
- [Render](https://render.com/) — free hosting

---

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "feat: your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request
