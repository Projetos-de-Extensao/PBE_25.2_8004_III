# Context processor para adicionar user_type em todos os templates

def user_type_processor(request):
    """
    Context processor para adicionar informações do usuário logado
    ao contexto de todos os templates
    """
    return {
        'user_type': request.session.get('user_type', None),
        'user_nome': request.session.get('user_nome', None),
        'user_email': request.session.get('user_email', None),
        'user_id': request.session.get('user_id', None),
    }

