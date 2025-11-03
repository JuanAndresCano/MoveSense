import os
##Cuando se hizo todo el proceso de acomodar los videos, nos vimos en la necesidad de estanarizar los nombres, y para esto sirvió este archivo
# Ruta de tus videos
folder_path = './Videos_IA'

# Extensiones permitidas
exts = ('.mp4', '.avi', '.mov', '.mkv')

# Crear unnoticed para contar los archivos por categoría
contador_por_categoria = {}

# Lista y ordena los archivos para procesar en orden
files = sorted(os.listdir(folder_path))

for filename in files:
    # Filtra solo archivos de video
    if filename.lower().endswith(exts):
        # Asumiendo que el nombre de categoría está antes del primer espacio o guion
        categoria = filename.split(' ')[0].lower()

        # Actualiza contador para esta categoría
        contador_por_categoria.setdefault(categoria, 0)
        contador_por_categoria[categoria] += 1

        numero = contador_por_categoria[categoria]
        nuevo_nombre = f"{categoria}_{numero}{os.path.splitext(filename)[1]}"

        # Ruta completa antes y después
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, nuevo_nombre)

        # Renombra si es diferente
        if old_path != new_path:
            print(f'Renombrando {filename} a {nuevo_nombre}')
            os.rename(old_path, new_path)