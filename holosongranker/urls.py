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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from . import homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "ads.txt",
        RedirectView.as_view(url=staticfiles_storage.url("ads.txt")),
    ),
]

urlpatterns += i18n_patterns(
    path('', homepage.Index, name='homepage'),
    path('about', homepage.About, name='about'),
    path('songs/', include('songs.urls', namespace='songs')),
    path('singers/', include('singers.urls', namespace='singers')),
)

handler404 = 'holosongranker.error_handler.view_404'

# if settings.DEBUG:
#     import debug_toolbar
#     DEBUG_TOOLBAR_CONFIG = {
#         'INTERCEPT_REDIRECTS': False,
#     }
#     urlpatterns += [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ]
