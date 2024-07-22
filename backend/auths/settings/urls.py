from django.urls import (
	path,
	include,
)


urlpatterns = (path('api/v1/auths/', include('app.urls')),)
