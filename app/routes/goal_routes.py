from flask import Blueprint, request, Response
from app.models.goal import Goal
from app.models.task import Task
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


@bp.post("/<goal_id>/tasks")
def post_task_ids_to_goal(goal_id):
    # validate goal_id
    goal = validate_model(Goal, goal_id)
    # remove the relation of the goal with its existing tasks
    for task in goal.tasks:
        task.goal_id = None
    #validate each task id in the request body
    
    request_body = request.get_json()
    task_ids = request_body.get("task_ids")
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }
@bp.get("/<goal_id>/tasks")
def get_tasks_of_one_goal(goal_id):
    #validate goal
    goal = validate_model(Goal, goal_id)
    response = goal.to_dict()
    response["tasks"] = [task.to_dict() for task in goal.tasks]
    return response