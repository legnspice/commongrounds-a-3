from django.shortcuts import redirect

def role_required(required_role):
    def decorator(view_func):
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
        
            if not request.user.profile.has_role(required_role):
                return redirect("accounts:permission_denied")
            
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
