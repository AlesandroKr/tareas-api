from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base


engine = create_engine("sqlite:///tareas.db")
Base = declarative_base()

class TareaDb(Base):
    __tablename__ = "tareas"
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    id = Column(Integer, primary_key = True)
    texto = Column(String)
    prioridad = Column(String)
    completado = Column(Boolean)