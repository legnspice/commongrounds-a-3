from django.contrib import admin
from .models import ProjectCategory, Project, Favorite, ProjectReview, ProjectRating


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'creator', 'created_on', 'updated_on')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('project', 'profile', 'date_favorited', 'project_status')


@admin.register(ProjectReview)
class ProjectReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'project')


@admin.register(ProjectRating)
class ProjectRatingAdmin(admin.ModelAdmin):
    list_display = ('profile', 'project', 'score')