---

# Study Hub API (AI-Powered)

**Product Vision:**
Develop an "Intelligent Study Hub" that leverages generative AI to transform multimedia content into educational material, reducing students' preparation time and centralizing their personal organization tools within a secure, high-performance ecosystem.

---

## Core Features (MVP Backlog)

* **User Module (Auth):**
* Registration with email verification using Redis as a temporary cache (Staging Pattern).
* Bulletproof authentication system with JWT (Access and Refresh Tokens).
* Password recovery via temporary tokens sent by email.


* **Summary Module (AI):**
* Transcription and structured summarization focused on objectivity using Gemini models (3.5/2.5 Flash).


* **Questions Module (AI):**
* Automatic generation of objective questions (multiple choice A-E) based on summaries.
* Detailed resolutions explaining the correct answer and the necessary fundamentals.
* Full CRUD (Create, Read, Update, Delete) for question management.


* **Organization Module (Productivity):**
* Full CRUD for Notes to jot down summaries or general content.



---

##  Crucial Business Rules & Architecture

* **AI Fallback:** If the primary AI model (Gemini 3.5) fails or hits its token limit, the system uses a *Factory* pattern to automatically attempt processing via the 2.5 model before returning an error.
* **Cache Security:** Account validation and password reset tokens have a strict TTL (Time-To-Live) of 300 seconds (5 minutes) in Redis.
* **Data Isolation (Tenant-like):** No data (note, question, summary) can be accessed, modified, or deleted unless it strictly belongs to the `sub` (ID) contained in the authenticated user's JWT.

---

##  Technologies & Infrastructure

* **Framework:** FastAPI
* **Database:** SQLite (ORM: SQLAlchemy)
* **AI/Multimodal:** Google GenAI SDK (Gemini 2.5/3.5 Flash)
* **Audio:** `faster-whisper` (Optimized local processing)
* **Cache/Session:** Redis (Recommended via Docker)
* **Security:** Passlib (Argon2), PyJWT
* **Messaging:** Email via `resend`

---

##  Quality Assurance & Testing (QA)

### 1. Requirements Traceability Matrix (RTM)

| ID        | Feature            | Main Test Scenario                                                            | Priority | Status |
|-----------|--------------------|-------------------------------------------------------------------------------|----------|--------|
| **US-01** | Registration/Login | Validate email flow and password hash creation.                               | High     | 🟢 OK  |
| **US-02** | Refresh Token      | Validate token renewal without forcing a new login.                           | High     | 🟢 OK  |
| **US-03** | Summary (AI)       | Test transcription and JSON integrity returned by the AI.                     | High     | 🟢 OK  |
| **US-04** | Questions (AI)     | Validate the number of questions and the structure of the alternatives (A-E). | Medium   | 🟢 OK  |
| **US-05** | Notes CRUD         | Validate CRUD with scope strictly limited to the logged-in user.              | High     | 🟢 OK  |

### 2. Test Plan (Security Checklist)

* **IDOR (Insecure Direct Object Reference) Audit:**
* *Criteria:* Authenticate User A and attempt to alter/delete data belonging to User B. The system must return HTTP 404 or 403.


* **Sanitization Audit against Prompt Injection:**
* *Criteria:* Insert malicious payloads into the base text. The AI must ignore the commands and return `None`.


* **Persistence Audit (Resilience):**
* *Criteria:* Simulate a network outage during AI processing. The database must trigger a `rollback` to avoid orphaned or corrupted data.



---

## 🔧 Installation & Setup

**1. Clone the repository:**

```bash
git clone https://github.com/Glauber-max/site_de_estudos_back.git
cd site_de_estudos_back

```

**2. Set up the Virtual Environment:**

```bash
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1
# Linux/macOS: source venv/bin/activate

```

**3. Start Redis via Docker:**

```bash
docker run -d -p 6379:6379 redis

```

**4. Install dependencies:**

```bash
pip install -r requirements.txt

```

**5. Start the server:**

```bash
uvicorn main:app --reload

```

*Access the interactive documentation (Swagger UI) at: `http://127.0.0.1:8000/docs*`

---

##  API Endpoints

### User

* **POST** `/user/create_user` - Register Routes
* **POST** `/user/validation_account` - Router For Validation Token
* **POST** `/user/login` - Login
* **POST** `/user/change_passoword` - Change Password
* **PATCH** `/user/token/change_password` - Verify Token For Change Password
* **POST** `/user/required/acesses_token` - Requirements Token
* **DELETE** `/user/delete/tables` - Hard Delete
* **POST** `/user/logout` - Logout
* **GET** `/user/obter/usuario` - Get User

### Summary

* **POST** `/summary/summary_videos/download` - Summary Videos
* **GET** `/summary/summary_videos/filter` - See Summary
* **GET** `/summary/summary_videos/see_all` - See All Summary
* **DELETE** `/summary/summary_videos/delete/{id_summary}` - Delete Summary

### Notes

* **POST** `/notes/write` - Write Note
* **GET** `/notes/get_note_all` - Get Notes
* **GET** `/notes/get_note/filter` - Get Filter Notes
* **DELETE** `/notes/delete_note/{note_id}` - Delete Note
* **PATCH** `/notes/update_note/{note_id}` - Update Notes

### Questions

* **POST** `/question/create/question` - Create Question
* **POST** `/question/create/question/ia` - Create Question Ia
* **PATCH** `/question/update/question/{question_id}` - Update Question
* **DELETE** `/question/delete/question/{question_id}` - Delete Question
* **GET** `/question/questions/get_all` - Get All Questions
* **GET** `/question/questions/filter` - Filter Questions

---

##  Known Issues & Roadmap (Next Steps)

* 🟡 **[BUG-002] Device Concurrency:** Update the login flow to avoid blindly overwriting the `refresh_token` in the database, allowing multiple concurrent sessions (e.g., Mobile and Desktop).
* 🔵 **[ENHANCEMENT-001] Soft Delete:** Replace the current *Hard Delete* system in the tables with a boolean flag (`is_active: False`), protecting the database against accidental data loss and allowing account restoration.
* 🔵 **[ENHANCEMENT-002] Unit Tests:** Add `pytest` test coverage for the `FactoryQuestionIA` and `FactorySummary` modules.
* 🔵 **[ENHANCEMENT-003] create a front-end

---

*Developed by Glauber-max*