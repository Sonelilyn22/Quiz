import pymysql as mdb

db = mdb.connect(host='localhost',user='root',password='root',database='Quiz')

db.autocommit(True)

def insert_one(table:str,query:str) -> str | None:#Название таблицы , запрос
    try:
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO {table} {query}')
        cursor.close()
        return None
    except mdb.IntegrityError: #Если произошла любая ошибка
        print('Во время выполнения запроса произошла ошибка')
        return 'error'

def get_one_by_id(table:str,id:int) -> list | None:
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM {table} WHERE id={id}')
    result = cursor.fetchone()
    cursor.close()
    return result #Результат запроса

def get_one_by_filter(table:str,filter:str) -> list | None:
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM {table} WHERE {filter}')
    result = cursor.fetchone()
    cursor.close()
    return result #Результат запроса
