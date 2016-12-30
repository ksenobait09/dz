"""dz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Hometask import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/register$', views.RegView.as_view(), name='register_url'),
    url(r'^login$', views.LogView.as_view(), name='login_url'),
    url(r'^$', views.BooksList.as_view(), name='main_page'),
    url(r'^add-new-book/$', views.add_new_book, name='add_new_book'),
    url(r'^book/(?P<book_id>[0-9]+)', views.ObjectView.as_view(), name='single_book'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
