from django.urls import include, path
from rest_framework.routers import SimpleRouter

from mainapp import views

router = SimpleRouter()

router.register('account', views.AccountViewSet, basename='account')
router.register('domains', views.DomainViewSet, basename='domains')
router.register('passwords', views.PasswordViewSet, basename='passwords')
router.register('password-share', views.PasswordShareViewSet, basename='password-share')

urlpatterns = [
    path('', include(router.urls)),
]
