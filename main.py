from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker
from tarea_db_models import Base, engine, TareaDb
from usuario_db_models import UsuarioDb

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class NuevoUsuario(BaseModel):
    nombre: str
    email: EmailStr

@app.post("/usuario")
def crearUsuario(nuevoUsuario: NuevoUsuario):
    session = Session()
    nueva = UsuarioDb(nombre=nuevoUsuario.nombre, email=nuevoUsuario.email)
    session.add(nueva)
    session.commit()
    session.close()
    return {"Guardado": True}

@app.get("/usuarios")
def extraerUsuarioDB():
    session = Session()
    resultado = session.query(UsuarioDb).all()
    session.close()
    return {"usuarios": resultado}


class NuevaTarea(BaseModel):
    text: str
    priority: str = "Medio"
    complete : bool = False
    usurio_id: int
    
    @field_validator("priority")
    @classmethod
    def validar_prioridad(cls, valor):
        if valor not in ["Alta", "Medio", "Baja"]:
            raise ValueError("Prioridad desconocida")
        return valor
        

#---------------------------
@app.get("/")
def extraerTareasDB():
    session = Session()
    resultado = session.query(TareaDb).all()
    session.close()
    return {"tareas": resultado}

#---------------------------

#Agregar input para buscar en la lista


@app.get("/tareas/buscar")
def buscarTareas(texto: str):
    session = Session()
    resultado = session.query(TareaDb).filter(TareaDb.texto.contains(texto)).all()
    session.close()
    return {"tareas": resultado}


#---------------------------
@app.post("/tareas/guardar")
def guardarTareaDB(nuevaTarea: NuevaTarea):
    session = Session()
    existente = session.query(TareaDb).filter(TareaDb.texto == nuevaTarea.text).first()
    if existente is not None:
        raise HTTPException(status_code=400, detail="Ya existe una tarea con ese texto")
    nueva = TareaDb(texto=nuevaTarea.text, prioridad=nuevaTarea.priority, completado=nuevaTarea.complete, usuario_id=nuevaTarea.usuario_id)
    session.add(nueva)
    session.commit()
    session.close()
    return {"Guardado": True}


#--------------------------
@app.delete("/tareas/borrar/{tarea_id}")
def borrarTareaDB(tarea_id : int):
    session = Session()
    resultado = session.query(TareaDb).filter(TareaDb.id == tarea_id).first()
    
    if resultado is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    session.delete(resultado)
    session.commit()
    session.close()
    return {"Eliminado": True}

#---------------------------
@app.put("/tareas/{tarea_id}")
def marcarCompletadoDB(tarea_id: int):
    session = Session()
    resultado = session.query(TareaDb).filter(TareaDb.id == tarea_id).first()
    
    if resultado is None:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
    resultado.completado = not resultado.completado;
    session.commit()
    session.close()
    return {"Editado" : True}

#---------------------------
@app.get("/tareas/pendientes")
def mostrarTareasPendientesDB():
    session = Session()
    resultado = session.query(TareaDb).filter(TareaDb.completado == False).all()
    session.close()
    return {"tareas": resultado}

#---------------------------
@app.get("/tareas/completados")
def mostrarTareasCompletadasDB():
    session = Session()
    resultado = session.query(TareaDb).filter(TareaDb.completado == True).all()
    session.close()
    return {"tareas": resultado}
