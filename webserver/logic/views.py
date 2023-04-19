from django.contrib.auth.forms import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from voteapp.models import Vote, VoteType
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as signin, logout as signout
from django.contrib.auth.decorators import login_required
from logic.forms import SignupForm, SigninForm, VoteForm 
import logging


logger = logging.getLogger('my_app')

def error_http(request, exception=None):
    context_dict = dict()
    context_dict['msg_error'] = exception
    return render(request, "voteapp/error.html", context_dict)

def anonymous_required(f):
    def wrapped(request):
        if request.user.is_authenticated:
            return HttpResponseForbidden(error_http(
                request, exception="Action restricted to anonymous users"))
        else:
            return f(request)

    return wrapped

def index(request):
    return render(request, 'voteapp/index.html')

@anonymous_required
def login(request):
    if request.method == 'POST':
        user_form = SigninForm(data=request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            request.session.clear()
            signin(request, user)
            logger.info(f"Usuario {user.username} se ha autenticado correctamente")
            return redirect(reverse('index'))
        else:
            return render(request, 'voteapp/login.html',
                          context={'user_form': user_form,
                                   'return_service': 'voteapp/'})
    else:
        user_form = SigninForm()
        return render(request, 'voteapp/login.html',
                      context={'user_form': user_form,
                               'return_service': 'voteapp/'})


@anonymous_required
def signup(request):
    if request.method == 'POST':
        sign_up_form = SignupForm(request.POST)
        if sign_up_form.is_valid():
            username = sign_up_form.cleaned_data.get('username')
            password = sign_up_form.cleaned_data.get('password')
            user = User.objects.create_user(username=username,
                                            password=password)
            signin(request, user)
            return render(request, 'voteapp/signup.html')
        return render(request, 'voteapp/signup.html',
                      context={'user_form': sign_up_form})
    else:
        sign_up_form = SignupForm()
        return render(request, 'voteapp/signup.html',
                      context={'user_form': sign_up_form})


@login_required
def logout(request):
    signout(request)
    request.session.clear()
    request.session.save()
    return render(request, 'voteapp/index.html')


@login_required
def myvotes(request):
    user = request.user
    votes = Vote.objects.filter(user=user).order_by('-date')
    context = dict()
    context['votes'] = votes
    context['cats'] = Vote.objects.filter(voteType=VoteType.CATS).count()
    context['dogs'] = Vote.objects.filter(voteType=VoteType.DOGS).count()
    context['tie'] = Vote.objects.filter(voteType=VoteType.TIE).count()
    
    return render(request, 'voteapp/myvotes.html', context=context)


@login_required
def vote(request):
    if request.method == 'POST':
        try:
            choice = int(request.POST.get('choice'))
            Vote.objects.create(user=request.user, voteType=choice)
            vote_type = "gatos" if choice == VoteType.CATS else "perros" if choice == VoteType.DOGS else "empate"
            log_message = f"Usuario {request.user.username} votó por {vote_type}"
            logger.info(log_message)
            return redirect(reverse('index'))
        except ValidationError:
            return error_http(request, "Vote not valid")

    else:
        vote_form = VoteForm()
        return render(request, 'voteapp/vote.html',
                      context={'vote_form': vote_form}) 
