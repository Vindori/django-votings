from django.urls import path, include
from rest_framework import routers

from . import views

app_name = "votings"

router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet, basename='questions')

urlpatterns = [
	path('', views.index, name='index'),
	path('api/vote/', views.VoteAPI.as_view(), name='vote-api'),
	path('api/', include(router.urls)),
]