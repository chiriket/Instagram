from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
   url('^$',views.index, name = 'home'),
   url(r'^image/(?P<image_id>\d+)', views.single_image, name='single_image'),
   url(r'^search/', views.search, name='search')
] 
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)