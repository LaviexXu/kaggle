from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


# Create your views here.
def register(request):
    if request.method != 'POST':
        form = UserForm()
    else:
        form = UserForm(data=request.POST)
        if form.is_valid():
            new_user = User()
            new_user.username = form['username']
            new_user.set_password(form['password'])
            new_user.email = form['email']
            new_user.save()
            profile = new_user.get_profile()
            profile.name = form['name']
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('tasks:index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)
