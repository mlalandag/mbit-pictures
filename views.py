from . import controller
from flask import Blueprint, request, make_response

bp = Blueprint('pictures', __name__, url_prefix='/')

@bp.post("/images/tags")
def get_tags():
    min_confidence = request.args.get("min_confidence")
    print(min_confidence)
    
    # input checks
    print("input checks")
    if min_confidence is None:
        min_confidence = 80
    else:
        min_confidence = int(min_confidence)
    
    if not request.is_json or "data" not in request.json:
        return make_response({"description": "Debes incluir el audio en base64 como un campo llamado data en el body"}, 400)

    response = controller.get_tags(min_confidence, request.json["data"])

    return response
    

@bp.get("/images")
def list_images():
    min_date = request.args.get("min_date")
    if min_date is not None:
        min_date.replace("%20", " ")
        print("min_date: ", min_date)   
    max_date = request.args.get("max_date")
    if max_date is not None:
        max_date.replace("%20", " ")
        print("max_date: ", max_date)      
    print("max_date: ", min_date)   
    tags = request.args.get("tags")
    if tags is not None:
        tags = tags.replace("%20", " ")
        tags = "'" + tags.replace(",", "','") + "'"
        print("tags: ", tags)


    response = controller.list_images(min_date, max_date, tags)

    return response        

@bp.get("/images/<id>")
def get_image(id):
    response = controller.get_image(id)
    return response

@bp.get("/images/tags")
def list_tags():
    min_date = request.args.get("min_date")
    if min_date is not None:
        min_date.replace("%20", " ")
        print("min_date: ", min_date)   
    max_date = request.args.get("max_date")
    if max_date is not None:
        max_date.replace("%20", " ")
        print("max_date: ", max_date)      
    print("max_date: ", min_date)  
    response = controller.list_tags(min_date, max_date)
    return response