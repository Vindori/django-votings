from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import Question, Choice
from .forms import LoginForm, SignupForm
from .tokens import account_activation_token
from .serializers import QuestionSerializer, ChoiceSerializer

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken

import json
import random


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def list(self, request):
        queryset = self.queryset.filter(public=True).order_by('-cr_date')
        s = self.serializer_class(queryset, many=True)
        response = [
            {key: x[key] for key in ['access_token', 'topic']}
            for x in s.data
        ]
        return Response(response)


class AuthAPI(ObtainAuthToken):

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'error': 'You must be authenticated.'},
                status=401
            )
        else:
            questions = Question.objects.filter(author=user)
            q = QuestionSerializer(questions, many=True)
            response = [
                {key: x[key] for key in ['access_token', 'topic']}
                for x in q.data
            ]
            return Response({
                'username': str(user),
                'questions': response,
            })

    def put(self, request):
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')
        email = data.get('email', '')
        if not (username and password and email):
            return Response(
                {'error': 'Bad request.'},
                status=400
            )
        if User.objects.filter(username=username) | User.objects.filter(email=email):
            return Response(
                {'error': 'This user already exists.'},
                status=406
            )
        user = User(
            username=username,
            password=password,
            email=email,
            is_active=False
        )
        user.save()
        current_site = get_current_site(request)
        subject = 'Polls. Activate your account.'
        message = render_to_string('email/activate.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email = send_mail(
            subject,
            message,
            'vindori@vindori.ru',
            [email],
            fail_silently=True
        )
        if email:
            return Response(
                {'success': 'Please confirm your email address to complete the registration.'},
                status=200
            )
        else:
            user.delete()
            return Response(
                {'error': 'An error occurred. Try later'},
                status=500
            )


def activate(request, uidb64, token):
    try:
        print(uidb64)
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print(e)
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('votings:index')
    else:
        return 'Activation link is invalid!'


def index(request):
    context = {
        'loginform': LoginForm(),
        'signupform': SignupForm()
    }
    return render(request, 'index.html', context)
