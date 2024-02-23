from fastapi import APIRouter,Depends,status
from app.schemas import User, ShowUser, UpdateUser
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.repositories import user
from typing import List
from app.oauth import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)



@router.get("/", response_model=List[ShowUser], status_code=status.HTTP_200_OK)
def get_users(db:Session= Depends(get_db),current_user: User = Depends(get_current_user)):
    return user.get_users(db)

@router.get("/{id}", response_model=ShowUser, status_code=status.HTTP_200_OK) 
def get_user(id:int, db:Session=Depends(get_db)):
    usuario = user.get_user(id, db)
    return usuario


@router.post('/',status_code=status.HTTP_201_CREATED)
def create_user(usuario: User, db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    user.create_user(usuario,db)
    return {'respuesta': 'Usuario creado satisfactoriamente !!'}
    

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_user(id:int, db:Session=Depends(get_db)):
    return user.delete_user(id, db)
    

@router.patch('/{id}',status_code=status.HTTP_201_CREATED)
def update_user(id:int, updateUser:UpdateUser, db:Session=Depends(get_db)):
    return user.update_user(id, updateUser, db)
    