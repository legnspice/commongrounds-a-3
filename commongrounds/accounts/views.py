from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileUpdateForm

@login_required
def profile_update_view(request, username):
    form = ProfileUpdateForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('accounts:profile_update', username=username)
    context = {
        'forms' : form
    }
    return render(request,"insert template here", context)
