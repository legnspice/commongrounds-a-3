from django.shortcuts import redirect

class RoleRequiredMixin:
    required_role = None
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        
        if request.user.profile.role != self.required_role:
            return redirect("accounts:permission_denied")
        
        return super().dispatch(request, *args, **kwargs)