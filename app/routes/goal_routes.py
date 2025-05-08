from flask import Blueprint, request, Response
from app.models.goal import Goal
from ..db import db
from .route_utilities import validate_model, create_response_from_model_data

#create bp
bp = Blueprint("goals", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_response_from_model_data(Goal, request_body)

@bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    return [goal.to_dict() for goal in goals]

@bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)

    return goal.to_nested_dict()

@bp.put("/<id>")
def update_goal(id):
    goal = validate_model(Goal, id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    return Response(status=204, mimetype='application/json')

@bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype='application/json')