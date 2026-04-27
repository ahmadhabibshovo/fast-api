import sys
import traceback

try:
    from app.utils import hash
    print("Hashing password:", hash("12345678"))
except Exception as e:
    traceback.print_exc()
