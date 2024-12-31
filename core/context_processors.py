def is_cofounder(request):
    if request.user.is_authenticated:
        return {'is_cofounder': request.user.groups.filter(name="Co-Founders").exists()}
    return {'is_cofounder': False}
