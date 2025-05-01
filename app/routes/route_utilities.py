from flask import abort, make_response
from ..db import db
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

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    return new_model
