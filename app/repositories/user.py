from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException, status
from app.hashing import Hash




def create_user(usuario,db:Session):
    usuario = usuario.dict()
    try:
        nuevo_usuario = models.User(
        username=usuario['username'],
        password=Hash.hash_password(usuario['password']),
        nombre=usuario['nombre'],
        apellido=usuario['apellido'],
        direccion=usuario['direccion'],
        telefono=usuario['telefono'],
        correo=usuario['correo']
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error en la creación de usuario {e}"
        )

def get_user(id, db:Session):
    usuario = db.query(models.User).filter(models.User.id == id).first()
    print(usuario, id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

def get_users(db:Session):
    data = db.query(models.User).all()
    return data

def delete_user(id, db:Session):
    usuario = db.query(models.User).filter(models.User.id == id)
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    usuario.delete(synchronize_session=False)
    db.commit()
    return {"respuesta":"Usuario eliminado satisfactoriamente!!"}

def update_user(id, updateUser, db:Session):
    usuario= db.query(models.User).filter(models.User.id==id)
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    usuario.update(updateUser.dict(exclude_unset=True))
    db.commit()
    return {"respuesta":"Usuario actualizado satisfactoriamente!!"}