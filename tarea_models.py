class ListaTareas():
    def __init__(self):
        self.tareas = []
        self.siguiente_id = 1

    def agregar(self, tarea, prioridad = "media", completado = False):
        self.tareas.append(
            {
                "id":self.siguiente_id,
                "texto" : tarea,
                "prioridad": prioridad,
                "completado": completado,
            }
        )
        self.siguiente_id += 1
    
    def eliminar(self, id_tarea):
        for tarea in self.tareas:
            if id_tarea == tarea["id"]:
                self.tareas.remove(tarea)
                
    def editar(self, tarea_id):
        for tarea in self.tareas:
            if tarea_id == tarea["id"]:
                tarea["completado"] = not tarea["completado"]
                
    def filtrar_por_estado(self, completado):        
        resultado = []
        for tarea in self.tareas:
            if tarea["completado"] == completado:
                resultado.append(tarea)
        return resultado
