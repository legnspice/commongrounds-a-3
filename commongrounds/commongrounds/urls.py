from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('merchstore/', include('merchstore.urls', namespace="merchstore")),
    path('localevents/', include('localevents.urls', namespace="localevents")),
    path("bookclub/", include("bookclub.urls", namespace="bookclub")),
    path('commissions/', include('commissions.urls', namespace="commissions")),
    path('admin/', admin.site.urls),
    path('diyprojects/', include('diyprojects.urls', namespace="diyprojects")),
    path('accounts/', include('django.contrib.auth.urls')),
]
