import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_handler import read_json, write_json

class Session:

    def__init__(self, session_id, problem_id):
        self.id = session_id
        self.problem_id = problem_id
        self.start_time = None
        self.end_time = None
        self.duration_seconds = 0
        self.pauses = []
        self.solved = False
        self.hints_used = 0
        self.notes = []
        self.solution_code = ""
    def to_dict(self):
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
    def from_dict(cls, data):
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
        status = "Solved" if self.solved else "Attempted"
        duration_min = self.duration_seconds // 60
        return f"Session {self.id} - Problem {self.problem_id} ({status}) - {duration_min}m"

    def __repr__(self):
        return f"Session(id={self.id}, problem_id={self.problem_id}, solved={self.solved})"

class SessionTracker:
    def __init__(self, data_file='data/sessions.json'):
        self.data_file = data_file
        self.sessions = []
        self.active_session = None
        self.load_sessions()

    def load_sessions(self):
        data = [session.to_dict() for session in self.sessions]
        write_json(self.data_file, data)

    def save_sessions(self):
        data = read_json(self.data_file)
        self.sessions = [Session.from_dict(s) for s in data]

    def save_sessions(self):
        data = [session.to_dict() for session in self.sessions]
        write_json(self.data_file, data)

    def start_session(self, problem_id):
        if self.active_session:
            return None

        if not self.sessions:
            new_id = 1
        else:
            new_id = max(s.id for s in self.sessions) + 1

        session = Session(new_id, problem_id)
        session.start_time = datetime.now().isoformat()

        self.active_session = session

        return session

    def get_active_session(self):
        return self.active_session

    def pause_session(self):
        if not self.active_session:
            return False

        if self.active_session.pauses and self.active_session.pauses[-1]['resume_time'] is None:
            return False

        pause_time = datetime.now().isoformat()
        self.active_session.pauses.append(
         {
             'pause_time': pause_time
             'resume_time': None
         }   
        )

        return True

    def resume_session(self):
        if not self.active_session:
            return False
        
        for pause in reversed(self.active_session.pauses):
            if pause['resume_time'] is None:
                pause['resume_time'] = datetime.now().isoformat()
                return True

        return False

    def is_paused(self):
        if not self.active_session:
            return False
        
        if not self.active_session.pauses:
            return False

        return self.active_session.pauses[-1]['resume_time'] is None

    def add_note(self, text):
        if not self.active_session:
            return False
        
        note = {
            'timestamp': datetime.now().isoformat(),
            'text': text
        }
        
        self.active_session.notes.append(note)
        
        return True

    def add_hint(self):
        if not self.active_session:
            return False
        
        self.active_session.hints_used += 1
        return True

    def calculate_duration(self, session):
        if not session.start_time or not session.end_time:
            return 0

        start = datetime.fromisoformat(session.start_time)
        end = datetime.fromisoformat(session.end_time)

        total_seconds = (end - start).total_seconds()

        pause_seconds = 0
        for pause in session.pauses:
            if pause['resume_time']:
                pause_start = datetime.fromisoformat(pause['pause_time'])
                pause_end = datetime.fromisoformat(pause['resume_time'])
                pause_seconds += (pause_end - pause_start).total_seconds()

        work_seconds = total_seconds - pause_seconds
        
        return int(work_seconds)

    def get_elapsed_time(self):
        if not self.active_session:
            return 0

        temp_session = Session(0, 0)
        temp_session.start_time = self.active_session.start_time
        temp_session.end_time = datetime.now().isoformat()
        temp_session.pauses = self.active_session.pauses.copy()

        if self.is_paused():
            temp_session.pauses[-1]['resume_time'] = datetime.now().isoformat()
        
        return self.calculate_duration(temp_session)

    def complete_session(self, solved=False, solution_code=''):
        if not self.active_session:
            return False
        
        self.active_session.end_time = datetime.now().isoformat()
        
        if self.is_paused():
            self.resume_session()

        self.active_session.solved = solved
        self.active_session.solution_code = solution_code
        duration = self.calculate_duration(self.active_session)
        self.active_session.duration_seconds = duration
        self.sessions.append(self.active_session)
        self.active_session = None
        self.save_sessions()

        return True

    def cancel_session(self):
        if not self.active_session:
            return False
        
        self.active_session = None
        return True

    def get_session_history(self, problem_id=None):
        if problem_id is None:
            return self.sessions
        else:
            return [s for s in self.sessions if s.problem_id == problem_id]

    def get_session_by_id(self, session_id):
        for session in self.sessions:
            if session.id == session_id:
                return session
        return None

    def get_statistics(self):
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
