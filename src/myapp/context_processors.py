# Adiciona informações do usuário em todos os templates

def user_type_processor(request):
    return {
        'user_type': request.session.get('user_type', None),
        'user_nome': request.session.get('user_nome', None),
        'user_email': request.session.get('user_email', None),
        'user_id': request.session.get('user_id', None),
    }

