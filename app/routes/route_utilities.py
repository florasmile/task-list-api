from flask import abort, make_response
from ..db import db
from sqlalchemy import asc, desc
# route helper functions

#retrieve a model instance by its ID
def validate_model(cls, id):
    #check if id is a num
    try:
        id = int(id)
    except:
        invalid = {"message": f"{cls.__name__} id ({id}) is invalid"}
        abort(make_response(invalid, 400))
    # check if id exists
    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} ({id}) not found"}
        abort(make_response(response, 404))
    
    return model

def create_response_from_model_data(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()
    

    return new_model.to_nested_dict(), 201

def get_all_sorted_with_filters(cls, request_data):
    query = db.select(cls)

    sort_order = "asc"
    sort_by = "title"

    for key, value in request_data.items():
        if key == "sort":
            sort_order = value
        elif key == "sort_by":
            sort_by = value
        elif hasattr(cls, key):
            query = query.where(getattr(cls, key).ilike(f"%{value}%"))
    
    sort_column = getattr(cls, sort_by)
    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    models = db.session.scalars(query)

    return [model.to_dict() for model in models]


