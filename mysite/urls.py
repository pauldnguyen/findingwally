"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, path, re_path
from django.conf.urls import handler500

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

from findingwally import views as findingwally_views

urlpatterns += [
    re_path(r'^$', findingwally_views.home, name='home'),
    re_path(r'^more_information/$', findingwally_views.more_information, name='more_information'),
    re_path(r'^ajax/find_wally/$', findingwally_views.find_wally, name='find_wally'),
]

handler500 = findingwally_views.error_500

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
