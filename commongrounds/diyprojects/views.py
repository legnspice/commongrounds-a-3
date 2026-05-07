from django.shortcuts import get_object_or_404, render, redirect
from accounts.decorators import role_required
from django.db import models
from .models import Project, Favorite
from .forms import ProjectForm, ProjectReviewForm, ProjectRatingForm
from .repositories import ProjectRepository


def project_list(request):
    repo = ProjectRepository()
    projects = repo.get_all()
    context = {'projects': projects}

    if request.user.is_authenticated:
        profile = request.user.profile
        created = projects.filter(creator=profile)
        favorited = projects.filter(favorite__profile=profile)
        reviewed = projects.filter(projectreview__reviewer=profile)
        all_grouped = created | favorited | reviewed
        remaining = projects.exclude(pk__in=all_grouped.values('pk'))
        context['created'] = created
        context['favorited'] = favorited
        context['reviewed'] = reviewed
        context['remaining'] = remaining

    return render(request, 'diyprojects/project_list.html', context)


def project_detail(request, pk):
    repo = ProjectRepository()
    project = repo.get_by_id(pk)
    reviews = project.projectreview_set.all()
    ratings = project.projectrating_set.all()
    avg_rating = ratings.aggregate(models.Avg('score'))['score__avg']
    favorites_count = project.favorite_set.count()

    review_form = None
    rating_form = None
    user_favorite = None

    if request.user.is_authenticated:
        profile = request.user.profile
        review_form = ProjectReviewForm()
        rating_form = ProjectRatingForm()
        user_favorite = project.favorite_set.filter(profile=profile).first()

        if request.method == 'POST':
            if 'review_submit' in request.POST:
                review_form = ProjectReviewForm(request.POST, request.FILES)
                if review_form.is_valid():
                    review = review_form.save(commit=False)
                    review.reviewer = profile
                    review.project = project
                    review.save()
                    return redirect('diyprojects:project_detail', pk=pk)

            elif 'rating_submit' in request.POST:
                rating_form = ProjectRatingForm(request.POST)
                if rating_form.is_valid():
                    rating = rating_form.save(commit=False)
                    rating.profile = profile
                    rating.project = project
                    rating.save()
                    return redirect('diyprojects:project_detail', pk=pk)

            elif 'favorite_submit' in request.POST:
                if user_favorite:
                    user_favorite.delete()
                else:
                    Favorite.objects.create(profile=profile, project=project, project_status='Backlog')
                return redirect('diyprojects:project_detail', pk=pk)

    context = {
        'project': project,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'favorites_count': favorites_count,
        'review_form': review_form,
        'rating_form': rating_form,
        'user_favorite': user_favorite,
    }
    return render(request, 'diyprojects/project_detail.html', context)


@role_required("Project Creator")
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


@role_required("Project Creator")
def project_update(request, pk):
    repo = ProjectRepository()
    project = repo.get_by_id(pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('diyprojects:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'diyprojects/project_update.html', {'form': form, 'project': project})