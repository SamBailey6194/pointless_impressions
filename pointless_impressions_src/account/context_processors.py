def user_context(request):
    """
    Add common user-related variables to all templates.
    """
    context = {}

    if request.user.is_authenticated:
        context['user_public_id'] = str(request.user.public_id)

        context['has_artist_profile'] = hasattr(request.user, 'artist')
    return context
