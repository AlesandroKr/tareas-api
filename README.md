# NoteBook API

Simple API para anotar tareas o notas.

## Funcionalidades

- Agregar tareas
- Buscar tareas
- Marcar tarea como completado o pendiente
- Borrar tareas
- Filtrar tareas entre estados (pendiente o completado)

## Como correrlo

1. Clonar el repositorio
2. El proyecto proviene con un entorno especifico
    2.1. Crear en entorno virtual con `python -m venv venv`
    2.2. Activar el entorn venv con source venv/bin/activate
    2.3. Instalar los requerimientos minimo con `pip install -r requirements.txt`
3. Levantar el servidor con `uvicorn main:app`. Si se desea que el sevidor se actualicen en cada cambio usar `uvicorn main:app --reload`
4. Ver el resultado en el navegador http://127.0.0.1:8000