
# Python Quiz App

A full-featured quiz application built with Python and Tkinter.

## Features

-   **User Authentication:** Register, login, and logout functionality.
-   **Password Security:** Passwords are securely hashed using bcrypt.
-   **Quiz Configuration:** Configure your quiz by:
    -   Number of Questions
    -   Category
    -   Difficulty (Easy, Medium, Hard)
    -   Question Type (Multiple Choice, True/False)
-   **OpenTDB Integration:** Fetches quiz questions from the Open Trivia Database API.
-   **Score Tracking:** Tracks user performance and stores scores in a SQLite database.
-   **Score History:** View your past quiz scores.
-   **Modern UI:** Clean and intuitive user interface inspired by popular quiz apps.

## Author

-   **Niket Basu**

## Getting Started

### Prerequisites

-   Python 3.x
-   pip

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/your-username/python-quiz-app.git
    ```

2.  Navigate to the project directory:

    ```bash
    cd python-quiz-app
    ```

3.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

Run the application with the following command:

```bash
python main.py
```

## Project Structure

-   `main.py`: The main entry point of the application.
-   `gui.py`: Contains all the code for the Tkinter user interface.
-   `database.py`: Handles all SQLite database operations.
-   `api.py`: Manages interactions with the Open Trivia Database API.
-   `requirements.txt`: A list of the required Python packages.
-   `README.md`: This file.

