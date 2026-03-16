import os
import json

class Agent:
    def __init__(self):
        self.setup_tools()
        self.messages =[
        {"role": "system", "content": "Eres Jarvis y tu creador es Jano"}
    ]

    def setup_tools(self):
        self.tools = [
            {
                "type": "function",
                "name": "list_files_in_dir",
                "description": "Lista los archivos que existen en un directorio dado (por defecto es el directorio actual) ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "directory": {
                            "type": "string",
                            "description": "Directorio para listar (opcional). por defecto es el directorio actual"
                        }
                    },
                    "required": []
                }
            },
            {
                "type": "function",
                "name": "read_file",
                "description": "Lee el contenido de un archivo en una ruta especificada",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "La ruta del archivo a leer"
                        }
                    },
                    "required": ['path']
                }
            },
            {
                "type": "function",
                "name": "edit_file",
                "description": "Edita el contenido de un archivo reemplazado prev_text por new_text. Crea el archivo si no existe.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "La ruta del archivo a editar"
                        },
                        "prev_text": {
                            "type": "string",
                            "description": "El texto que se va a buscar para reemplazar (puede ser vacio para archivos nuevos)"
                        },
                        "new_text": {
                            "type": "string",
                            "description": "El texto que reemplazará a prev_text (o el texto para un archivo nuevo)"
                        }
                    },
                    "required": ["path", "new_text"]
                }
            }
        ]

    #Definicion de herramientas
    def list_files_in_dir(self, directory="."):
        print("Herramienta llamada: list_files_in_dir")
        try:
            files = os.listdir(directory)
            return {"files": files}
        
        except Exception as e:
            return {"error": str(e)}
        
    #herramienta: leer archivos
    def read_files(self, path):
        print("     Herramienta llamada: read_file")
        try:
            with open(path, encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            err = f"Error al leer el archivo {path}"
            print(err)
            return err
        
    #Herrameinta: Editar archivos
    def edit_files(self, path, prev_text, new_text):
        print("     Herramienta llamada: edit_file")
        try:
            existed = os.path.exists(path)
            if existed and prev_text:
                content = self.read_files(path)

                if prev_text not in content:
                    return f"Texto {prev_text} no encontrado en el archivo"
                
                content = content.replace(prev_text, new_text)
            else:
                #Crear o sobreescribir con el nuevo texto directamente
                dir_name = os.path.dirname(path)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)
                
                content = new_text
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            action = "editado" if existed and prev_text else "creado"
            return f"archivo {path} {action} exitosamente"
        except Exception as e:
            err = f"Error al crear o editar el archivo {path}"
            print(err)
            return err

    def process_response(self, response):
        #True = si llama a una funcion. False = no hubo llamado
        
        #Almacenar para historial
        self.messages += response.output

        for output in response.output:
            if output.type == "function_call":
                fn_name = output.name
                args = json.loads(output.arguments)
        
                print(f"    - El modelo considera llamar a la herramienta {fn_name}")
                print(f"    - Argumentos: {args}")

                if fn_name == "list_files_in_dir":
                    result = self.list_files_in_dir(**args)
                elif fn_name == "read_file":
                    result = self.read_files(**args)
                elif fn_name == "edit_file":
                    result = self.edit_files(**args)


                #Agregar a la memoria la respuesta del llamado
                self.messages.append({
                    "type": "function_call_output",
                    "call_id": output.call_id,
                    "output": json.dumps({
                        "files": result
                    })
                })
                

                return True

            elif output.type == "message":
                #print(f"Asistente: {output.content}")
                reply = "\n".join(part.text for part in output.content)
                print(f"Asistente: {reply}")

        return False