from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileUpdateForm

@login_required
def profile_update_view(request, username):
    if request.user.username != username:
        return redirect('accounts:profile_update', username=request.user.username)
    
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile_update', username=username)
    else:
        form = ProfileUpdateForm(instance=profile)  

    context = {'form': form}
    return render(request, 'update_user.html', context)

def permission_denied(request):
    return render(request,'permission_denied.html')