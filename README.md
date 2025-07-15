# Guide to the Project

## Task Requirements
You are provided with part of an internal FastAPI project for a small business application. Your task is to implement user registration and login API endpoints that securely handle user data, including:

- **User registration** (via `/register`):
  - Accepts email, password, and display name
  - Validates input and enforces unique email addresses
  - Stores user data **securely** (passwords must be hashed)
  - Returns properly structured responses and error codes

- **User login** (via `/login`):
  - Accepts email and password
  - Authenticates users using hashed passwords
  - On success, returns a valid JWT access token in the response
  - Returns robust error handling (401 for invalid credentials, 400 for bad requests)

All user data must persist **in-memory** (e.g., dictionary or list), with **no external or persistent storage**. Use FastAPI best practices, including Pydantic models for request/response, and secure password handling.

You must only modify the `routes/user.py` file. The rest of the project (main app file, config, and test scripts) is already set up and should not be changed.

## What You Should Deliver
- Two fully functional FastAPI routes (register, login) as described
- Robust validation and error responses using Pydantic models and FastAPI's error handling
- In-memory storage for user data, handling unique emails and password hashing securely
- JWT token generation for successful authentication
- Use FastAPI's dependency injection and response modeling where appropriate

**Do not make architectural changes or modify files outside `routes/user.py`.**

## Verifying Your Solution
- Registration and login endpoints should work within the provided project structure
- Registering duplicate emails must be rejected with correct error responses
- Passwords must be stored in hashed form and never returned in any response
- JWT tokens should be valid and parseable (but actual JWT verification is not part of this task)
- All responses must have appropriate status codes and adhere to the specified response models

If you see existing tests or scripts, running those will help verify the correctness of your implementation.

---

**Tip:** Review the structure of existing Pydantic models and FastAPI error handling for structured, clear responses. Follow security best practices for password storage (hashing, never storing plaintext), and verify JWT generation is correct.