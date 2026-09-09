from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker
from tarea_db_models import Base, engine, TareaDb
from usuario_db_models import UsuarioDb
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#----- CLASES MODELOS-----

class NuevoUsuario(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    
class LoginAccount(BaseModel):
    email: EmailStr
    password: str


@app.post("/login")
def iniciarSesion(loginAccount: LoginAccount):
    session = Session()
    usuario = session.query(UsuarioDb).filter(UsuarioDb.email == loginAccount.email).first()
    
    if usuario is None:
        raise HTTPException(status_code=404, detail="Ese correo no está registrado")
    
    is_valid = password_hash.verify(loginAccount.password, usuario.password_hash)
    
    if is_valid is False:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    session.close()
    
    usuario_logged = {
        "id": usuario.id,
        "nombre": usuario.nombre
    }
    
    return usuario_logged
    
class NuevaTarea(BaseModel):
    text: str
    priority: str = "Medio"
    complete : bool = False
    
    @field_validator("priority")
    @classmethod
    def validar_prioridad(cls, valor):
        if valor not in ["Alta", "Medio", "Baja"]:
            raise ValueError("Prioridad desconocida")
        return valor
        

#------------- ENDPOINTS --------------#
@app.get("/")
def extraer_Tareas():
    session = Session()
    resultado = session.query(TareaDb).all()
    session.close()
    return {"tareas": resultado}


#------------- EXTRACT AND CREATE USERS --------------
@app.get("/usuarios")
def extraer_Usuario():
    session = Session()
    resultado = session.query(UsuarioDb).all()
    session.close()
    return {"usuarios": resultado}

@app.post("/usuario")
def crear_Usuario(nuevoUsuario: NuevoUsuario):
    session = Session()
    
    hashed_password = password_hash.hash(nuevoUsuario.password)
    nueva = UsuarioDb(nombre=nuevoUsuario.nombre, email=nuevoUsuario.email, password_hash=hashed_password)
    session.add(nueva)
    session.commit()
    session.close()
    return {"Guardado": True}
#---------------------------



#------------- EXTRACT, CREATE, AND SEARCH TAKS --------------

@app.get("/usuarios/{usuario_id}/tareas")
def extraer_Tareas_Usuario(usuario_id: int):
    session = Session()
    usuario = session.query(UsuarioDb).filter(UsuarioDb.id == usuario_id).first()
    if usuario is None:
            raise HTTPException(status_code=404, detail="No existe ese Usuario")
    resultado = session.query(TareaDb).filter(TareaDb.usuario_id == usuario_id).all()
    session.close()
    return {"tareas": resultado}

@app.post("/usuarios/{usuario_id}/tareas/guardar")
def guardar_Tarea_Usuarios(nuevaTarea: NuevaTarea, usuario_id: int):
    session = Session()
    existente = session.query(TareaDb).filter(TareaDb.texto == nuevaTarea.text, TareaDb.usuario_id == usuario_id).first()
    if existente is not None:
        raise HTTPException(status_code=400, detail="Ya existe una tarea con ese texto")
    nueva = TareaDb(texto=nuevaTarea.text, prioridad=nuevaTarea.priority, completado=nuevaTarea.complete, usuario_id=usuario_id)
    session.add(nueva)
    session.commit()
    session.close()
    return {"Guardado": True}


@app.get("/usuarios/{usuario_id}/tareas/buscar")
def buscar_Tareas_Usuarios(texto: str, usuario_id: int):
    session = Session()
    usuario = session.query(UsuarioDb).filter(UsuarioDb.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    resultado = session.query(TareaDb).filter(TareaDb.texto.contains(texto), TareaDb.usuario_id == usuario_id).all()
    session.close()
    return {"tareas": resultado}
#---------------------------

#------------- DELETE, CHECK, AND FILTER TAKS --------------

@app.delete("/usuarios/{usuario_id}/tareas/borrar/{tarea_id}")
def borrar_Tarea_Usuarios(tarea_id : int, usuario_id: int):
    session = Session()
    
    usuario = session.query(UsuarioDb).filter(UsuarioDb.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    resultado = session.query(TareaDb).filter(TareaDb.id == tarea_id).first()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    if resultado.usuario_id != usuario_id:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    session.delete(resultado)
    session.commit()
    session.close()
    return {"Eliminado": True}

@app.put("/usuarios/{usuario_id}/tareas/{tarea_id}")
def marcar_Completado(tarea_id: int, usuario_id: int):
    session = Session()
    
    usuario = session.query(UsuarioDb).filter(UsuarioDb.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    resultado = session.query(TareaDb).filter(TareaDb.id == tarea_id).first()
    
    if resultado is None:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
    if resultado.usuario_id != usuario_id:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        
    resultado.completado = not resultado.completado
    session.commit()
    session.close()
    return {"Editado" : True}

@app.get("/usuarios/{usuario_id}/tareas/pendientes")
def mostrar_Tareas_Pendientes(usuario_id: int):
    session = Session()
    
    usuario = session.query(UsuarioDb).filter(UsuarioDb.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    resultado = session.query(TareaDb).filter(TareaDb.completado == False, TareaDb.usuario_id== usuario_id).all()
    
    session.close()
    
    return {"tareas": resultado}


@app.get("/usuarios/{usuario_id}/tareas/completados")
def mostrar_Tareas_Completadas(usuario_id: int):
    session = Session()
    
    usuario = session.query(UsuarioDb).filter(UsuarioDb.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    resultado = session.query(TareaDb).filter(TareaDb.completado == True, TareaDb.usuario_id == usuario_id).all()
    
    session.close()
    
    return {"tareas": resultado}

#---------------------------