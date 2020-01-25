from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse

from .models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer
from .forms import LoginForm
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

import json
import random


def get_base_context(request):
    return {
        'loginform': LoginForm(),
        'user': request.user,
    }


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def list(self, request):
        queryset = self.queryset.filter(public=True).order_by('-cr_date')
        s = self.serializer_class(queryset, many=True)
        return Response(s.data)

    def my(self, request):
        queryset = self.queryset.filter(author=1).order_by('-cr_date')
        s = self.serializer_class(queryset, many=True)
        return Response(s.data)


def index(request):
    context = get_base_context(request)
    return render(request, 'index.html', context)
