from flask import Blueprint, request
from . import controller

bp = Blueprint('pictures', __name_, url_prefix='/')


@app.post("/images/tags")
def get_tags():
    min_confidence = int(request.args.get("min_confidence"))
    print(min_confidence)
    
    # input checks
    print("input checks")
    if min_confidence is None:
        min_confidence = 80
    
    if not request.is_json or "data" not in request.json:
        return make_response({"description": "Debes incluir el audio en base64 como un campo llamado data en el body"}, 400)

    response = controller.get_tags(min_confidence, request.json["data"])

    return response
    

@app.get("/images")
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
        tags = "'" + tags.replace(",", "','") + "'"
        print("tags: ", min_date)


    response = controller.list_images(min_date, max_date, tags)

    return response        

@app.get("/images/{i}")
def get_image():
    return None

@app.get("/images/tags")
def list_tags():
    return None