from django.contrib import admin
from django.urls import (
    path,
    include,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('information_pages.urls')),
    path('', include('auths.urls')),
]
