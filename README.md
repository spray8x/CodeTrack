# CodeTrack - Coding Problem Practice Tracker

> A comprehensive Python-based tool to track coding practice, analyze progress, and identify areas for improvement.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📖 Overview

**CodeTrack** is a local-first practice tracking system designed for students and programmers who want to systematically monitor their coding problem-solving journey. It provides a command-line interface to manage problems, track timed practice sessions, and generate insightful analytics about your progress.

Whether you're preparing for technical interviews, competing in coding contests, or simply improving your problem-solving skills, CodeTrack helps you stay organized and motivated.

---

## ✨ Features

### 🗂️ Problem Library Management
- Add, edit, and delete coding problems
- Categorize by difficulty (Easy, Medium, Hard)
- Tag with multiple topics (Arrays, DP, Graphs, Strings, etc.)
- Track status for each problem (Not Started, In Progress, Solved, Reviewed)
- Search and filter by any attribute
- Store problem URLs and platform information

### ⏱️ Practice Session Tracking
- Start timed practice sessions for problems
- Pause and resume timer functionality
- Add notes during practice (approach, observations)
- Progressive hints system
- Store your solution code
- Complete session history with timestamps

### 📊 Analytics & Progress Dashboard
- View total problems solved and current streak
- Analyze success rate by topic
- See average solve time by difficulty
- Visual charts and graphs:
  - Problems solved over time
  - Difficulty distribution
  - Topic strength analysis
  - Practice calendar (30-day heatmap)
- Identify weak areas needing more practice
- Export reports for review

### 💾 Data Management
- JSON-based local storage
- Automatic backup functionality
- Data validation and error handling
- Import/export capabilities

---

## 🛠️ Technologies & Tools Used

- **Language:** Python 3.8+
- **Data Storage:** JSON
- **Visualization:** Matplotlib, Seaborn
- **CLI Enhancement:** Colorama (for colored terminal output)
- **Date/Time:** datetime, time modules
- **Data Processing:** collections, itertools
- **Testing:** unittest

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/codetrack.git
cd codetrack
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python main.py
```

---

## 🚀 How to Use

### First Time Setup
When you run CodeTrack for the first time, it will automatically create the necessary data directories and files.

### Main Menu Options

```
=== CodeTrack - Main Menu ===
1. Problem Library Manager
2. Practice Session Tracker
3. Analytics & Reports
4. Settings & Data Management
5. Exit
```

### Example Workflow

#### 1. Add a New Problem
```
Select: Problem Library Manager → Add New Problem

Enter problem details:
- Title: Two Sum
- Difficulty: Easy
- Topics: Arrays, Hash Table
- Platform: LeetCode
- URL: https://leetcode.com/problems/two-sum/
```

#### 2. Start a Practice Session
```
Select: Practice Session Tracker → Start New Session

Choose a problem from your library
Timer starts automatically
Add notes as you work
Mark as solved when complete
```

#### 3. View Your Progress
```
Select: Analytics & Reports → Dashboard

View:
- Current streak: 7 days
- Total solved: 45 problems
- Weak topics: Dynamic Programming (40% success)
- Strong topics: Arrays (85% success)
```

---

## 📸 Screenshots

### Main Dashboard
```
╔═══════════════════════════════════════════════╗
║           CodeTrack Dashboard                 ║
╠═══════════════════════════════════════════════╣
║  Total Problems: 127                          ║
║  Problems Solved: 45 (35%)                    ║
║  Current Streak: 7 days 🔥                    ║
║  Avg Time (Medium): 32 minutes                ║
╚═══════════════════════════════════════════════╝
```

### Topic Strength Analysis
```
Arrays          ████████████████░░ 85%
Strings         ███████████████░░░ 78%
Graphs          ██████████░░░░░░░░ 55%
Dynamic Prog    ███████░░░░░░░░░░░ 40%
```

*(Add actual screenshots here when your app is ready)*

---

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run specific test module:
```bash
python -m pytest tests/test_problem_manager.py
```

---

## 📁 Project Structure

```
CodeTrack/
├── main.py                      # Entry point
├── modules/
│   ├── __init__.py
│   ├── problem_manager.py       # Problem library operations
│   ├── session_tracker.py       # Practice session tracking
│   └── analytics.py             # Analytics and reports
├── utils/
│   ├── __init__.py
│   ├── data_handler.py          # JSON file operations
│   ├── validators.py            # Input validation
│   └── helpers.py               # Utility functions
├── ui/
│   └── cli_interface.py         # Command-line interface
├── data/
│   ├── problems.json            # Problem library
│   ├── sessions.json            # Session history
│   └── user_stats.json          # User statistics
├── tests/
│   └── test_modules.py          # Unit tests
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── statement.md                 # Project statement
```

---

## 🤝 Contributing

This is a student project, but suggestions and feedback are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**[Your Name]**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Inspired by the need for better practice tracking during interview preparation
- Built as part of VITyarthi Problem Solving course project
- Thanks to all open-source libraries used in this project

---

## 🔮 Future Enhancements

- [ ] Web-based GUI using Flask
- [ ] Integration with LeetCode/Codeforces APIs
- [ ] Collaborative features (share progress with study groups)
- [ ] Mobile app version
- [ ] AI-powered problem recommendations
- [ ] Spaced repetition algorithm for review scheduling
- [ ] Export to Notion/Obsidian for note-taking integration

---

**Happy Coding! 🚀**
