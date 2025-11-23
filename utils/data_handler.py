import json
import os

def read_json(file):
    try:
        with open(file, 'r') as rfile:
            data = json.load(rfile)
            return data
    except FileNotFoundError:
        if 'problems' in file:
            return []
        elif 'sessions' in file:
            return []
        else:
            return {}
    except json.JSONDecodeError:
        print(f"Error: {file} is corrupted")
        backup_file = file+'.backup'
        if os.path.exists(backup_file):
            print("Restoring from backup....")
            with open(backup_file, 'r') as rfile:
                return json.load(rfile)
        else:
            return [] if 'problems' in filename or 'sessions' in filename else {}

def write_json(file, data):
    backup_data(file)
    temp_file = file+'.tmp'

    try:
        with open(temp_file,'w') as wfile:
            json.dump(data, file, indent =2, ensure_ascii = False)

        os.replace(temp_file,file)
        return True
    except Exception as e:
        print(f"Error writing to {file}: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file) 
        return False

def backup_data(file):
    if not os.path.exists(file):
        return
    bkpfile = file+'backup'

    try:
        with open(file, 'r') as og:
            data = rfile.read()
        with open(bkupfile, 'w') as bkup:
            bkup.write(data)
        return True
    
    except Exception as e:
        print(f"Warning: Could not backup {file}: {e}")
        return False

# test
# Test 1: Write and read
data = [{"id": 1, "name": "test"}]
write_json('test.json', data)
result = read_json('test.json')
print(result)  # Should print: [{"id": 1, "name": "test"}]

# Test 2: Read non-existent file
result = read_json('nonexistent.json')
print(result)  # Should print: [] or {}

# Test 3: Backup
write_json('test.json', [1, 2, 3])
# Check: test.json.backup should exist with old data
