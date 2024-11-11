import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class OpsFileHandler(FileSystemEventHandler):
    last_modified_time = None

    def on_modified(self, event):
        if event.src_path.endswith("ops.json"):
            current_time = time.time()

            if self.last_modified_time is None or (current_time - self.last_modified_time) > 1:
                self.last_modified_time = current_time
                print("Cambio detectado en ops.json. Actualizando niveles...")
                modificar_ops(event.src_path)

def modificar_ops(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        for player in data:
            if player['name'] != 'XKeros' and player['level'] == 4:
                player['level'] = 1

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        file.close()

        print("El archivo ops.json ha sido actualizado correctamente.")

    except FileNotFoundError:
        print(f"No se encontró el archivo en la ruta: {file_path}")
    except json.JSONDecodeError:
        print("Error al leer el archivo JSON. Asegúrate de que tenga un formato válido.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    path = "./"
    event_handler = OpsFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()

    try:
        print("Escuchando cambios en ops.json... Presiona Ctrl+C para detener.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nDeteniendo observador...")

    observer.join()
