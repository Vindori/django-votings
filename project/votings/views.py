from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse

from .models import Question
from .serializers import QuestionSerializer
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

import json
import random


class QuestionViewSet(viewsets.ModelViewSet):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer

	def list(self, request):
		queryset = self.queryset.filter(public=True).order_by('-cr_date')
		s = self.serializer_class(queryset, many=True)
		return Response(s.data)

	def my(self, response):
		queryset = self.queryset.filter(author=1).order_by('-cr_date')
		s = self.serializer_class(queryset, many=True)
		return Response(s.data)




def index(request):
	context = {}
	return render(request, 'index.html', context)
