"""wearable_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fetch import views as fetchviews

from django.conf.urls import (
handler400, handler403, handler404, handler500
)

handler400 = 'fetch.views.bad_request'
handler403 = 'fetch.views.permission_denied'
handler404 = 'fetch.views.page_not_found'
handler500 = 'fetch.views.server_error'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', fetchviews.index, name='fetch-home'),

    path('publish/', fetchviews.index__, name='publish-home'),


]
