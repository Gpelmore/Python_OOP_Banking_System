import hashlib
import time
import getpass
import secrets
from collections import defaultdict


def hash_PW(password: str, salt: str = None):
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}{password}". encode()).hexdigest()
    return hashed, salt


def generate_token():
    return secrets.token_hex(32)


class Acc_info:
    def __init__(self):
        self.users = {}
        pass


class Rate_Lim:
    MAX_ATT = 5
    FREEZE_TIME = 30

    def __init__(self):
        self.attempts = defaultdict(list)
    
    def is_locked(self, username):
        now = time.time()
        recent = [t for t in self.attempts[username] if now - t < self.FREEZE_TIME]
        self.attempts[username] = recent
        if len(recent) >= self.MAX_ATT:
            wait = int(self.FREEZE_TIME - (now - recent[0]))
            print(f"Account is locked. Try again in {wait} seconds.")
            return True
        return False
    
    def record_att(self, username):

        self.attempts[username].append(time.time())

    def clear(self, username):

        self.attempts[username] = []



class Bank:
    SESSION_DURATION = 600

    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.limiter = Rate_Lim()

    def Register(self, username, password, accounts):
        if username in self.users:
            print(f"Username {username} already exists.")
            return False
        hashed, salt = hash_PW(password)

        self.users[username] = {
            "hash":     hashed,
            "salt":     salt,
            "Accounts":     accounts
        }

        print(f"User {username} created successfully.")
        return True
    
    def Login(self, username, password):
        if self.limiter.is_locked(username):
            return None
        user = self.users.get(username)

        if not user:
            self.limiter.record_att(username)
            print("\nInvalid username or password.")
            return None
        
        hashed, _ = hash_PW(password ,user["salt"])
        if hashed != user["hash"]:
            self.limiter.record_att(username)
            remaining = Rate_Lim.MAX_ATT - len(self.limiter.attempts[username])
            print(f"Invalid username or password, {remaining} attempt(s) remaining.")
            return None
        
        self.limiter.clear(username)

        token = generate_token()

        self.sessions[token] = {
            "Username": username,
            "Accounts": user["Accounts"],
            "Expires at": time.time() + self.SESSION_DURATION
        }
        
        print(f"Welcome {username}!")
        return token
    
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
    
    def Logout(self, token):
        if token in self.sessions:
            del self.sessions[token]
            print("Logged out successfully.")

    def Sesh_Refresh(self, token):
        session = self.sessions.get(token)
        if session:
            session["Expires at"] = time.time() + self.SESSION_DURATION