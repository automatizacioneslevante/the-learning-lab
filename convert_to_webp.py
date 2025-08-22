from PIL import Image
import os

# Carpeta donde tienes los JPG
input_folder = "imagenes_jpg"
# Carpeta donde se guardarán los WEBP
output_folder = "imagenes_webp"

# Crear carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Recorrer archivos en la carpeta
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith((".jpg", ".jpeg")):
        img_path = os.path.join(input_folder, file_name)
        img = Image.open(img_path).convert("RGB")  # Convertir a RGB por si acaso

        # Nuevo nombre con extensión .webp
        new_name = os.path.splitext(file_name)[0] + ".webp"
        output_path = os.path.join(output_folder, new_name)

        # Guardar en formato WebP con calidad 80
        img.save(output_path, "webp", quality=80)

        print(f"Convertido: {file_name} → {new_name}")

print("Conversión terminada.")