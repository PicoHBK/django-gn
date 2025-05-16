import base64
from PIL import Image
from io import BytesIO

def compress_images_base64(image_list: list) -> list:
    compressed_images = []

    # Mostrar el tamaño de la lista original en MB
    original_size_mb = sum(len(image) for image in image_list) / (1024 * 1024)
    print(f"Tamaño original de las imágenes: {original_size_mb:.2f} MB")

    for image_data in image_list:
        # Convertir la cadena base64 a bytes
        image_bytes = base64.b64decode(image_data)

        # Usar PIL para abrir la imagen
        image = Image.open(BytesIO(image_bytes))

        # Crear un buffer para guardar la imagen en formato WebP
        buf = BytesIO()

        # Guardar la imagen como WebP con compresión (puedes ajustar la calidad aquí)
        quality = 80  # La calidad de la imagen WebP (0-100)
        image.save(buf, format="WebP", quality=quality)

        # Obtener los datos de la imagen en WebP
        webp_image_data = buf.getvalue()

        # Convertir los datos a base64
        compressed_base64 = base64.b64encode(webp_image_data).decode('utf-8')

        # Agregar la imagen comprimida a la lista
        compressed_images.append(compressed_base64)

    # Mostrar el tamaño de la lista comprimida en MB
    compressed_size_mb = sum(len(image) for image in compressed_images) / (1024 * 1024)
    print(f"Tamaño comprimido de las imágenes: {compressed_size_mb:.2f} MB")

    return compressed_images  # Retorna la lista de imágenes en base64
