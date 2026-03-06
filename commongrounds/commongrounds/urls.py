from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('merchstore/', include('merchstore.urls', namespace="merchstore")),
    path('localevents/', include('localevents.urls', namespace="localevents")),
    path('admin/', admin.site.urls),
    path('diyprojects/', include('diyprojects.urls')),
]