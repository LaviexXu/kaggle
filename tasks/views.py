from django.shortcuts import render
from .models import Task,Result
from django.http import HttpResponseRedirect, Http404
from .forms import TaskForm,ResultForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


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
        form = TaskForm(instance=task, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks:task_list'))
    context = {'task': task,  'form': form}
    return render(request, 'tasks/edit_task.html', context)


def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    context = {'task': task}
    return render(request, 'tasks/task_detail.html', context)


def new_task(request):
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks:task_list'))
        else:
            context = {'form': form}
            return render(request, 'tasks/error.html', context)
    context = {'form': form}
    return render(request, 'tasks/new_task.html', context)


def task_description(request, task_id):
    task = Task.objects.get(id=task_id)
    context = {'task': task}
    return render(request, 'tasks/overview.html', context)


def task_data(request, task_id):
    # download data zip
    task = Task.objects.get(id=task_id)
    context = {'task': task}
    return render(request, 'tasks/data.html', context)


def task_leaderboard(request, task_id):
    # filter students' results by task_id
    task = Task.objects.get(id=task_id)
    context = {'task': task}
    return render(request, 'tasks/leaderboard.html', context)


def submit_result(request, task_id):
    task = Task.objects.get(id=task_id)
    user = request.user
    submit_history = Result.objects.filter(task=task, user=user)
    # 如果超过规定的可以提交的次数，则无法提交
    if len(submit_history) > 9:
        return render(request, 'tasks/submit_failed.html')
    if request.method != 'POST':
        result_form = ResultForm()
        context = {'form': result_form, 'task': task}
        return render(request, 'tasks/new_submission.html', context)
    else:
        result_form = ResultForm(data=request.POST, files=request.FILES)
        if result_form.is_valid():
            result = result_form.save(commit=False)
            result.task = task
            result.user = user
            result.save()
            return HttpResponseRedirect(reverse('tasks:view_submissions', args=[task_id]))


def view_submissions(request, task_id):
    task = Task.objects.get(id=task_id)
    user = request.user
    submit_history = Result.objects.filter(task=task, user=user)
    context = {'submissions': submit_history, 'task': task}
    return render(request, 'tasks/view_submissions.html', context)
