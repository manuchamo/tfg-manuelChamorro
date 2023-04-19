import logging

logger = logging.getLogger(__name__)

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

@login_required
def vote(request):
    if request.method == 'POST':
        try:
            choice = int(request.POST.get('choice'))
            vote = Vote.objects.create(user=request.user, voteType=choice)
            vote_type = "gatos" if choice == VoteType.CATS else "perros" if choice == VoteType.DOGS else "empate"
            logger.info(f"Usuario {request.user.username} votó por {vote_type}")
            return redirect(reverse('index'))
        except ValidationError:
            return error_http(request, "Vote not valid")

    else:
        vote_form = VoteForm()
        return render(request, 'voteapp/vote.html',
                      context={'vote_form': vote_form}) 