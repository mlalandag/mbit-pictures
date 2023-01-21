from datetime import datetime
from sqlalchemy import create_engine
import base64

def get_tags(path, tags):

    # Almacenamos información en la base de datos
    print("Almacenamos información en la base de datos")
    engine = create_engine("mysql+pymysql://mbit:mbit@db/Pictures")
    
    # Tabla Pictures
    with engine.connect() as conn:
        result = conn.execute(f"""INSERT INTO pictures (path, date)
        VALUES ('{path}','{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}')
        """)
    
    # Tabla Tags
        # Recuperamos id
        picture_id = 0
        result = conn.execute(f"""
        SELECT id, path, date FROM pictures WHERE path = '{path}'
        """)
        for row in result:
            picture_id = row[0]
            picture_path = row[1]
            picture_date = row[2]
            print("id:", row[0])
    
        for tag in tags:
            print("tag:", tag)
            conn.execute(f"""INSERT INTO tags (tag, picture_id, confidence, date)
            VALUES ('{tag["tag"]}',{picture_id},{tag["confidence"]},
                '{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}')
            """)
            
        # Obtenemos el tamaño del fichero
        picture_length = get_image_length(picture_path)

    return {
        "id": picture_id,
        "size": picture_length,
        "date": picture_date,
        "tags": tags
    }


def list_images(min_date, max_date, tags):
    # Recuperamos lista de imagenes
    engine = create_engine("mysql+pymysql://mbit:mbit@db/Pictures")

    # Query Base Pictures
    sql_query = """SELECT * FROM pictures p INNER JOIN tags t ON t.picture_id = p.id ORDER BY p.id"""
    
    # Construimos where clausule en funcion de query params
    sql_where = ""
    if min_date is not None and max_date is not None:
        sql_where = sql_where + f""" and p.date between '{min_date}' and '{max_date}' """
    elif min_date is None and max_date is not None:
        sql_where = sql_where + f""" and p.date < '{max_date}' """        
    elif min_date is not None and max_date is None:
        sql_where = sql_where + f""" and p.date > '{min_date}' """   
        
    if tags is not None:
        sql_where = sql_where + f""" and tag IN ('{tags}') """

    print(f"""sql = {sql_query + sql_where}""" )

    list_images = []
    with engine.connect() as conn:        
        result = conn.execute(sql_query + sql_where)
        id = 0
        first_time = True
        list_tags = []
        for row in result:
            print(f"""Tratamos row '{row}'""")
            if first_time:
                id = row[0]
            if row[0] != id and not first_time:
                print(f"""id ha cambiado '{id}'""")
                list_images.append(prepare_image_data(current_id, current_path, current_date, list_tags))
                list_tags = []
                id = row[0]
            current_id = row[0]
            current_path = row[1]
            current_date = row[2]
            tag = {"tag": row[3], "confidence": row[5]}
            list_tags.append(tag)
            first_time = False
        list_images.append(prepare_image_data(current_id, current_path, current_date, list_tags))

    return list_images

def prepare_image_data(current_id, current_path, current_date, list_tags):
    print(f"""Preparamos los datos de la imagen '{id}'""")
    image = {
        "id": current_id,
        "size": get_image_length(current_path),
        "date": current_date,
        "tags": list_tags
    }
    return image

def get_image_length(path):
    print(f"""Obtenemos el tamaño del fichero '{path}'""")
    image_file = open(path, "r")
    print("Pasamos la imagen a binario")
    binary_image_file = base64.b64decode(image_file.read())
    picture_length = len(binary_image_file)
    image_file.close()
    return picture_length