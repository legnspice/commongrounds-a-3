from django.shortcuts import redirect

def role_required(required_role):
    def decorator(view_func):
        def wrapped(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.profile.role == required_role:
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect("accounts:permission_denied")
            else:
                return redirect("login")
        return wrapped
    return decorator
