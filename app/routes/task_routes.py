from flask import Blueprint, request, Response
from sqlalchemy import asc, desc
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model, create_response_from_model_data
from datetime import datetime
import requests
import os

#create bp
bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_response_from_model_data(Task, request_body)


@bp.get("")
def get_all_tasks():
    query = db.select(Task)
    sort_param = request.args.get("sort")
    if sort_param == 'asc':
        query = query.order_by(asc(Task.title))
    elif sort_param == 'desc':
        query = query.order_by(desc(Task.title))
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query)

    return [task.to_dict() for task in tasks]

@bp.put("/<id>")
def update_task(id):
    task = validate_model(Task, id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype='application/json')

@bp.get("/<id>")
def get_task(id):
    task = validate_model(Task, id)

    return task.to_nested_dict()

@bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype='application/json')

@bp.patch("/<id>/<completion_status>")
def modify_task_completion_status(id, completion_status):
    task = validate_model(Task, id)
    
    if completion_status == 'mark_incomplete':
        task.completed_at = None
    else:
        task.completed_at = datetime.now()
        # send message to slack workspace
        send_request_to_slackbot(task.title)

    db.session.commit()

    return Response(status= 204, mimetype="application/json")

def send_request_to_slackbot(task_title):
    path = "https://slack.com/api/chat.postMessage"
   
    headers = {
    "Authorization": f"Bearer {os.environ.get('SLACKBOT_ACCESS_TOKEN')}",
    "Content-Type": "application/json"
    }

    body = {
        "channel": "test-slack-api",
        "text": f"Dehui just completed the task {task_title}"
    }

    response = requests.post(path, headers=headers, json=body)

    print(response.status_code)
    print(response.json())
