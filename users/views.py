from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import UserProfile


# Create your views here.
def register(request):
    if request.method != 'POST':
        form = UserForm()
    else:
        form = UserForm(data=request.POST)
        if form.is_valid():
            new_user = User()
            new_user.username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password'])
            new_user.email = form.cleaned_data['email']
            new_user.save()
            profile = UserProfile()
            profile.user_id = new_user.id
            profile.name = form.cleaned_data['name']
            profile.save()
            authenticated_user = authenticate(username=new_user.username,
                                              password=form.cleaned_data['password'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('tasks:index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)
