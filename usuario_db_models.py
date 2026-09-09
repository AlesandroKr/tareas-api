from sqlalchemy import Column, Integer, String
from tarea_db_models import engine as tareaEngine, Base as tareaBase

engine = tareaEngine

class UsuarioDb(tareaBase):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    email = Column(String)
    password_hash = Column(String)