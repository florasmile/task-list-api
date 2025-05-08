from flask import Blueprint, request, Response
from app.models.goal import Goal
from ..db import db
from .route_utilities import validate_model, create_model

#create bp
bp = Blueprint("bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    new_goal = create_model(Goal, request_body)

    db.session.add(new_goal)
    db.session.commit()
    
    response = {
        "goal": new_goal.to_dict()
    }
    return response, 201