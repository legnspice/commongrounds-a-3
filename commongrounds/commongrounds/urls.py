from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # --- LANDING PAGE ---
    # Redirects the root URL to your Community Events list
    path('', RedirectView.as_view(url='/localevents/events/'), name='index'),

    # --- ADMIN ---
    path('admin/', admin.site.urls),

    # --- ACCOUNTS & AUTH ---
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),

    # --- GROUP APPS ---
    path('bookclub/', include('bookclub.urls', namespace='bookclub')),
    path('commissions/', include('commissions.urls', namespace='commissions')),
    path('diyprojects/', include('diyprojects.urls', namespace='diyprojects')),
    path('localevents/', include('localevents.urls')),
    path('merchstore/', include('merchstore.urls', namespace='merchstore')),
]