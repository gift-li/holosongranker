"""holosongranker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
import mimetypes
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import set_language
from . import homepage

urlpatterns = [
    path("", homepage.Index, name='homepage'),
    path("about/", homepage.About, name='about'),
    path('admin/', admin.site.urls),
    path('songs/', include('songs.urls')),
    path('singers/', include('singers.urls')),
    path('setlang/', set_language, name="setlang"),
]

if settings.DEBUG:
    import debug_toolbar
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
