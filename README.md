# SocratesAI 🧠

**The AI Tutor That Teaches You *How* to Think.**

## 📌 Problem & Solution

**The Problem:**
Students often struggle to learn independently. Traditional resources or direct Answer-engines give the solution immediately, depriving students of the critical thinking process required to truly master a subject.

**The Solution:**
SocratesAI is an intelligent tutoring system built on the Socratic method. Instead of providing direct answers, it guides students through the learning process using a "Why, How, What" approach. It breaks down complex problems (like math equations `2x + 4 = 10`) into step-by-step logical progressions, offering hints and asking leading questions to help students derive the solution themselves.

---

## 🚀 Key Features

- **Socratic Tutoring Engine:** Powered by Google's Gemini Pro, the AI adopts the persona of Socrates to guide users with questions rather than answers.
- **Multi-Modal Learning:** Support for uploading PDFs and Images to provide context for questions (e.g., uploading a screenshot of a math problem).
- **Contextual Memory:** Remembers the conversation history to maintain context throughout the problem-solving session.
- **Interactive UI:** A modern, responsive React-based frontend for seamless interaction.
- **Real-time Feedback:** Instant responses to guide students through their thought process.

---

## 🛠️ Technical Stack

- **Frontend:** React, Vite, Lucide React
- **Backend:** Python, FastAPI, Uvicorn
- **AI/LLM:** Google Gemini Pro (`google-generativeai`)
- **Storage:** In-memory session storage (Redis ready)

---

## 📦 Installation & Usage

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- Google Gemini API Key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/socrates-ai.git
cd socrates-ai
```

### 2. Backend Setup
Navigate to the backend directory and set up the Python environment.

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**Configuration:**
Create a `.env` file in the `backend/` directory:
```env
GEMINI_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-pro
```

**Run the Server:**
```bash
uvicorn app.main:app --reload
```
The backend will start at `http://localhost:8000`.

### 3. Frontend Setup
Open a new terminal and navigate to the frontend directory.

```bash
cd frontend
npm install
npm run dev
```
The frontend will launch at `http://localhost:5173`.

---

## 📝 Usage

1. Open the application in your browser.
2. Type a question or math problem into the chat input (e.g., "Help me solve 3x - 5 = 10").
3. Alternatively, upload a document or image for the AI to analyze.
4. Follow the AI's guidance as it leads you through the solution steps!
