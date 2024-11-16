# Flask Todo API

A RESTful API built with Flask for managing todo items with user authentication and authorization.

## Features

- User registration and authentication using JWT
- CRUD operations for todo items
- Todo items pagination
- Per-user todo list isolation
- Status tracking for todo items

## Prerequisites

- Python 3.8+
- PostgreSQL/MySQL (or your preferred database)
- pip (Python package manager)
- Postman (for testing)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd flask-todo-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
JWT_SECRET_KEY=your-secret-key-here
```

5. Initialize the database:
```bash
flask db upgrade
```

## API Endpoints Documentation

### Authentication Endpoints

#### 1. Register User
- **URL**: `/register`
- **Method**: `POST`
- **Request Headers**: 
  ```
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
      "name": "John Doe",
      "email": "john@example.com",
      "password": "secure_password"
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**:
    ```json
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
- **Error Response**:
  - **Code**: 400
  - **Content**:
    ```json
    {
        "message": "Email already registered"
    }
    ```

#### 2. Login
- **URL**: `/login`
- **Method**: `POST`
- **Request Headers**: 
  ```
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
      "email": "john@example.com",
      "password": "secure_password"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
- **Error Response**:
  - **Code**: 401
  - **Content**:
    ```json
    {
        "message": "Invalid credentials"
    }
    ```

### Todo Endpoints

All todo endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

#### 1. Create Todo
- **URL**: `/todos`
- **Method**: `POST`
- **Request Headers**:
  ```
  Content-Type: application/json
  Authorization: Bearer <your_jwt_token>
  ```
- **Request Body**:
  ```json
  {
      "title": "Complete project",
      "description": "Finish the REST API implementation",
      "status": "To Do"  // Optional, defaults to "To Do"
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**:
    ```json
    {
        "id": 1,
        "title": "Complete project",
        "description": "Finish the REST API implementation",
        "status": "To Do"
    }
    ```
- **Error Response**:
  - **Code**: 400
  - **Content**:
    ```json
    {
        "message": "Title is required"
    }
    ```

#### 2. Get All Todos
- **URL**: `/todos`
- **Method**: `GET`
- **Request Headers**:
  ```
  Authorization: Bearer <your_jwt_token>
  ```
- **URL Parameters**:
  - `page` (optional, default=1): Page number
  - `limit` (optional, default=10): Items per page
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
        "data": [
            {
                "id": 1,
                "title": "Complete project",
                "description": "Finish the REST API implementation",
                "status": "To Do"
            }
        ],
        "page": 1,
        "limit": 10,
        "total": 1
    }
    ```

#### 3. Update Todo
- **URL**: `/todos/<todo_id>`
- **Method**: `PUT`
- **Request Headers**:
  ```
  Content-Type: application/json
  Authorization: Bearer <your_jwt_token>
  ```
- **Request Body**:
  ```json
  {
      "title": "Updated title",
      "description": "Updated description",
      "status": "In Progress"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
        "id": 1,
        "title": "Updated title",
        "description": "Updated description",
        "status": "In Progress"
    }
    ```
- **Error Responses**:
  - **Code**: 404
    ```json
    {
        "message": "To-Do item not found"
    }
    ```
  - **Code**: 403
    ```json
    {
        "message": "You do not have permission to edit this To-Do item"
    }
    ```

#### 4. Delete Todo
- **URL**: `/todos/<todo_id>`
- **Method**: `DELETE`
- **Request Headers**:
  ```
  Authorization: Bearer <your_jwt_token>
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
        "message": "To-Do item deleted successfully"
    }
    ```
- **Error Responses**:
  - **Code**: 404
    ```json
    {
        "message": "To-Do item not found"
    }
    ```
  - **Code**: 403
    ```json
    {
        "message": "You do not have permission to delete this To-Do item"
    }
    ```

## Testing with Postman

### Setting Up Postman

1. Import the API collection:
   - Create a new collection in Postman
   - Name it "Todo API"
   - Create folders for "Auth" and "Todos"

2. Set up environment variables:
   - Create a new environment in Postman
   - Add the following variables:
     - `BASE_URL`: `http://localhost:5000`
     - `TOKEN`: Empty 


### Testing Flow

1. **Register a New User**:
   - Send POST request to `{{BASE_URL}}/register`
   - Body:
     ```json
     {
         "name": "Test User",
         "email": "test@example.com",
         "password": "test123"
     }
     ```
   - Save the returned token

2. **Login**:
   - Send POST request to `{{BASE_URL}}/login`
   - Body:
     ```json
     {
         "email": "test@example.com",
         "password": "test123"
     }
     ```
   - Verify token is received
   - Token will be automatically saved to environment variable

3. **Create a Todo**:
   - Send POST request to `{{BASE_URL}}/todos`
   - Add Authorization header:
     ```
     Bearer {{TOKEN}}
     ```
   - Body:
     ```json
     {
         "title": "Test Todo",
         "description": "Testing the API",
         "status": "To Do"
     }
     ```
   - Save the returned todo ID for future tests

4. **Get All Todos**:
   - Send GET request to `{{BASE_URL}}/todos?page=1&limit=10`
   - Verify pagination works
   - Verify returned todos belong to authenticated user

5. **Update Todo**:
   - Send PUT request to `{{BASE_URL}}/todos/1`
   - Body:
     ```json
     {
         "status": "In Progress"
     }
     ```
   - Verify todo status is updated

6. **Delete Todo**:
   - Send DELETE request to `{{BASE_URL}}/todos/1`
   - Verify todo is deleted
   - Verify attempting to get deleted todo returns 404


## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 200: Success
- 201: Resource created
- 400: Bad request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource not found
- 500: Server error

## Security Considerations

1. Always use HTTPS in production
2. Store JWT tokens securely
3. Implement rate limiting for API endpoints
4. Sanitize and validate all input data
5. Use environment variables for sensitive configuration
6. Regularly update dependencies

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
