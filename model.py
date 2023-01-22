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
        picture_length = get_image_length_and_data(picture_path)[0]

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
    sql_query = """SELECT * FROM pictures p INNER JOIN tags t ON t.picture_id = p.id"""
    
    # Construimos where clausule en funcion de query params
    sql_where = ""
    if min_date is not None and max_date is not None:
        sql_where = sql_where + f""" where p.date between '{min_date}' and '{max_date}' """
    elif min_date is None and max_date is not None:
        sql_where = sql_where + f""" where p.date < '{max_date}' """        
    elif min_date is not None and max_date is None:
        sql_where = sql_where + f""" where p.date > '{min_date}' """   
        
    if tags is not None:
        if len(sql_where) > 0:
            sql_where = sql_where + f""" and t.tag IN ({tags}) """
        else:
            sql_where = f""" where t.tag IN ({tags}) """

    sql_query_order_by =   """ ORDER BY p.id """

    print(f"""sql = {sql_query + sql_where + sql_query_order_by}""" )

    list_images = []
    with engine.connect() as conn:        
        result = conn.execute(sql_query + sql_where + sql_query_order_by)
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
        if id > 0:
            list_images.append(prepare_image_data(current_id, current_path, current_date, list_tags))

    return list_images

def prepare_image_data(current_id, current_path, current_date, list_tags):
    print(f"""Preparamos los datos de la imagen '{id}'""")
    image = {
        "id": current_id,
        "size": get_image_length_and_data(current_path)[0],
        "date": current_date,
        "tags": list_tags
    }
    return image


def get_image_length_and_data(path):
    print(f"""Obtenemos el tamaño del fichero '{path}'""")
    image_file = open(path, "r")
    print("Leemos base64")
    base64_image_file = image_file.read()
    print("Pasamos la imagen a binario")
    binary_image_file = base64.b64decode(base64_image_file)
    print("Longitud del binario")
    picture_length = len(binary_image_file)
    image_file.close()
    print("return")
    return picture_length, binary_image_file, base64_image_file


def get_image(id):
    # Recuperamos lista de imagenes
    engine = create_engine("mysql+pymysql://mbit:mbit@db/Pictures")

    # Query Base Pictures
    sql_query = f"""SELECT * FROM pictures p INNER JOIN tags t ON t.picture_id = p.id where p.id = {id}"""

    with engine.connect() as conn:        
        result = conn.execute(sql_query)

        id = 0
        list_tags = []
        image = {}
        for row in result:
            print(f"""Tratamos row '{row}'""")
            id = row[0]
            path = row[1]
            date = row[2]
            tag = {"tag": row[3], "confidence": row[5]}
            list_tags.append(tag)
        if id > 0:
            image = prepare_image_data_with_file(id, path, date, list_tags)

    return image

def prepare_image_data_with_file(current_id, current_path, current_date, list_tags):
    print(f"""Preparamos los datos de la imagen '{id}'""")
    lenth, data, base64 = get_image_length_and_data(current_path)
    image = {
        "id": current_id,
        "size": lenth,
        "date": current_date,
        "tags": list_tags,
        "data": base64
    }
    return image


def list_tags(min_date, max_date):
    # Recuperamos lista de imagenes
    engine = create_engine("mysql+pymysql://mbit:mbit@db/Pictures")

    # Query Base Pictures
    sql_query = f"""SELECT tag,count(*),min(t.confidence),max(t.confidence),avg(t.confidence) FROM tags t """

        # Construimos where clausule en funcion de query params
    sql_where = ""
    if min_date is not None and max_date is not None:
        sql_where = sql_where + f""" where t.date between '{min_date}' and '{max_date}' """
    elif min_date is None and max_date is not None:
        sql_where = sql_where + f""" where t.date < '{max_date}' """        
    elif min_date is not None and max_date is None:
        sql_where = sql_where + f""" where t.date > '{min_date}' """  

    sql_query_group_by =   """ GROUP BY t.tag """

    with engine.connect() as conn:        
        result = conn.execute(sql_query + sql_where + sql_query_group_by)
        list_tags = []
        for row in result:
            print(f"""Tratamos tag '{row}'""")
            tag = {
                "tag": row[0],
                "n_images": row[1],
                "min_confidence": row[2],
                "max_confidence": row[3],
                "mean_confidence": row[4]
            }
            list_tags.append(tag)


    return list_tags