from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm


def project_list(request):
    projects = Project.objects.all()
    context = {'projects': projects}

    if request.user.is_authenticated:
        profile = request.user.profile
        created = Project.objects.filter(creator=profile)
        favorited = Project.objects.filter(favorite__profile=profile)
        reviewed = Project.objects.filter(projectreview__reviewer=profile)
        all_grouped = created | favorited | reviewed
        remaining = projects.exclude(pk__in=all_grouped.values('pk'))
        context['created'] = created
        context['favorited'] = favorited
        context['reviewed'] = reviewed
        context['remaining'] = remaining

    return render(request, 'diyprojects/project_list.html', context)


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'diyprojects/project_detail.html', {'project': project})


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user.profile
            project.save()
            return redirect('diyprojects:project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'diyprojects/project_create.html', {'form': form})


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('diyprojects:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'diyprojects/project_update.html', {'form': form, 'project': project})