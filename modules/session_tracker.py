"""
Session Tracker Module
Handles practice session tracking with timer, notes, and history
"""

from datetime import datetime
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_handler import read_json, write_json


class Session:
    """Represents a single practice session"""
    
    def __init__(self, session_id, problem_id):
        self.id = session_id
        self.problem_id = problem_id
        self.start_time = None
        self.end_time = None
        self.duration_seconds = 0
        self.pauses = []  # List of {pause_time, resume_time}
        self.solved = False
        self.hints_used = 0
        self.notes = []  # List of {timestamp, text}
        self.solution_code = ""
    
    def to_dict(self):
        """Convert Session object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration_seconds': self.duration_seconds,
            'pauses': self.pauses,
            'solved': self.solved,
            'hints_used': self.hints_used,
            'notes': self.notes,
            'solution_code': self.solution_code
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Session object from dictionary"""
        session = cls(
            session_id=data['id'],
            problem_id=data['problem_id']
        )
        session.start_time = data.get('start_time')
        session.end_time = data.get('end_time')
        session.duration_seconds = data.get('duration_seconds', 0)
        session.pauses = data.get('pauses', [])
        session.solved = data.get('solved', False)
        session.hints_used = data.get('hints_used', 0)
        session.notes = data.get('notes', [])
        session.solution_code = data.get('solution_code', '')
        return session
    
    def __str__(self):
        """String representation for printing"""
        status = "Solved" if self.solved else "Attempted"
        duration_min = self.duration_seconds // 60
        return f"Session {self.id} - Problem {self.problem_id} ({status}) - {duration_min}m"
    
    def __repr__(self):
        """Official string representation"""
        return f"Session(id={self.id}, problem_id={self.problem_id}, solved={self.solved})"


class SessionTracker:
    """Manages all practice sessions"""
    
    def __init__(self, data_file='data/sessions.json'):
        self.data_file = data_file
        self.sessions = []  # All completed sessions
        self.active_session = None  # Currently running session
        self.load_sessions()
    
    def load_sessions(self):
        """Load sessions from JSON file into memory"""
        data = read_json(self.data_file)
        self.sessions = [Session.from_dict(s) for s in data]
    
    def save_sessions(self):
        """Save sessions from memory to JSON file"""
        data = [session.to_dict() for session in self.sessions]
        write_json(self.data_file, data)
    
    def start_session(self, problem_id):
        """
        Start a new practice session
        
        Args:
            problem_id (int): ID of the problem to practice
        
        Returns:
            Session: The newly created session
        """
        # Check if there's already an active session
        if self.active_session:
            return None  # Can't start new session while one is active
        
        # Generate new session ID
        if not self.sessions:
            new_id = 1
        else:
            new_id = max(s.id for s in self.sessions) + 1
        
        # Create new session
        session = Session(new_id, problem_id)
        session.start_time = datetime.now().isoformat()
        
        # Set as active session
        self.active_session = session
        
        return session
    
    def get_active_session(self):
        """
        Get the currently active session
        
        Returns:
            Session or None: Active session if exists
        """
        return self.active_session
    
    def pause_session(self):
        """
        Pause the currently active session
        
        Returns:
            bool: True if successful, False if no active session
        """
        if not self.active_session:
            return False
        
        # Check if already paused
        if self.active_session.pauses and self.active_session.pauses[-1]['resume_time'] is None:
            return False  # Already paused
        
        # Record pause time
        pause_time = datetime.now().isoformat()
        self.active_session.pauses.append({
            'pause_time': pause_time,
            'resume_time': None
        })
        
        return True
    
    def resume_session(self):
        """
        Resume the paused session
        
        Returns:
            bool: True if successful, False if not paused
        """
        if not self.active_session:
            return False
        
        # Find the last pause that hasn't been resumed
        for pause in reversed(self.active_session.pauses):
            if pause['resume_time'] is None:
                pause['resume_time'] = datetime.now().isoformat()
                return True
        
        return False  # No paused session to resume
    
    def is_paused(self):
        """
        Check if active session is currently paused
        
        Returns:
            bool: True if paused, False otherwise
        """
        if not self.active_session:
            return False
        
        if not self.active_session.pauses:
            return False
        
        # Check if last pause has no resume time
        return self.active_session.pauses[-1]['resume_time'] is None
    
    def add_note(self, text):
        """
        Add a note to the active session
        
        Args:
            text (str): Note text
        
        Returns:
            bool: True if successful, False if no active session
        """
        if not self.active_session:
            return False
        
        note = {
            'timestamp': datetime.now().isoformat(),
            'text': text
        }
        
        self.active_session.notes.append(note)
        
        return True
    
    def add_hint(self):
        """
        Increment hints used for active session
        
        Returns:
            bool: True if successful, False if no active session
        """
        if not self.active_session:
            return False
        
        self.active_session.hints_used += 1
        return True
    
    def calculate_duration(self, session):
        """
        Calculate actual work time excluding pauses
        
        Args:
            session (Session): Session to calculate duration for
        
        Returns:
            int: Duration in seconds
        """
        if not session.start_time or not session.end_time:
            return 0
        
        # Convert ISO strings to datetime objects
        start = datetime.fromisoformat(session.start_time)
        end = datetime.fromisoformat(session.end_time)
        
        # Total elapsed time
        total_seconds = (end - start).total_seconds()
        
        # Subtract pause durations
        pause_seconds = 0
        for pause in session.pauses:
            if pause['resume_time']:
                pause_start = datetime.fromisoformat(pause['pause_time'])
                pause_end = datetime.fromisoformat(pause['resume_time'])
                pause_seconds += (pause_end - pause_start).total_seconds()
        
        # Actual work time
        work_seconds = total_seconds - pause_seconds
        
        return int(work_seconds)
    
    def get_elapsed_time(self):
        """
        Get elapsed time for active session (excluding pauses)
        
        Returns:
            int: Elapsed seconds, or 0 if no active session
        """
        if not self.active_session:
            return 0
        
        # Create temporary end time (now)
        temp_session = Session(0, 0)
        temp_session.start_time = self.active_session.start_time
        temp_session.end_time = datetime.now().isoformat()
        temp_session.pauses = self.active_session.pauses.copy()
        
        # If currently paused, close the pause temporarily
        if self.is_paused():
            temp_session.pauses[-1]['resume_time'] = datetime.now().isoformat()
        
        return self.calculate_duration(temp_session)
    
    def complete_session(self, solved=False, solution_code=""):
        """
        Complete and save the active session
        
        Args:
            solved (bool): Whether the problem was solved
            solution_code (str): Solution code (optional)
        
        Returns:
            bool: True if successful, False if no active session
        """
        if not self.active_session:
            return False
        
        # Set end time
        self.active_session.end_time = datetime.now().isoformat()
        
        # If paused, auto-resume before completing
        if self.is_paused():
            self.resume_session()
        
        # Set solved status and solution
        self.active_session.solved = solved
        self.active_session.solution_code = solution_code
        
        # Calculate duration
        duration = self.calculate_duration(self.active_session)
        self.active_session.duration_seconds = duration
        
        # Add to sessions list
        self.sessions.append(self.active_session)
        
        # Clear active session
        self.active_session = None
        
        # Save to file
        self.save_sessions()
        
        return True
    
    def cancel_session(self):
        """
        Cancel the active session without saving
        
        Returns:
            bool: True if successful, False if no active session
        """
        if not self.active_session:
            return False
        
        self.active_session = None
        return True
    
    def get_session_history(self, problem_id=None):
        """
        Get session history, optionally filtered by problem
        
        Args:
            problem_id (int, optional): Filter by problem ID
        
        Returns:
            list: List of Session objects
        """
        if problem_id is None:
            return self.sessions
        else:
            return [s for s in self.sessions if s.problem_id == problem_id]
    
    def get_session_by_id(self, session_id):
        """
        Get a specific session by ID
        
        Args:
            session_id (int): Session ID
        
        Returns:
            Session or None: The session if found
        """
        for session in self.sessions:
            if session.id == session_id:
                return session
        return None
    
    def get_statistics(self):
        """
        Get statistics about all sessions
        
        Returns:
            dict: Statistics dictionary
        """
        total_sessions = len(self.sessions)
        solved_sessions = len([s for s in self.sessions if s.solved])
        
        total_time = sum(s.duration_seconds for s in self.sessions)
        avg_time = (total_time / total_sessions) if total_sessions > 0 else 0
        
        total_hints = sum(s.hints_used for s in self.sessions)
        
        return {
            'total_sessions': total_sessions,
            'solved_sessions': solved_sessions,
            'success_rate': (solved_sessions / total_sessions * 100) if total_sessions > 0 else 0,
            'total_time_seconds': total_time,
            'average_time_seconds': int(avg_time),
            'total_hints_used': total_hints
        }


# Test code
if __name__ == "__main__":
    tracker = SessionTracker()
    
    print("Starting session for problem 1...")
    session = tracker.start_session(1)
    print(f"Session started: {session}")
    
    import time
    time.sleep(2)
    
    print("\nAdding note...")
    tracker.add_note("Using hash map approach")
    
    print("Pausing session...")
    tracker.pause_session()
    time.sleep(1)
    
    print("Resuming session...")
    tracker.resume_session()
    time.sleep(2)
    
    print("\nAdding another note...")
    tracker.add_note("Found the solution!")
    
    print("Adding hint...")
    tracker.add_hint()
    
    print(f"\nElapsed time: {tracker.get_elapsed_time()} seconds")
    
    print("\nCompleting session...")
    tracker.complete_session(
        solved=True,
        solution_code="def solution():\n    return 42"
    )
    
    print("\nSession history:")
    for s in tracker.get_session_history():
        print(f"  {s}")
    
    print("\nStatistics:")
    stats = tracker.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
