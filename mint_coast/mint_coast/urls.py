"""
URL configuration for mint_coast project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from .settings import DEBUG
from django.contrib.sitemaps.views import sitemap
from .sitemaps import MModelSitemap


sitemaps = {
    'mmodels': MModelSitemap
}


urlpatterns = [
    path('cart/', include('cart.urls')),
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name="mint_coast/robots.txt", content_type='text/plain')),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('mint_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls")),]
