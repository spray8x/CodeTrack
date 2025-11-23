from datetime import datetime, timedelta
from collections import defaultdict
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Analytics:
    
    def __init__(self, problem_manager, session_tracker):
        self.problem_manager = problem_manager
        self.session_tracker = session_tracker
        self.problems = problem_manager.problems
        self.sessions = session_tracker.sessions
    
    def calculate_statistics(self):
        problem_stats = self.problem_manager.get_statistics()
        session_stats = self.session_tracker.get_statistics()
        streak = self.calculate_streak()
        longest_streak = self.calculate_longest_streak()
        
        return {
            'total_problems': problem_stats['total'],
            'total_solved': problem_stats['solved'],
            'total_in_progress': problem_stats['in_progress'],
            'total_not_started': problem_stats['not_started'],
            'completion_rate': problem_stats['completion_rate'],
            'total_sessions': session_stats['total_sessions'],
            'solved_sessions': session_stats['solved_sessions'],
            'session_success_rate': session_stats['success_rate'],
            'total_practice_time': session_stats['total_time_seconds'],
            'average_session_time': session_stats['average_time_seconds'],
            'total_hints_used': session_stats['total_hints_used'],
            'current_streak': streak,
            'longest_streak': longest_streak
        }
    
    def calculate_streak(self):
        if not self.sessions:
            return 0
        
        dates = set()
        for session in self.sessions:
            date = session.start_time.split('T')[0]
            dates.add(date)
        
        sorted_dates = sorted(dates, reverse=True)
        today = datetime.now().date()
        streak = 0
        
        for i in range(len(sorted_dates)):
            date = datetime.fromisoformat(sorted_dates[i]).date()
            expected_date = today - timedelta(days=i)
            
            if date == expected_date:
                streak += 1
            else:
                break
        
        return streak
    
    def calculate_longest_streak(self):
        if not self.sessions:
            return 0
        
        dates = set()
        for session in self.sessions:
            date = session.start_time.split('T')[0]
            dates.add(date)
        
        sorted_dates = sorted(dates)
        
        if not sorted_dates:
            return 0
        
        longest = 1
        current = 1
        
        for i in range(1, len(sorted_dates)):
            prev_date = datetime.fromisoformat(sorted_dates[i-1]).date()
            curr_date = datetime.fromisoformat(sorted_dates[i]).date()
            
            if (curr_date - prev_date).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        return longest
    
    def get_topic_analysis(self):
        topic_stats = {}
        
        for problem in self.problems:
            for topic in problem.topics:
                if topic not in topic_stats:
                    topic_stats[topic] = {'total': 0, 'solved': 0, 'success_rate': 0}
                
                topic_stats[topic]['total'] += 1
                
                if problem.status == 'Solved' or problem.status == 'Reviewed':
                    topic_stats[topic]['solved'] += 1
        
        for topic, stats in topic_stats.items():
            if stats['total'] > 0:
                stats['success_rate'] = stats['solved'] / stats['total']
            else:
                stats['success_rate'] = 0
        
        return topic_stats
    
    def get_difficulty_analysis(self):
        diff_stats = {
            'Easy': {'total': 0, 'solved': 0, 'total_time': 0, 'count': 0, 'avg_time': 0},
            'Medium': {'total': 0, 'solved': 0, 'total_time': 0, 'count': 0, 'avg_time': 0},
            'Hard': {'total': 0, 'solved': 0, 'total_time': 0, 'count': 0, 'avg_time': 0}
        }
        
        for problem in self.problems:
            diff = problem.difficulty
            diff_stats[diff]['total'] += 1
            
            if problem.status == 'Solved' or problem.status == 'Reviewed':
                diff_stats[diff]['solved'] += 1
        
        for session in self.sessions:
            if session.solved:
                problem = self.problem_manager.get_problem(session.problem_id)
                if problem:
                    diff = problem.difficulty
                    diff_stats[diff]['total_time'] += session.duration_seconds
                    diff_stats[diff]['count'] += 1
        
        for diff, stats in diff_stats.items():
            if stats['count'] > 0:
                stats['avg_time'] = stats['total_time'] // stats['count']
            else:
                stats['avg_time'] = 0
        
        return diff_stats
    
    def get_practice_calendar(self, days=30):
        calendar = {}
        today = datetime.now().date()
        
        for i in range(days):
            date = (today - timedelta(days=i)).isoformat()
            calendar[date] = 0
        
        for session in self.sessions:
            date = session.start_time.split('T')[0]
            if date in calendar:
                calendar[date] += 1
        
        return calendar
    
    def get_weak_topics(self, threshold=0.5):
        topic_stats = self.get_topic_analysis()
        weak = [(topic, stats) for topic, stats in topic_stats.items() 
                if stats['success_rate'] < threshold and stats['total'] > 0]
        
        weak.sort(key=lambda x: x[1]['success_rate'])
        
        return weak
    
    def get_strong_topics(self, threshold=0.7):
        topic_stats = self.get_topic_analysis()
        strong = [(topic, stats) for topic, stats in topic_stats.items() 
                  if stats['success_rate'] >= threshold and stats['total'] > 0]
        
        strong.sort(key=lambda x: x[1]['success_rate'], reverse=True)
        
        return strong
    
    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
    
    def draw_ascii_bar(self, value, max_value, width=40):
        if max_value == 0:
            return ''
        
        filled = int((value / max_value) * width)
        bar = '█' * filled + '░' * (width - filled)
        return bar
    
    def display_statistics(self):
        stats = self.calculate_statistics()
        
        print("\n" + "="*60)
        print("CODETRACK STATISTICS".center(60))
        print("="*60)
        
        print("\nProblem Statistics:")
        print(f"  Total Problems:      {stats['total_problems']}")
        print(f"  Solved:              {stats['total_solved']} ({stats['completion_rate']:.1f}%)")
        print(f"  In Progress:         {stats['total_in_progress']}")
        print(f"  Not Started:         {stats['total_not_started']}")
        
        print("\nPractice Statistics:")
        print(f"  Total Sessions:      {stats['total_sessions']}")
        print(f"  Successful Sessions: {stats['solved_sessions']} ({stats['session_success_rate']:.1f}%)")
        print(f"  Total Practice Time: {self.format_time(stats['total_practice_time'])}")
        print(f"  Avg Session Time:    {self.format_time(stats['average_session_time'])}")
        print(f"  Hints Used:          {stats['total_hints_used']}")
        
        print("\nStreak Information:")
        print(f"  Current Streak:      {stats['current_streak']} days")
        print(f"  Longest Streak:      {stats['longest_streak']} days")
        
        print("="*60 + "\n")
    
    def display_difficulty_chart(self):
        diff_stats = self.get_difficulty_analysis()
        
        print("\n" + "="*60)
        print("DIFFICULTY DISTRIBUTION".center(60))
        print("="*60 + "\n")
        
        max_total = max(stats['total'] for stats in diff_stats.values())
        
        for difficulty in ['Easy', 'Medium', 'Hard']:
            stats = diff_stats[difficulty]
            bar = self.draw_ascii_bar(stats['total'], max_total, 30)
            
            print(f"{difficulty:8} [{bar}] {stats['total']} problems")
            print(f"          Solved: {stats['solved']}/{stats['total']}", end='')
            
            if stats['total'] > 0:
                success_rate = (stats['solved'] / stats['total']) * 100
                print(f" ({success_rate:.1f}%)", end='')
            
            if stats['avg_time'] > 0:
                print(f" | Avg Time: {self.format_time(stats['avg_time'])}")
            else:
                print()
            print()
        
        print("="*60 + "\n")
    
    def display_topic_chart(self):
        topic_stats = self.get_topic_analysis()
        
        if not topic_stats:
            print("\nNo topic data available yet.\n")
            return
        
        print("\n" + "="*60)
        print("TOPIC SUCCESS RATES".center(60))
        print("="*60 + "\n")
        
        sorted_topics = sorted(topic_stats.items(), 
                              key=lambda x: x[1]['success_rate'], 
                              reverse=True)
        
        max_rate = 1.0
        
        for topic, stats in sorted_topics:
            rate = stats['success_rate']
            bar = self.draw_ascii_bar(rate, max_rate, 30)
            percentage = rate * 100
            
            print(f"{topic:20} [{bar}] {percentage:5.1f}%")
            print(f"{'':22} {stats['solved']}/{stats['total']} solved")
            print()
        
        print("="*60 + "\n")
    
    def display_practice_calendar(self, days=14):
        calendar = self.get_practice_calendar(days)
        
        print("\n" + "="*60)
        print(f"PRACTICE CALENDAR (Last {days} days)".center(60))
        print("="*60 + "\n")
        
        sorted_dates = sorted(calendar.keys())
        
        max_sessions = max(calendar.values()) if calendar.values() else 1
        
        for date in sorted_dates:
            count = calendar[date]
            
            date_obj = datetime.fromisoformat(date)
            date_str = date_obj.strftime('%b %d')
            day_str = date_obj.strftime('%a')
            
            if count > 0:
                bar = '█' * count
                indicator = '+'
            else:
                bar = '-'
                indicator = ' '
            
            print(f"{indicator} {date_str} ({day_str:3}) {bar} ({count} sessions)")
        
        print("\n" + "="*60 + "\n")
    
    def display_weak_topics(self):
        weak = self.get_weak_topics(threshold=0.5)
        
        if not weak:
            print("\nNo weak topics! You're doing great!\n")
            return
        
        print("\n" + "="*60)
        print("TOPICS NEEDING PRACTICE".center(60))
        print("="*60 + "\n")
        
        for topic, stats in weak[:5]:
            rate = stats['success_rate'] * 100
            print(f"[!] {topic}")
            print(f"    Success Rate: {rate:.1f}% ({stats['solved']}/{stats['total']} solved)")
            print(f"    Recommendation: Practice {stats['total'] - stats['solved']} more problems")
            print()
        
        print("="*60 + "\n")
    
    def display_strong_topics(self):
        strong = self.get_strong_topics(threshold=0.7)
        
        if not strong:
            print("\nKeep practicing to build your strengths!\n")
            return
        
        print("\n" + "="*60)
        print("YOUR STRONG TOPICS".center(60))
        print("="*60 + "\n")
        
        for topic, stats in strong[:5]:
            rate = stats['success_rate'] * 100
            print(f"[*] {topic}")
            print(f"    Success Rate: {rate:.1f}% ({stats['solved']}/{stats['total']} solved)")
            print()
        
        print("="*60 + "\n")
    
    def generate_full_report(self):
        print("\n" + "="*60)
        print("CODETRACK ANALYTICS REPORT".center(60))
        print("="*60)
        
        self.display_statistics()
        self.display_difficulty_chart()
        self.display_topic_chart()
        self.display_practice_calendar(14)
        self.display_strong_topics()
        self.display_weak_topics()
        
        print("\n" + "="*60)
        print("Report generated at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("="*60 + "\n")


if __name__ == "__main__":
    from problem_manager import ProblemManager
    from session_tracker import SessionTracker
    
    pm = ProblemManager()
    st = SessionTracker()
    
    analytics = Analytics(pm, st)
    
    analytics.generate_full_report()
