# TechRecall 🧠

**TechRecall** is a Spaced Repetition System (SRS) designed specifically for Computer Science interview preparation. It helps students retain theoretical concepts (OS, DBMS, SQL, Networks) using a smart scheduling algorithm and a gamified "swipe" interface.

## 🚀 Features

- **Smart Review Scheduling**: Uses a modified SuperMemo-2 algorithm to schedule reviews.
- **Swipe-to-Study**: Tinder-style interface for quick reviews (Right = Knew it, Left = Forgot).
- **Progress Heatmap**: Visualizes your daily study consistency.
- **Deck Management**: Create and organize cards by topics.

## 🛠️ Tech Stack

- **Frontend**: Vue 3, Vite, TailwindCSS
- **Backend**: Flask, SQLAlchemy, SQLite (Dev) / PostgreSQL (Prod)
- **Deployment**: Docker, Gunicorn

## 📦 Installation

### Backend

1. Navigate to backend: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Run app: `python run.py`

### Frontend

1. Navigate to frontend: `cd frontend`
2. Install dependencies: `npm install`
3. Run dev server: `npm run dev`

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
