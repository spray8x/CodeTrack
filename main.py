import sys
import os
import time
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.problem_manager import ProblemManager
from modules.session_tracker import SessionTracker
from modules.analytics import Analytics


def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header(title):
    print("\n" + "="*60)
    print(title.center(60))
    print("="*60 + "\n")


def pause():
    input("\nPress Enter to continue...")


def get_input(prompt, input_type=str, allow_empty=False):
    while True:
        try:
            value = input(prompt).strip()
            
            if not value and not allow_empty:
                print("Input cannot be empty. Try again.")
                continue
            
            if not value and allow_empty:
                return None
            
            if input_type == int:
                return int(value)
            elif input_type == float:
                return float(value)
            else:
                return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None


def problem_library_menu(pm):
    while True:
        clear_screen()
        print_header("PROBLEM LIBRARY")
        print("1. Add New Problem")
        print("2. View All Problems")
        print("3. Search Problems")
        print("4. Filter Problems")
        print("5. Edit Problem")
        print("6. Delete Problem")
        print("7. Back to Main Menu")
        
        choice = get_input("\nEnter choice: ", int, allow_empty=True)
        
        if choice == 1:
            add_problem(pm)
        elif choice == 2:
            view_all_problems(pm)
        elif choice == 3:
            search_problems(pm)
        elif choice == 4:
            filter_problems(pm)
        elif choice == 5:
            edit_problem(pm)
        elif choice == 6:
            delete_problem(pm)
        elif choice == 7:
            break


def add_problem(pm):
    clear_screen()
    print_header("ADD NEW PROBLEM")
    
    title = get_input("Problem Title: ")
    if not title:
        return
    
    print("\nDifficulty: 1) Easy  2) Medium  3) Hard")
    diff_choice = get_input("Select difficulty: ", int)
    difficulty_map = {1: "Easy", 2: "Medium", 3: "Hard"}
    difficulty = difficulty_map.get(diff_choice, "Medium")
    
    topics_str = get_input("Topics (comma-separated): ", allow_empty=True)
    topics = [t.strip() for t in topics_str.split(",")] if topics_str else []
    
    platform = get_input("Platform (e.g., LeetCode): ", allow_empty=True)
    url = get_input("Problem URL: ", allow_empty=True)
    
    problem = pm.add_problem(title, difficulty, topics, platform or "", url or "")
    
    print(f"\nProblem added successfully! ID: {problem.id}")
    pause()


def view_all_problems(pm):
    clear_screen()
    print_header("ALL PROBLEMS")
    
    problems = pm.list_problems()
    
    if not problems:
        print("No problems found.")
        pause()
        return
    
    print(f"{'ID':<5} {'Title':<30} {'Difficulty':<10} {'Status':<15}")
    print("-" * 60)
    
    for p in problems:
        print(f"{p.id:<5} {p.title[:29]:<30} {p.difficulty:<10} {p.status:<15}")
    
    print(f"\nTotal: {len(problems)} problems")
    pause()


def search_problems(pm):
    clear_screen()
    print_header("SEARCH PROBLEMS")
    
    query = get_input("Enter search term: ")
    if not query:
        return
    
    results = pm.search_problems(query)
    
    if not results:
        print(f"\nNo problems found matching '{query}'")
        pause()
        return
    
    print(f"\nFound {len(results)} problem(s):\n")
    
    for p in results:
        print(f"[{p.id}] {p.title}")
        print(f"    Difficulty: {p.difficulty} | Status: {p.status}")
        print(f"    Topics: {', '.join(p.topics)}")
        print()
    
    pause()


def filter_problems(pm):
    clear_screen()
    print_header("FILTER PROBLEMS")
    
    print("Filter by:")
    print("1. Difficulty")
    print("2. Status")
    print("3. Topic")
    print("4. Back")
    
    choice = get_input("\nSelect filter: ", int)
    
    difficulty = None
    status = None
    topics = None
    
    if choice == 1:
        print("\n1) Easy  2) Medium  3) Hard")
        diff_choice = get_input("Select difficulty: ", int)
        difficulty_map = {1: "Easy", 2: "Medium", 3: "Hard"}
        difficulty = difficulty_map.get(diff_choice)
    elif choice == 2:
        print("\n1) Not Started  2) In Progress  3) Solved  4) Reviewed")
        status_choice = get_input("Select status: ", int)
        status_map = {1: "Not Started", 2: "In Progress", 3: "Solved", 4: "Reviewed"}
        status = status_map.get(status_choice)
    elif choice == 3:
        topic = get_input("Enter topic: ")
        topics = [topic] if topic else None
    else:
        return
    
    results = pm.filter_problems(difficulty=difficulty, status=status, topics=topics)
    
    if not results:
        print("\nNo problems match the filter.")
        pause()
        return
    
    print(f"\nFound {len(results)} problem(s):\n")
    
    for p in results:
        print(f"[{p.id}] {p.title} - {p.difficulty} - {p.status}")
    
    pause()


def edit_problem(pm):
    clear_screen()
    print_header("EDIT PROBLEM")
    
    problem_id = get_input("Enter problem ID: ", int)
    if not problem_id:
        return
    
    problem = pm.get_problem(problem_id)
    if not problem:
        print(f"\nProblem with ID {problem_id} not found.")
        pause()
        return
    
    print(f"\nCurrent: {problem.title} - {problem.difficulty} - {problem.status}")
    print("\nWhat would you like to edit?")
    print("1. Status")
    print("2. Title")
    print("3. Difficulty")
    print("4. Cancel")
    
    choice = get_input("\nSelect option: ", int)
    
    if choice == 1:
        print("\n1) Not Started  2) In Progress  3) Solved  4) Reviewed")
        status_choice = get_input("New status: ", int)
        status_map = {1: "Not Started", 2: "In Progress", 3: "Solved", 4: "Reviewed"}
        new_status = status_map.get(status_choice)
        if new_status:
            pm.edit_problem(problem_id, status=new_status)
            print("\nStatus updated successfully!")
    elif choice == 2:
        new_title = get_input("New title: ")
        if new_title:
            pm.edit_problem(problem_id, title=new_title)
            print("\nTitle updated successfully!")
    elif choice == 3:
        print("\n1) Easy  2) Medium  3) Hard")
        diff_choice = get_input("New difficulty: ", int)
        difficulty_map = {1: "Easy", 2: "Medium", 3: "Hard"}
        new_diff = difficulty_map.get(diff_choice)
        if new_diff:
            pm.edit_problem(problem_id, difficulty=new_diff)
            print("\nDifficulty updated successfully!")
    
    pause()


def delete_problem(pm):
    clear_screen()
    print_header("DELETE PROBLEM")
    
    problem_id = get_input("Enter problem ID to delete: ", int)
    if not problem_id:
        return
    
    problem = pm.get_problem(problem_id)
    if not problem:
        print(f"\nProblem with ID {problem_id} not found.")
        pause()
        return
    
    print(f"\nAre you sure you want to delete: {problem.title}?")
    confirm = get_input("Type 'yes' to confirm: ")
    
    if confirm.lower() == 'yes':
        pm.delete_problem(problem_id)
        print("\nProblem deleted successfully!")
    else:
        print("\nDeletion cancelled.")
    
    pause()


def practice_session_menu(pm, st):
    while True:
        clear_screen()
        print_header("PRACTICE SESSION")
        
        active = st.get_active_session()
        
        if active:
            problem = pm.get_problem(active.problem_id)
            elapsed = st.get_elapsed_time()
            minutes = elapsed // 60
            seconds = elapsed % 60
            
            print(f"Active Session: {problem.title if problem else 'Unknown'}")
            print(f"Elapsed Time: {minutes}m {seconds}s")
            print(f"Status: {'PAUSED' if st.is_paused() else 'RUNNING'}")
            print()
            print("1. Pause Session" if not st.is_paused() else "1. Resume Session")
            print("2. Add Note")
            print("3. Add Hint Used")
            print("4. Complete Session")
            print("5. Cancel Session")
        else:
            print("No active session.")
            print()
            print("1. Start New Session")
            print("2. View Session History")
        
        print("6. Back to Main Menu")
        
        choice = get_input("\nEnter choice: ", int, allow_empty=True)
        
        if active:
            if choice == 1:
                if st.is_paused():
                    st.resume_session()
                    print("\nSession resumed!")
                else:
                    st.pause_session()
                    print("\nSession paused!")
                time.sleep(1)
            elif choice == 2:
                note = get_input("Enter note: ")
                if note:
                    st.add_note(note)
                    print("\nNote added!")
                    time.sleep(1)
            elif choice == 3:
                st.add_hint()
                print("\nHint recorded!")
                time.sleep(1)
            elif choice == 4:
                complete_session(pm, st)
            elif choice == 5:
                confirm = get_input("Cancel session? (yes/no): ")
                if confirm.lower() == 'yes':
                    st.cancel_session()
                    print("\nSession cancelled.")
                    time.sleep(1)
            elif choice == 6:
                if get_input("Exit with active session? (yes/no): ").lower() == 'yes':
                    break
        else:
            if choice == 1:
                start_session(pm, st)
            elif choice == 2:
                view_session_history(st, pm)
            elif choice == 6:
                break


def start_session(pm, st):
    clear_screen()
    print_header("START PRACTICE SESSION")
    
    problems = pm.list_problems()
    
    if not problems:
        print("No problems available. Add some problems first!")
        pause()
        return
    
    print("Available problems:\n")
    for p in problems:
        print(f"[{p.id}] {p.title} - {p.difficulty} - {p.status}")
    
    problem_id = get_input("\nEnter problem ID: ", int)
    if not problem_id:
        return
    
    problem = pm.get_problem(problem_id)
    if not problem:
        print("\nInvalid problem ID.")
        pause()
        return
    
    session = st.start_session(problem_id)
    if session:
        pm.edit_problem(problem_id, status="In Progress")
        print(f"\nSession started for: {problem.title}")
        print("Timer is running!")
        time.sleep(2)
    else:
        print("\nFailed to start session.")
        pause()


def complete_session(pm, st):
    clear_screen()
    print_header("COMPLETE SESSION")
    
    solved = get_input("Did you solve it? (yes/no): ")
    solved_bool = solved.lower() == 'yes'
    
    solution = ""
    if solved_bool:
        print("\nEnter solution code (press Ctrl+D or Ctrl+Z when done):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            solution = "\n".join(lines)
    
    st.complete_session(solved=solved_bool, solution_code=solution)
    
    active_problem = pm.get_problem(st.sessions[-1].problem_id)
    if active_problem and solved_bool:
        pm.edit_problem(active_problem.id, status="Solved")
    
    elapsed = st.sessions[-1].duration_seconds
    minutes = elapsed // 60
    seconds = elapsed % 60
    
    print(f"\nSession completed!")
    print(f"Time: {minutes}m {seconds}s")
    print(f"Result: {'SOLVED' if solved_bool else 'NOT SOLVED'}")
    pause()


def view_session_history(st, pm):
    clear_screen()
    print_header("SESSION HISTORY")
    
    sessions = st.get_session_history()
    
    if not sessions:
        print("No session history found.")
        pause()
        return
    
    print(f"{'ID':<5} {'Problem':<30} {'Duration':<12} {'Result':<10}")
    print("-" * 60)
    
    for s in sessions:
        problem = pm.get_problem(s.problem_id)
        title = problem.title[:29] if problem else "Unknown"
        minutes = s.duration_seconds // 60
        duration = f"{minutes}m"
        result = "SOLVED" if s.solved else "ATTEMPTED"
        
        print(f"{s.id:<5} {title:<30} {duration:<12} {result:<10}")
    
    print(f"\nTotal sessions: {len(sessions)}")
    pause()


def analytics_menu(analytics):
    while True:
        clear_screen()
        print_header("ANALYTICS & REPORTS")
        print("1. View Statistics")
        print("2. Difficulty Distribution")
        print("3. Topic Analysis")
        print("4. Practice Calendar")
        print("5. Strong Topics")
        print("6. Weak Topics")
        print("7. Full Report")
        print("8. Back to Main Menu")
        
        choice = get_input("\nEnter choice: ", int, allow_empty=True)
        
        if choice == 1:
            clear_screen()
            analytics.display_statistics()
            pause()
        elif choice == 2:
            clear_screen()
            analytics.display_difficulty_chart()
            pause()
        elif choice == 3:
            clear_screen()
            analytics.display_topic_chart()
            pause()
        elif choice == 4:
            clear_screen()
            analytics.display_practice_calendar()
            pause()
        elif choice == 5:
            clear_screen()
            analytics.display_strong_topics()
            pause()
        elif choice == 6:
            clear_screen()
            analytics.display_weak_topics()
            pause()
        elif choice == 7:
            clear_screen()
            analytics.generate_full_report()
            pause()
        elif choice == 8:
            break


def main():
    clear_screen()
    
    pm = ProblemManager()
    st = SessionTracker()
    analytics = Analytics(pm, st)
    
    while True:
        clear_screen()
        print_header("CODETRACK - MAIN MENU")
        
        print("1. Problem Library")
        print("2. Practice Session")
        print("3. Analytics & Reports")
        print("4. Exit")
        
        choice = get_input("\nEnter choice: ", int, allow_empty=True)
        
        if choice == 1:
            problem_library_menu(pm)
        elif choice == 2:
            practice_session_menu(pm, st)
            analytics = Analytics(pm, st)
        elif choice == 3:
            analytics = Analytics(pm, st)
            analytics_menu(analytics)
        elif choice == 4:
            if st.get_active_session():
                print("\nYou have an active session!")
                confirm = get_input("Exit anyway? (yes/no): ")
                if confirm.lower() != 'yes':
                    continue
            
            print("\nThank you for using CodeTrack!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        sys.exit(0)
