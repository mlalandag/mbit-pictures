from datetime import datetime
from sqlalchemy import create_engine

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
        print("Obtenemos el tamaño del fichero:")
        image_file = open(picture_path, "r")
        picture_length = len(image_file.read())
        image_file.close()


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
    sql_query = """SELECT * FROM pictures p INNER JOIN tags t ON t.picture_id = p.id """
    
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
        for row in result:
            image = {
                "id": row[0],
                "size": 0,  #TODO
                "date": row[2],
                "tags": None  # TODO 
            }
            list_images.append(image)

    return list_images