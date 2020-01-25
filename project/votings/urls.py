from django.urls import path, include
from rest_framework import routers

from . import views

app_name = "votings"

router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet, basename='questions')

urlpatterns = [
	path('api/', include(router.urls)),
	path('', views.index, name='index')
]
