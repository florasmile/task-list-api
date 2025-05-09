from flask import abort, make_response
from datetime import datetime

def validate_datetime(str):
    try:
        datetime.fromisoformat(str)
    except ValueError:
        invalid = {
            "error": "Invalid datetime format"
        }
        abort(make_response(invalid, 400))
    
    return True