from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import UserProfile


# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('tasks:index'))
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
            new_user.userprofile.name = form.cleaned_data['name']
            new_user.userprofile.save()
            authenticated_user = authenticate(username=new_user.username,
                                              password=form.cleaned_data['password'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('tasks:index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))