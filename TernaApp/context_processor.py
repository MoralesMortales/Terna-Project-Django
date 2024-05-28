from .models import Estudiante, Profesor, Secretario 

def get_user_role(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'estudiante'):
            return {'user_role': 'student'}
        elif hasattr(request.user, 'profesor'):
            return {'user_role': 'professor'}
        elif hasattr(request.user, 'secretario'):
            return {'user_role': 'secretary'}
    return {'user_role': 'guest'}

def user_name(request):
    if request.user.is_authenticated:
        return {'user_name': request.user.first_name}
    return {}