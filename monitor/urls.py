from django.conf.urls import url, include
from django.urls import path

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'tokens', views.TokenViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('volumes/<int:pk>/',views.ListVolume.as_view()),
    path('update_volumes/<int:token_id>/',views.update_volumes),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]