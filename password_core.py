import string
import hashlib
import math
import bcrypt
import zxcvbn
import requests
import os
import sys

COMMON_PASSWORDS = set()

def get_resource_path(filename):
    """
    Get the correct path to a resource file.
    Works in both development and PyInstaller bundled environments.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled EXE (PyInstaller)
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

def load_common_passwords(filename="common_passwords.txt"):
    try:
        resource_path = get_resource_path(filename)
        with open(resource_path, "r", encoding="utf-8") as f:
            for line in f:
                COMMON_PASSWORDS.add(line.strip().lower())
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Common password checking disabled.")

def analyze_password(password):
    score = 0
    charset = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if any(c.islower() for c in password):
        score += 1
        charset += 26
    else:
        feedback.append("Add lowercase letters")

    if any(c.isupper() for c in password):
        score += 1
        charset += 26
    else:
        feedback.append("Add uppercase letters")

    if any(c.isdigit() for c in password):
        score += 1
        charset += 10
    else:
        feedback.append("Add numbers")

    if any(c in string.punctuation for c in password):
        score += 1
        charset += len(string.punctuation)
    else:
        feedback.append("Add symbols")

    is_common = password.lower() in COMMON_PASSWORDS
    entropy = len(password) * math.log2(charset) if charset > 0 else 0
    
    # Use zxcvbn for advanced analysis
    zxcvbn_result = zxcvbn.zxcvbn(password)
    crack_times = zxcvbn_result['crack_times_display']
    zxcvbn_feedback = zxcvbn_result['feedback']['suggestions']
    
    # Check if breached
    breached_count = check_breached_password(password)
    
    return score, charset, feedback, is_common, entropy, crack_times, zxcvbn_feedback, breached_count

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode('utf-8', errors='ignore')

def check_breached_password(password):
    """
    Check if password has been breached using k-anonymity.
    Returns:
    - Positive number: times breached
    - 0: not breached
    - -1: check failed (offline/error)
    """
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]
    try:
        response = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}", 
            timeout=5
        )
        if response.status_code == 200:
            hashes = response.text
            for line in hashes.split('\n'):
                if line.startswith(suffix):
                    count = int(line.split(':')[1])
                    return count  # Number of times breached
        return 0  # Not breached
    except requests.RequestException:
        return -1  # Check failed (assume offline)
