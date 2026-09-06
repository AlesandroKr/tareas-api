from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base


engine = create_engine("sqlite:///tareas.db")
Base = declarative_base()

class TareaDb(Base):
    __tablename__ = "tareas"
    
    id = Column(Integer, primary_key = True)
    texto = Column(String)
    prioridad = Column(String)
    completado = Column(Boolean)