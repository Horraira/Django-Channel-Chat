from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat', include('ChatApp.urls')),
    path('video/', include('base.urls')),
]
