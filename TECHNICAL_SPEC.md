# Technical Specification: SocratesAI

## 1. System Architecture

SocratesAI follows a modern Client-Server architecture, decoupling the frontend user interface from the backend intelligence logic.

```mermaid
graph TD
    User[User] -->|Interacts| Client[React Client (Vite)]
    Client -->|HTTP/JSON| API[FastAPI Backend]     
    
    subgraph Backend Services
        API -->|Route Handler| ServiceLayer[Service Layer]
        ServiceLayer -->|Manage Context| Memory[Memory Service]
        ServiceLayer -->|Generate Response| AI[Gemini Service]
        ServiceLayer -->|Extract Text| FileProc[File Processor]
    end
    
    AI -->|API Call| Gemini[Google Gemini API]
    Memory -->|Store/Retrieve| Redis[(Redis/In-Memory)]
```

### Components
- **Client**: A Single Page Application (SPA) built with React and Vite. Handles user input, chat rendering, and file uploads.
- **Backend API**: Built with FastAPI. Exposes REST endpoints for chat (`POST /chat`) and health checks.
- **Service Layer**:
    - **GeminiService**: Encapsulates logic for interacting with Google's Generative AI. Handles system prompting and model configuration.
    - **MemoryService**: Manages conversation history to provide stateful interactions. Currently supports in-memory storage, designed for extensibility to Redis.
    - **FileProcessor**: Handles parsing of PDF and Image files to extract text or image data for the LLM.

---

## 2. Logic & Algorithms

### The Socratic Engine
The core value proposition is the "Socratic Method" implemented via prompt engineering and state management.

#### Algorithm: Response Generation
1. **Input Reception**: The system receives `user_message`, `conversation_id`, and optional `files`.
2. **Context Retrieval**: 
   - `MemoryService.get_conversation(conversation_id)` fetches previous User-AI exchanges.
   - History is formatted specifically for the Gemini API (User/Model roles).
3. **Prompt Construction**:
   - A static `SOCRATES_SYSTEM_PROMPT` defines the persona: "You are Socrates. Do not give answers. Ask guiding questions. Break down problems."
   - The user's current message and any file context are appended.
4. **Inference**:
   - The constructed context is sent to `Gemini Pro`.
   - The model generates a response adhering to the Socratic constraints.
5. **State Update**:
   - The new exchange (`user_message` and `ai_response`) is appended to the `MemoryService` for the given `conversation_id`.
6. **Response**: The text is returned to the client.

---

## 3. Technology Stack

### Frontend
- **React (v18)**: Component-based UI library for dynamic interfaces.
- **Vite**: Next-generation build tool for fast development and bundling.
- **Lucide-React**: Lightweight, consistent icon library.
- **Axios**: Promise-based HTTP client for API requests.
- **CSS Modules / Standard CSS**: For styling components.

### Backend
- **Python (v3.10+)**: Core programming language.
- **FastAPI**: High-performance web framework for building APIs with Python types.
- **Uvicorn**: ASGI web server implementation.
- **Google Generative AI SDK**: Official Python client for Gemini models.
- **PyPDF2**: Library for extracting text from PDF documents.
- **Pillow (PIL)**: Image processing library.

### Infrastructure & Data
- **Redis (Optional/Planned)**: For persistent, distributed conversation storage.
- **Docker (Recommended)**: For containerized deployment (e.g., `docker-compose` for API + Redis).

---

## 4. Repository Structure

The project maps to a standard monorepo-style structure separating concerns between `backend` and `frontend`.

```
socrates-ai-learning/
├── backend/                # Server-side logic
│   ├── app/
│   │   ├── api/            # API Route definitions
│   │   ├── core/           # Config and System Prompts
│   │   ├── models/         # Pydantic data models
│   │   ├── services/       # Business logic (Gemini, Memory)
│   │   └── main.py         # App entry point
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables
│
├── frontend/               # Client-side application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── assets/         # Static assets
│   │   └── App.jsx         # Main application component
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Build configuration
│
└── README.md               # Project documentation
```
