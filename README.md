# StammerApp API

A FastAPI-based REST API for the StammerApp speech therapy application.

## Features

- User authentication with JWT tokens
- Secure password hashing with bcrypt
- Input validation and error handling
- Database session management
- Comprehensive logging

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (optional):
```bash
export SECRET_KEY="your-secure-secret-key"
export DATABASE_URL="sqlite:///./stammer_app.db"
export ACCESS_TOKEN_EXPIRE_MINUTES="30"
```

3. Run the application:
```bash
python main.py
```

Or using uvicorn:
```bash
uvicorn main:app --reload
```

## API Endpoints

### User Management

#### POST /users/signup
Register a new user (parent).

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

**Response:**
```json
{
  "message": "User registered successfully",
  "user_id": 1
}
```

#### POST /users/login
Login and get JWT token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### GET /users/me
Get current user information (requires authentication).

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-01T00:00:00"
}
```

#### POST /users/logout
Logout (client should discard token).

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

### Kids Management

#### POST /kids/signup
Register a new kid for the authenticated parent.

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Request Body:**
```json
{
  "name": "Sarah",
  "age_group": "5-8",
  "gender": "F"
}
```

**Age Groups:**
- `"5-8"`: Ages 5-8
- `"9-12"`: Ages 9-12

**Gender Options:**
- `"M"`: Male
- `"F"`: Female

**Response:**
```json
{
  "id": 1,
  "name": "Sarah",
  "age_group": "5-8",
  "gender": "F",
  "created_at": "2024-01-01T00:00:00",
  "parent_id": 1
}
```

#### GET /kids/
Get all kids for the authenticated parent.

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Sarah",
    "age_group": "5-8",
    "gender": "F",
    "created_at": "2024-01-01T00:00:00",
    "parent_id": 1
  },
  {
    "id": 2,
    "name": "Tommy",
    "age_group": "9-12",
    "gender": "M",
    "created_at": "2024-01-02T00:00:00",
    "parent_id": 1
  }
]
```

### Other Endpoints

#### GET /
Root endpoint.

**Response:**
```json
{
  "message": "Welcome to StammerApp API"
}
```

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Input validation and sanitization
- Comprehensive error handling
- Logging for security events
- CORS middleware
- Trusted host middleware

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid credentials or missing token
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side errors

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Formatting
```bash
pip install black
black .
```

### Linting
```bash
pip install flake8
flake8 .
```

## Production Deployment

1. Set secure environment variables:
   - `SECRET_KEY`: Use a strong, random secret key
   - `DATABASE_URL`: Use a production database
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Set appropriate token expiration

2. Configure CORS properly for your domain

3. Set up proper logging

4. Use HTTPS in production

5. Consider adding rate limiting middleware

## Database Schema

The application uses SQLAlchemy with the following main models:

- `User`: User accounts with authentication
- `Kid`: Children associated with users
- `Story`: Speech therapy stories
- `StorySentence`: Individual sentences in stories
- `KidStoryProgress`: Progress tracking for kids
- `SpeechAttempt`: Speech attempt recordings and scores
- `Hint`: Speech therapy hints
- `HardLetter`: Letters that kids struggle with

## License

This project is licensed under the MIT License. 