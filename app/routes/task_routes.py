from flask import Blueprint, request
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model, create_model

#create bp
bp = Blueprint("bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    new_task = create_model(Task, request_body)

    db.session.add(new_task)
    db.session.commit()
    
    return new_task.to_dict(), 201

