from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('bookclub/', include('bookclub.urls', namespace='bookclub')),
    path('commissions/', include('commissions.urls', namespace='commissions')),
    path('diyprojects/', include('diyprojects.urls', namespace='diyprojects')),
    path('localevents/', include('localevents.urls')),
    path('merchstore/', include('merchstore.urls', namespace='merchstore')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
