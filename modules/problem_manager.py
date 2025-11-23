import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.absath(__file__))))
from utils.data_handler import read_json, write_json

class Problem:
    def __init__(self, id, title, difficulty, topics = None, platform = "", url = "", status = "Not Started"):
        self.id = id
        self.title = title
        self.difficulty = difficulty
        self.topics = topics if topics else []
        self.platform = platform
        self.status = status
        self.date_added = datetime.now().isoformat()
        self.date_modified = datetime.now().isoformat

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'difficulty': self.difficulty,
            'topics': self.topics,
            'platform': self.platform,
            'url': self.url,
            'status': self.status,
            'date_added': self.date_added,
            'date_modified': self.date_modified
        }
    def from_dict(cls, data):
        problem = cls(
            id=data['id'],
            title=data['title'],
            difficulty=data['difficulty'],
            topics=data.get('topics', []),
            platform=data.get('platform', ''),
            url=data.get('url', ''),
            status=data.get('status', 'Not Started')
        )

    def __str__(self):
        return f"[{self.id}] {self.title} ({self.difficulty}) - {self.status}"

    def __repr__(self):
        return f"Problem(id={self.id}, title='{self.title}', difficulty='{self.difficulty}')"
    
class ProblemManager:
    def __init__(self, data_file='data/problems.json'):
        self.data_file = data_file
        self.problems = []
        self.load_problems()

    def load_problems(self):
        data = [problem.to_dict() for problem in self.problems]
        write_json(self.data_file, data)

    def add_problem(self, title, difficulty, topics=None, platform ="", url =""):
        if not self.problems:
            new_id = 1
        else:
            new_id = max(p.id for p in self.problems)+1

        new_problem = Problem(
            id=new_id,
            title=title,
            difficulty=difficulty,
            topics=topics,
            platform=platform,
            url=url,
            status="Not Started"
        )
        
        self.problems.append(new_problem)
        self.save_problems()

        return new_problem
    
    def get_problem(self, problem_id):
        for problem in self.problems:
            if problem.id == problem_id:
                return problem
            
        return None
    
    def edit_problem(self, problem_id, **updates):
        if not problem:
            return False
        
        for key, value in updates.items():
            if hasattr(problem, key):
                setattr(problem, key, value)

        problem.date_modified = datetime.now().isoformat()
        
        self.save_problems()
        
        return True
    
    def delete_problem(self, problem_id):
        if not problem:
            return False
        
        self.problems.remove(problem)
        self.save_problems()
        
        return True
    
    def list_problems(self, sort_by='date_added'):
        if sort_by == 'date_added':
            return sorted(self.problems, key=lambda p: p.date_added, reverse=True)
        elif sort_by == 'difficulty':
            order = {'Easy': 1, 'Medium': 2, 'Hard': 3}
            return sorted(self.problems, key=lambda p: order.get(p.difficulty, 0))
        elif sort_by == 'title':
            return sorted(self.problems, key=lambda p: p.title.lower())
        elif sort_by == 'status':
            order = {'Not Started': 1, 'In Progress': 2, 'Solved': 3, 'Reviewed': 4}
            return sorted(self.problems, key=lambda p: order.get(p.status, 0))
        else:
            return self.problems

    def filter_problems(self, difficulty=None, status=None, topics=None):
        if difficulty:
            results = [p for p in results if p.difficulty == difficulty]
        if status:
            results = [p for p in results if p.status == status]
        if topics:
            results = [p for p in results 
                      if any(topic in p.topics for topic in topics)]

        return results

    def get_statistics(self):
        total = len(self.problems)
        solved = len([p for p in self.problems if p.status == 'Solved'])
        in_progress = len([p for p in self.problems if p.status == 'In Progress'])
        not_started = len([p for p in self.problems if p.status == 'Not Started'])
        reviewed = len([p for p in self.problems if p.status == 'Reviewed'])
        
        return {
            'total': total,
            'solved': solved,
            'in_progress': in_progress,
            'not_started': not_started,
            'reviewed': reviewed,
            'completion_rate': (solved / total * 100) if total > 0 else 0
        }
