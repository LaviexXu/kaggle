from django.shortcuts import render
from .models import Task
from django.http import HttpResponseRedirect, Http404
from .forms import TaskForm
from django.core.urlresolvers import reverse


# Create your views here.
def index(request):
    return render(request, 'tasks/index.html')


def tasks(request):
    task_list = Task.objects.order_by('date_added')
    context = {'tasks': task_list}
    return render(request, 'tasks/task_list.html', context)


def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method != 'POST':
        form = TaskForm(instance=task)
    else:
        form = TaskForm(instance=task, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks:task_list'))
    context = {'task': task,  'form': form}
    return render(request, 'tasks/edit_task.html', context)


def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    context = {'task': task}
    return render(request, 'tasks/task_detail.html', context)
