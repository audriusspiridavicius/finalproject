
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views
urlpatterns = [
    path('wow-shop/',views.HomepageView.as_view(), name='homepage'),
    path('',views.HomepageView.as_view(), name='homepage'),
    path('kategorijos/', views.CategoriesView.as_view(), name='categories')

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +  \
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)