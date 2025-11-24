"""
Problem Manager Module
Handles CRUD operations for coding problems
"""

from datetime import datetime
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_handler import read_json, write_json


class Problem:
    """Represents a single coding problem"""
    
    def __init__(self, id, title, difficulty, topics=None, platform="", url="", status="Not Started"):
        self.id = id
        self.title = title
        self.difficulty = difficulty  # Easy, Medium, Hard
        self.topics = topics if topics else []
        self.platform = platform
        self.url = url
        self.status = status  # Not Started, In Progress, Solved, Reviewed
        self.date_added = datetime.now().isoformat()
        self.date_modified = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert Problem object to dictionary for JSON serialization"""
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
    
    @classmethod
    def from_dict(cls, data):
        """Create Problem object from dictionary"""
        problem = cls(
            id=data['id'],
            title=data['title'],
            difficulty=data['difficulty'],
            topics=data.get('topics', []),
            platform=data.get('platform', ''),
            url=data.get('url', ''),
            status=data.get('status', 'Not Started')
        )
        # Restore original timestamps
        problem.date_added = data.get('date_added', problem.date_added)
        problem.date_modified = data.get('date_modified', problem.date_modified)
        return problem
    
    def __str__(self):
        """String representation for printing"""
        return f"[{self.id}] {self.title} ({self.difficulty}) - {self.status}"
    
    def __repr__(self):
        """Official string representation"""
        return f"Problem(id={self.id}, title='{self.title}', difficulty='{self.difficulty}')"


class ProblemManager:
    """Manages the collection of all coding problems"""
    
    def __init__(self, data_file='data/problems.json'):
        self.data_file = data_file
        self.problems = []
        self.load_problems()
    
    def load_problems(self):
        """Load problems from JSON file into memory"""
        data = read_json(self.data_file)
        self.problems = [Problem.from_dict(p) for p in data]
    
    def save_problems(self):
        """Save problems from memory to JSON file"""
        data = [problem.to_dict() for problem in self.problems]
        write_json(self.data_file, data)
    
    def add_problem(self, title, difficulty, topics=None, platform="", url=""):
        """
        Add a new problem to the library
        
        Args:
            title (str): Problem title
            difficulty (str): Easy, Medium, or Hard
            topics (list): List of topic tags
            platform (str): Platform name (LeetCode, HackerRank, etc.)
            url (str): Problem URL
        
        Returns:
            Problem: The newly created problem
        """
        # Generate new ID
        if not self.problems:
            new_id = 1
        else:
            new_id = max(p.id for p in self.problems) + 1
        
        # Create new problem
        new_problem = Problem(
            id=new_id,
            title=title,
            difficulty=difficulty,
            topics=topics,
            platform=platform,
            url=url,
            status="Not Started"
        )
        
        # Add to list and save
        self.problems.append(new_problem)
        self.save_problems()
        
        return new_problem
    
    def get_problem(self, problem_id):
        """
        Get a problem by ID
        
        Args:
            problem_id (int): Problem ID
        
        Returns:
            Problem or None: The problem if found, None otherwise
        """
        for problem in self.problems:
            if problem.id == problem_id:
                return problem
        return None
    
    def edit_problem(self, problem_id, **updates):
        """
        Edit an existing problem
        
        Args:
            problem_id (int): Problem ID to edit
            **updates: Keyword arguments of fields to update
        
        Returns:
            bool: True if successful, False if problem not found
        """
        problem = self.get_problem(problem_id)
        
        if not problem:
            return False
        
        # Update fields
        for key, value in updates.items():
            if hasattr(problem, key):
                setattr(problem, key, value)
        
        # Update modified timestamp
        problem.date_modified = datetime.now().isoformat()
        
        # Save changes
        self.save_problems()
        
        return True
    
    def delete_problem(self, problem_id):
        """
        Delete a problem from the library
        
        Args:
            problem_id (int): Problem ID to delete
        
        Returns:
            bool: True if successful, False if problem not found
        """
        problem = self.get_problem(problem_id)
        
        if not problem:
            return False
        
        self.problems.remove(problem)
        self.save_problems()
        
        return True
    
    def list_problems(self, sort_by='date_added'):
        """
        List all problems with optional sorting
        
        Args:
            sort_by (str): Sort key - 'date_added', 'difficulty', 'title', 'status'
        
        Returns:
            list: List of Problem objects
        """
        if sort_by == 'date_added':
            return sorted(self.problems, key=lambda p: p.date_added, reverse=True)
        elif sort_by == 'difficulty':
            # Custom order: Easy -> Medium -> Hard
            order = {'Easy': 1, 'Medium': 2, 'Hard': 3}
            return sorted(self.problems, key=lambda p: order.get(p.difficulty, 0))
        elif sort_by == 'title':
            return sorted(self.problems, key=lambda p: p.title.lower())
        elif sort_by == 'status':
            # Custom order: Not Started -> In Progress -> Solved -> Reviewed
            order = {'Not Started': 1, 'In Progress': 2, 'Solved': 3, 'Reviewed': 4}
            return sorted(self.problems, key=lambda p: order.get(p.status, 0))
        else:
            return self.problems
    
    def search_problems(self, query):
        """
        Search problems by title (case-insensitive)
        
        Args:
            query (str): Search query
        
        Returns:
            list: List of matching Problem objects
        """
        query = query.lower()
        results = []
        
        for problem in self.problems:
            if query in problem.title.lower():
                results.append(problem)
        
        return results
    
    def filter_problems(self, difficulty=None, status=None, topics=None):
        """
        Filter problems by multiple criteria
        
        Args:
            difficulty (str): Filter by difficulty (Easy, Medium, Hard)
            status (str): Filter by status
            topics (list): Filter by topics (problem must have at least one)
        
        Returns:
            list: List of matching Problem objects
        """
        results = self.problems
        
        # Filter by difficulty
        if difficulty:
            results = [p for p in results if p.difficulty == difficulty]
        
        # Filter by status
        if status:
            results = [p for p in results if p.status == status]
        
        # Filter by topics
        if topics:
            results = [p for p in results 
                      if any(topic in p.topics for topic in topics)]
        
        return results
    
    def get_statistics(self):
        """
        Get basic statistics about problems
        
        Returns:
            dict: Statistics dictionary
        """
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
