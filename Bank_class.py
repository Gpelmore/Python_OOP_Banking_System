import hashlib
import os
import json
import time
import getpass
import secrets
from collections import defaultdict
from Account_Classes import user
from Account_Classes import Savings
from Account_Classes import Checking


# Hashes the password with a salt for secure storage
def hash_PW(password: str, salt: str = None):
    # Generate a new salt if one isn't provided (e.g., during registration)
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}{password}". encode()).hexdigest()
    return hashed, salt

# Generates a random session identifier
def generate_token():
    return secrets.token_hex(32)

#=========================================================================================================

# Security class to prevent brute-force login attempts
class Rate_Lim:
    MAX_ATT = 5
    FREEZE_TIME = 30

    def __init__(self):
        # Keeps track of login attempt timestamps for each username
        self.attempts = defaultdict(list)
    
    # Checks if the user is currently locked out
    def is_locked(self, username):
        now = time.time()
        # Only keep attempts that happened within the freeze window
        recent = [t for t in self.attempts[username] if now - t < self.FREEZE_TIME]
        self.attempts[username] = recent
        
        # Lock out if max attempts are reached
        if len(recent) >= self.MAX_ATT:
            wait = int(self.FREEZE_TIME - (now - recent[0]))
            print(f"Account is locked. Try again in {wait} seconds.")
            return True
        return False
    
    # Logs a failed attempt
    def record_att(self, username):
        self.attempts[username].append(time.time())

    # Resets the attempts upon successful login
    def clear(self, username):
        self.attempts[username] = []

#=============================================================================================================================

# Core engine for managing users, sessions, and data storage
class Bank:
    SESSION_DURATION = 600 # 10 minutes

    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.limiter = Rate_Lim()
        # Automatically load existing data on startup
        self.Load_All_Users()
    
    # Reads the local directory and rebuilds objects from JSON files
    def Load_All_Users(self):
        all_files = os.listdir() 
        
        for filename in all_files:
            # Check if the file is one of our user data files
            if filename.endswith("_data.json"):
                with open(filename, "r") as f:
                    data = json.load(f)
                    
                    # 3. Rebuild the User object from the file data
                    username = data["username"]
                    
                    # We need to turn the 'accts' dictionaries back into real objects
                    rebuilt_accts = []
                    for a in data["acct"]:
                        if a["type"] == "Checking":
                            acc_obj = Checking(a["id"])
                        else:
                            #acc_obj = Savings(a["id"])
                            saved_time = a.get("last_interest_time", time.time())
                            acc_obj = Savings(a["id"], last_interest_time = saved_time)

                        # Restore the saved balance
                        acc_obj.Bal_info = a["balance"]
                        rebuilt_accts.append(acc_obj)
                    
                    # 4. Store the rebuilt User object in our bank's dictionary
                    self.users[username] = user(
                        username, 
                        data["hash"], 
                        data["salt"], 
                        rebuilt_accts
                    )
        
        print(f"System ready. {len(self.users)} users loaded from disk.")

    # Creates a new user, hashes their password, and saves them
    def Register(self, username, password, accounts):
        # Prevent duplicate usernames
        if username in self.users:
            print(f"Username {username} already exists.")
            return False
            
        hashed, salt = hash_PW(password)

        nuser = user(username, hashed, salt, accounts)

        # Store in memory
        self.users[username] = nuser

        print(f"User {username} created successfully.")
        
        # Save to disk
        nuser.save_to_json()
        return True
    
    # Authenticates a user and creates an active session
    def Login(self, username, password):
        # Check if they are locked out before checking credentials
        if self.limiter.is_locked(username):
            return None
            
        user = self.users.get(username)

        # Username doesn't exist
        if not user:
            self.limiter.record_att(username)
            print("\nInvalid username or password.")
            return None
        
        # Hash the input with the stored salt to see if it matches the stored hash
        hashed, _ = hash_PW(password ,user.salt)
        if hashed != user.hash:
            self.limiter.record_att(username)
            remaining = Rate_Lim.MAX_ATT - len(self.limiter.attempts[username])
            print(f"Invalid username or password, {remaining} attempt(s) remaining.")
            return None
        
        # Success! Clear failed attempts
        self.limiter.clear(username)

        token = generate_token()

        # Create the session with an expiration timestamp
        self.sessions[token] = {
            "Username": username,
            "Accounts": user.acct,
            "Expires at": time.time() + self.SESSION_DURATION
        }
        
        print(f"Welcome {username}!")
        return token
    
    # Retrieves an active session, killing it if it has expired
    def Get_Session(self, token):
        session = self.sessions.get(token)
        if not session:
            print("Invalid seeion.")
            return None
        if time.time() > session["Expires at"]:
            del self.sessions[token]
            print("Session expired. Please log in again.\n\n")
            return None
        return session
    
    # Explicitly ends a session
    def Logout(self, token):
        if token in self.sessions:
            del self.sessions[token]
            print("Logged out successfully.")

    # Resets the timeout clock on a session so active users aren't booted
    def Sesh_Refresh(self, token):
        session = self.sessions.get(token)
        if session:
            session["Expires at"] = time.time() + self.SESSION_DURATION