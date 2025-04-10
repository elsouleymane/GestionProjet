from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from gestion_ressources.views import logout_view, accueil

urlpatterns = [
    path('', accueil, name='accueil'),  # Page d'accueil
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('gestion/', include('gestion_ressources.urls')),
]