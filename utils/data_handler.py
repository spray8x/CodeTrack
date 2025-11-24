import json
import os


def read_json(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    
    except FileNotFoundError:
        if 'problems' in filename:
            return []
        elif 'sessions' in filename:
            return []
        else:
            return {}
    
    except json.JSONDecodeError:
        print(f"Error: {filename} is corrupted")
        backup_file = filename + '.backup'
        if os.path.exists(backup_file):
            print("Restoring from backup...")
            with open(backup_file, 'r') as file:
                return json.load(file)
        else:
            return [] if 'problems' in filename or 'sessions' in filename else {}


def write_json(filename, data):
    backup_data(filename)
    
    temp_filename = filename + '.tmp'
    
    try:
        with open(temp_filename, 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        
        os.replace(temp_filename, filename)
        return True
    
    except Exception as e:
        print(f"Error writing to {filename}: {e}")
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        return False


def backup_data(filename):
    if not os.path.exists(filename):
        return
    
    backup_filename = filename + '.backup'
    
    try:
        with open(filename, 'r') as original:
            data = original.read()
        
        with open(backup_filename, 'w') as backup:
            backup.write(data)
        
        return True
    
    except Exception as e:
        print(f"Warning: Could not create backup of {filename}: {e}")
        return False
