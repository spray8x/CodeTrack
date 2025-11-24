# CodeTrack - Coding Problem Practice Tracker

## Problem Statement

Students and aspiring programmers who practice coding problems on platforms like LeetCode, HackerRank, and Codeforces often struggle to track their progress systematically. Without proper tracking, it becomes difficult to:

- Identify weak areas that need more practice
- Maintain consistency and build practice streaks
- Understand time spent on different difficulty levels
- Review previously solved problems
- Track improvement over time

Many existing platforms provide basic problem lists but lack personalized analytics and local tracking capabilities. Students need a lightweight, offline-capable tool that helps them monitor their coding practice journey, identify patterns in their learning, and stay motivated through visual progress tracking.

**CodeTrack** addresses this gap by providing a comprehensive yet simple system to log coding problems, track practice sessions with timing, and generate insightful analytics about strengths, weaknesses, and progress trends.

---

## Scope of the Project

### In Scope:
- Problem library management (add, edit, delete, search, filter)
- Timed practice session tracking with notes
- Progress analytics and statistics
- Topic-based strength analysis
- Streak tracking and consistency monitoring
- Visual reports and charts
- Local data storage (JSON-based)
- Command-line interface for all operations
- Data export capabilities

### Out of Scope:
- Integration with actual coding platforms (LeetCode API, etc.)
- Online synchronization or cloud storage
- Multi-user support or authentication
- Running/testing code within the application
- Auto-grading or solution verification
- Mobile application version
- Real-time collaboration features

---

## Target Users

### Primary Users:
1. **Computer Science Students** - Preparing for placements and coding interviews
2. **Competitive Programmers** - Training for contests and improving problem-solving skills
3. **Self-Learners** - Building programming skills through structured practice

### User Characteristics:
- Basic familiarity with command-line interfaces
- Regular practice on coding problem platforms
- Need for systematic progress tracking
- Goal-oriented learners who value metrics and insights

---

## High-Level Features

### 1. Problem Library Management
- Store problems with metadata (title, difficulty, platform, topics, URL)
- Categorize by difficulty: Easy, Medium, Hard
- Tag with multiple topics (Arrays, DP, Graphs, etc.)
- Track status: Not Started, In Progress, Solved, Reviewed
- Search and filter by any attribute
- Bulk import/export functionality

### 2. Practice Session Tracking
- Start timed sessions for specific problems
- Pause and resume capability
- Add approach notes and thought process
- Progressive hints system (reveal hints one by one)
- Store solution code snippets
- Complete session history with timestamps

### 3. Analytics & Progress Dashboard
- **Core Statistics:**
  - Total problems solved
  - Current practice streak (consecutive days)
  - Average solve time by difficulty
  - Success rate per topic
  - Most/least practiced topics
  
- **Visual Analytics:**
  - Problems solved over time (line chart)
  - Difficulty distribution (pie chart)
  - Topic strength heatmap
  - Practice calendar (30-day view)
  - Time spent analysis

### 4. Data Management
- Reliable JSON-based local storage
- Automatic data backup
- Data validation and integrity checks
- Export reports to CSV/PDF
- Import problems from templates

---

## Expected Outcomes

Upon completion, users will be able to:
1. Systematically track all coding problems they attempt
2. Gain insights into their learning patterns and weak areas
3. Maintain motivation through streak tracking and visual progress
4. Make data-driven decisions about what to practice next
5. Review past problems and solutions efficiently
6. Export and share progress reports

This project demonstrates practical application of:
- Data structure design and management
- File I/O operations
- Algorithm implementation (search, filter, sort)
- Time-based calculations
- Data visualization
- Modular software design
- User interface design principles
