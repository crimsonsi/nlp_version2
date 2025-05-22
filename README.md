# Data Science Interview Simulator

An AI-powered interview simulator that helps you practice data science interview questions and get instant feedback on your answers.

## Features

- 🎯 Practice with real data science interview questions
- ⏱️ Timed interview sessions
- 💡 Instant AI-powered feedback
- 📊 Performance analytics and history
- 🔒 User authentication and progress tracking
- 🎨 Modern and responsive UI

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd interview-prep-assistant
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your configuration:

```
DATABASE_URL=sqlite:///data/interview.db
```

5. Run the application:

```bash
streamlit run app.py
```

## Usage

1. Register a new account or log in with existing credentials
2. Choose an interview category
3. Start the interview session
4. Answer each question within the time limit
5. Get instant feedback on your answers
6. Review your performance and history

## Project Structure

```
interview-prep-assistant/
├── app.py                 # Main application entry point
├── components/           # UI components
│   ├── auth.py          # Authentication component
│   ├── dashboard.py     # Dashboard component
│   ├── interview.py     # Interview component
│   ├── feedback.py      # Feedback component
│   ├── timer.py         # Timer component
│   ├── question.py      # Question component
│   └── results.py       # Results component
├── styles/              # CSS styles
│   ├── main.css        # Main styles
│   └── components.css  # Component-specific styles
├── utils/              # Utility functions
│   ├── db_utils.py     # Database utilities
│   ├── auth_utils.py   # Authentication utilities
│   └── interview_utils.py  # Interview utilities
├── data/               # Data directory
│   └── interview.db    # SQLite database
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
