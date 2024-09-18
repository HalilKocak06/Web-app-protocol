# Chat Assistant with Flask

This project implements a basic chat assistant using Flask as a web framework. It uses SQLite as a database to store user information and chat history. Additionally, the project incorporates password hashing with `bcrypt`, session management with `Flask-Session`, and integrates the `MaipClient` and `MaipContext` classes to handle chat interactions.

## Project Structure

- **HTML/CSS/JS**: Frontend of the application, including templates for:
  - Sign-up (`sign_up.html`)
  - Sign-in (`sign_in.html`)
  - Chat (`new_chat.html`)
  - User homepage (`user_home.html`)
  
- **Python Files**: 
  - `context-resolver-builder-client.py`: Handles the core logic for the chat assistant.
  - `MaipClient`, `MaipContext`, `MaipBuilder`: Responsible for context generation and handling the chat functionality.

## Key Features

- **User Authentication**: 
  - Sign-up functionality with password hashing using `bcrypt`.
  - Secure user sign-in with session management.
  - User sessions for maintaining state between requests.
  
- **Chat Functionality**: 
  - Save user and assistant messages in a SQLite database.
  - A chat context is generated using `MaipClient` and `MaipContext`.
  
- **Database**: 
  - SQLite database (`users_info.db` and `chat.db`) to store user credentials and chat history.

## Prerequisites

- Python 3.x
- Flask
- SQLite3
- `bcrypt`
- `flask-session`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
2. **Install the libraries**
pip install -r requirements.txt

3. **Database Setup:**

The application will automatically create the SQLite databases (users_info.db and chat.db) when you run the app for the first time.

4.**Run the Flask application:**

python app.py

5.**Access the application:**

Open a web browser and go to http://127.0.0.1:5000.

## Usage
Sign-Up: Create a new account on the sign-up page (/sign_up).

Sign-In: Log in to your account on the sign-in page (/sign_in).

Chat: After signing in, you will be redirected to the chat interface. Start a new chat session, and your interactions will be saved in the database.

## Security
Passwords are hashed using bcrypt to ensure secure storage.
Sessions are managed securely using Flask's SECRET_KEY.
