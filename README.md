# Study Hub API

**Product Vision**
Develop an "Intelligent Study Hub" that leverages generative AI to transform multimedia content into educational material, reducing students' preparation time and centralizing their personal organization tools within a secure system.


## explain the architecture (MVP)

The project architecture follows an MVC model, where we have the model for storing table information, the controller for
handling the more complex functions that call other functions. The view/routes is the API itself that will receive requests
and contact the other functions. In the services folder, we have functions specific to Redis, sending emails, and creating 
questions and video summaries via AI. Finally, we have folders like schemas and database, which are used to filter request 
information and connect to the database, respectively.
The project has token authentication, and requests based on JWT.
Two different AI models in case one fails, and a log of errors or request information.

## Technologies

* Python >3.10 version
* Framework: FastAPI for create API
* Database: SQLite with SQLAlchemy ORM (it can be replaced by other relational databases if used in production)
* AI/Multimodal: Google GenAI SDK to create all the summaries and questions
* Cache/Session: Redis (Docker) used to temporarily store user data until the account is validated, then it gets added to the database
* Security: Passlib (Argon2), PyJWT
* Messaging: Resend

## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/Glauber-max/site_de_estudos_back.git
cd site_de_estudos_back
```
2. Set up the virtual environment:
```bash
python -m venv venv
#active the virtual environment

# Linux/macOS: source venv/bin/activate

# Windows: .\venv\Scripts\Activate.ps1
```
3. Install dependencies (make sure your virtual environment is active):
```bash
pip install -r requirements.txt
```
4. Configure your API Keys and environment:
   * Create an API key in Google AI Studio: https://aistudio.google.com/api-keys
   * Create an API key in Resend: https://resend.com/api-keys
   * *Note: If you have a custom domain, update `send_email.py` (line 23), changing `onboarding@resend.dev` to your domain.*

if you don't have a custom domain and want only test, send email for yourself email, follow this struct in archive .env
```env
RESEND_API_KEY=your_resend_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
EMAIL_FROM=onboarding@resend.dev  # Change to your custom domain email in production
```
5. Start Redis via Docker: 
```bash
docker compose up -d 
```
6. Start the server:

before using uvicorn in the terminal, make sure the database has been created correctly, 
go to the main.py file and run that file containing the 'create_table' function to create a new database

```bash
uvicorn main:app --reload
```
Access the interactive documentation (Swagger UI) at: http://127.0.0.1:8000/docs

Next Steps:
Device Concurrency: Update the login flow to avoid blindly overwriting the refresh token, allowing multiple concurrent sessions utilizing Device IDs.

Soft Delete: Replace the current hard delete system with a boolean flag to protect against accidental data loss.

Unit Tests: Add Pytest test coverage for the AI and Summary modules.

Front-end Integration: Begin development of the web client to consume the API.