from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class CustomCorsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Obtener los dominios permitidos desde CSRF_TRUSTED_ORIGINS
        allowed_origins = settings.CSRF_TRUSTED_ORIGINS
        
        # Obtener el valor del header 'Origin' de la solicitud
        origin = request.META.get("HTTP_ORIGIN")
        
        # Verificar si el origen está en la lista de dominios permitidos
        if origin and origin not in allowed_origins:
            # Si el origen no está permitido, devolver un error CORS
            return JsonResponse(
                {"error": "CORS policy does not allow this origin"},
                status=403
            )

        # Si todo está bien, dejar que la solicitud continúe
        return None
