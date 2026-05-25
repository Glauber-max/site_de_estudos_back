#  AI Video Summarizer & Auth Hub
this project is a RESTful API built with FastAPI that automates the process of generating detailed summaries from YouTube videos using multimodal Artificial Intelligence (Gemini 2.5 Flash). Additionally, the application features a complete, secure authentication and user management ecosystem utilizing JWT, Redis for session/staging caching, and SQLITE or other database for persistent data.

##  Technologies & Infrastructure

* **Python 3.11+**
* **FastAPI** (High-performance Web Framework)
* **SQLITE** (Relational Database for users and summaries storage)
* **Redis** (In-memory database for temporary staging cache and session tokens)
* **Google GenAI SDK** (Native integration with Gemini 2.5 Flash and Gemma)
* **Pytube** (YouTube audio extraction and download)
* **PyJWT / Passlib** (Secure JWT generation and password hashing with bcrypt)
* **SMTP / Email Service** (Password recovery token delivery system)

## Advanced System Flows

### 1. User Registration & Activation (Staging Pattern)
To prevent "ghost" or unverified users from bloating the primary database, the initial signup process hashes the password and stores the temporary user object inside **Redis**. An activation token is sent via email; once successfully verified, the user data is fetched from Redis and permanently persisted into **SQLITE**.

### 2. Primary AI Pipeline (Gemini 2.5 Flash)
The audio stream is extracted from the YouTube video and uploaded directly to Google's Files API. Gemini 2.5 Flash processes the native audio file directly in approximately 30 seconds, returning a highly accurate, structured summary mapped straight into a Pydantic Validation Schema.

### 3. Resilient AI Fallback (Gemma + Whisper)
If the Gemini API encounters rate limits or downtime, the system automatically triggers a local fallback pipeline. A local Whisper instance transcribes the audio into a long text block, which is then fed into the Gemma LLM to compile the structured summary.

---

##  Prerequisites

Ensure you have the following components installed on your environment:
* **Python 3.11+**
* A running **Redis Server** (`docker run -d -p 6379:6379 redis`)
* A Google AI Studio **Gemini API Key**
* A Resend (for send email) API key

---

## 🔧 Installation & Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Glauber-max/site_de_estudos_back.git
    cd site_de_estudos_back

2. **Activate the MV:**
    ```bash
   python -m venv venv
    # Ativação (Linux/macOS): source venv/bin/activate
    # Ativação (Windows): .\venv\Scripts\Activate.ps1

3. **install requirements:**
    ```bash
    pip install -r requirements.txt

4. **activate the aplication**
    ```bash
   uvicorn main:app --reload

for see all routes, go in http://127.0.0.1:8000/docs after you run the uvicorn, but in resume is:
user


POST
/user/create_user
Register Routes

POST
/user/validation_account
Router For Validation Token

POST
/user/login
Login

POST
/user/change_passoword
Change Password

PATCH
/user/token/change_password
Verify Token For Change Password

POST
/user/required/acesses_token
Requirements Token

***summary***

POST
/summary/summary_videos/download
Summary Videos

* Refresh Token Leak Fix: Adjust the login controller logic to prevent generating/stacking infinite Refresh Tokens for the same active user inside the database.

* Fallback Optimization: Migrate the standard local Whisper processing over to fast-whisper (bringing fallback execution times down from 10 minutes to under 2 minutes).

* Enhanced Documentation: Expand Docstrings across all Controllers, Factories, and Schemas.

developed by Glauber-max