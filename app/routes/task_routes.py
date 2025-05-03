from flask import Blueprint, request, Response
from sqlalchemy import asc, desc
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
    
    return new_task.to_nested_dict(), 201

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

@bp.delete("<id>")
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype='application/json')