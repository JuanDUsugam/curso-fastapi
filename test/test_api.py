from fastapi.testclient import TestClient
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from main import app
from app.db.models import Base
from app.hashing import Hash
from app.db.database import get_db
import time

db_path = os.path.join(os.path.dirname(__file__),'test.db')
db_uri = "sqlite:///{}".format(db_path)

SQLALCHEMY_DATABASE_URL = db_uri
engine_test = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})
TestingSessionLocal = sessionmaker(bind=engine_test,autocommit=False,autoflush=False)
Base.metadata.create_all(bind=engine_test)


client = TestClient(app)

def insert_user_test():
    password_hash = Hash.hash_password('prueba12')
    conn = engine_test.connect()
    data = ({"username":'prueba12', 'password':password_hash, 'nombre':'prueba_nombre', 'apellido':'prueba_apellido', 'direccion':'prueba_direccion', 'telefono':1212, 'correo':'prueba12@mail.com'})
    query = text("""INSERT INTO usuario(username, password, nombre, apellido, direccion, telefono, correo) VALUES (:username, :password, :nombre, :apellido, :direccion, :telefono, :correo)""")
    conn.execute(query, data)
    conn.commit()
    conn.close()


insert_user_test()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
def test_create_user():
    usuario_login ={"username": "prueba12", "password": "prueba12"}
    response_token = client.post('/login/', data=usuario_login)
    assert response_token.status_code == 200
    usuario = {
        "username": "prueba",   
        "password": "1234",
        "nombre": "prueba",
        "apellido": "prueba",
        "direccion": "prueba",
        "telefono": 0,
        "correo": "prueba@mail.com",
        "creacion": "2024-02-22T13:43:38.596430"
    }
    headers = {
        "Authorization": f"Bearer {response_token.json()['access_token']}"
    }
    response = client.post('/user/', json=usuario, headers=headers)
    assert response.status_code == 201
    assert response.json()['respuesta'] == 'Usuario creado satisfactoriamente !!'


def test_get_users():
    response_token = client.post('/login/', data={"username": "prueba12", "password": "prueba12"})
    assert response_token.status_code == 200
    headers = {
        "Authorization": f"Bearer {response_token.json()['access_token']}"
    }
    response = client.get('/user/', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_user():
    response=client.get('/user/1')
    assert response.status_code == 200
    assert response.json()['username'] == 'prueba12'

def test_delete_user():
    response=client.delete('/user/1')
    assert response.status_code == 200
    assert response.json()['respuesta'] == 'Usuario eliminado satisfactoriamente!!'

def test_update_user():
    usuario={
        "username": "juan",
        "correo": "juan@gmail.com"
    }
    response=client.patch('/user/2', json=usuario)
    assert response.status_code == 201
    assert response.json()['respuesta'] == "Usuario actualizado satisfactoriamente!!"

def test_delete_databases():
    engine_test.dispose()
    db_path = os.path.join(os.path.dirname(__file__),'test.db')
    os.remove(db_path)