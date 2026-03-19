import requests
import base64

def get_base64_from_url(image_url: str):
    try:
        # Realizamos la solicitud HTTP para obtener la imagen
        response = requests.get(image_url)
        
        # Verificamos si la solicitud fue exitosa (código 200)
        if response.status_code == 200:
            # Convertir la imagen a base64 y retornar la cadena
            img_base64 = base64.b64encode(response.content).decode('utf-8')
            return img_base64
        else:
            # Si el código de estado no es 200, retornamos None
            return None
    except requests.RequestException:
        # Si ocurre algún error (como problemas de red, URL incorrecta, etc.), retornamos None
        return None
