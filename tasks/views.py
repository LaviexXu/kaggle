from django.shortcuts import render
from .models import Task, Result, Report
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse,FileResponse
from .forms import TaskForm, ResultForm, ReportForm, EmailForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import csv
from .pdfdiff import read_pdf, get_similarity
from kaggle.settings import STATIC_ROOT, DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from smtplib import SMTPException
import os,sys


class SimilarPair():
    def __init__(self, origin_sentence, similar_sentence):
        self.origin_sentence = origin_sentence
        self.similar_sentence = similar_sentence


# Create your views here.
def index(request):
    return render(request, 'tasks/index.html')


def tasks(request):
    task_list = Task.objects.order_by('date_added')
    context = {'tasks': task_list}
    return render(request, 'tasks/task_list.html', context)


@login_required
def edit_task(request, task_id):
    # students can not edit any task
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('tasks:task_description', args=[task_id]))
    task = Task.objects.get(id=task_id)
    if request.method != 'POST':
        form = TaskForm(instance=task)
    else:
        form = TaskForm(instance=task, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks:task_list'))
    context = {'task': task,  'form': form}
    return render(request, 'tasks/teacher_only/edit_task.html', context)


def task_detail(request, task_id):
    # the page students and teachers can see are different
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('tasks:task_description', args=[task_id]))
    task = Task.objects.get(id=task_id)
    context = {'task': task}
    return render(request, 'tasks/teacher_only/task_detail.html', context)


@login_required
def new_email(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('tasks:task_list'))
    if request.method != 'POST':
        form = EmailForm()
        context = {'form': form}
        return render(request, 'tasks/teacher_only/new_email.html', context)
    else:
        form = EmailForm(data=request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            recipient_user_list = User.objects.filter(is_staff=False)
            recipient = []*len(recipient_user_list)
            for user in recipient_user_list:
                recipient.append(user.email)
            try:
                send_mail(subject, content, from_email=DEFAULT_FROM_EMAIL, recipient_list=recipient, fail_silently=False)
            except SMTPException:
                print("Unexpected error:", sys.exc_info()[0])
                return HttpResponse('email sending failed')
            return HttpResponse('email has been sent to all student.You can check it in your mail-box')


@login_required
def new_task(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('tasks:task_list'))
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks:task_list'))
    context = {'form': form}
    return render(request, 'tasks/teacher_only/new_task.html', context)


def task_description(request, task_id):
    task = Task.objects.get(id=task_id)
    context = {'task': task}
    return render(request, 'tasks/overview.html', context)


def task_data(request, task_id):
    # download data zip page
    task = Task.objects.get(id=task_id)
    context = {'task': task}
    return render(request, 'tasks/data.html', context)


def data_download(request, task_id):
    task = Task.objects.get(id=task_id)
    data_file = open(task.data_zip.path, 'rb')
    response = FileResponse(data_file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(task.data_zip.name)
    return response


def task_leaderboard(request, task_id):
    # filter students' results by task_id
    task = Task.objects.get(id=task_id)
    users = User.objects.all()
    results = []*len(users)
    for user in users:
        if Result.objects.filter(task=task, user=user).count() > 0:
            user_results = Result.objects.filter(task=task, user=user).order_by('score')
            results.append(user_results[0])

    results.sort(key=lambda result: result.score)
    context = {'task': task, 'results': results}
    return render(request, 'tasks/leaderboard.html', context)


@login_required
def submit_result(request, task_id):
    task = Task.objects.get(id=task_id)
    user = request.user
    # 如果超过规定的可以提交的次数，则无法提交
    if Result.objects.count() > 9:
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
            ref_result = []
            user_result = []
            with open(task.result_csv.path, newline='') as ref_csv:
                ref_csv_reader = csv.reader(ref_csv, quoting=csv.QUOTE_NONNUMERIC)
                for data in ref_csv_reader:
                    ref_result.append(data[0])
            with open(result.result_csv.path, newline='') as user_csv:
                user_csv_reader = csv.reader(user_csv, quoting=csv.QUOTE_NONNUMERIC)
                for data in user_csv_reader:
                    user_result.append(data[0])
            if len(user_result) == len(ref_result):
                mean_square_error = 0
                for i in range(len(ref_result)):
                    mean_square_error += (user_result[i]-ref_result[i])**2
                result.score = mean_square_error
                result.save()
            # else: 上传失败页面
            return HttpResponseRedirect(reverse('tasks:view_submissions', args=[task_id]))


@login_required
def view_submissions(request, task_id):
    task = Task.objects.get(id=task_id)
    user = request.user
    submit_history = Result.objects.filter(task=task, user=user).order_by('date_added')
    context = {'submissions': submit_history, 'task': task}
    return render(request, 'tasks/view_submissions.html', context)


@login_required
def submit_report(request, task_id):
    task = Task.objects.get(id=task_id)
    user = request.user
    if Report.objects.filter(task=task, user=user).count() > 0:
        context = {'task': task}
        return render(request, 'tasks/submit_successful.html', context)

    if request.method != 'POST':
        report_form = ReportForm()
        context = {'form': report_form, 'task': task}
        return render(request, 'tasks/submit_report.html', context)
    else:
        report_form = ReportForm(data=request.POST, files=request.FILES)
        report = report_form.save(commit=False)
        report.task = task
        report.user = user
        report.save()
        context = {'task': task}
        return render(request, 'tasks/submit_successful.html', context)


@login_required
# 此页面仅教师可见
def view_reports(request, task_id):
    task = Task.objects.get(id=task_id)
    reports = Report.objects.filter(task=task)
    context = {'reports': reports,'task': task}
    return render(request, 'tasks/teacher_only/view_reports.html', context)


# @login_required 此页面仅教师可见
def report_detail(request, task_id, student_id):
    task = Task.objects.get(id=task_id)
    student = User.objects.get(id=student_id)
    report = Report.objects.get(task=task, user=student)
    sentences = read_pdf(report.report.path)
    context = {'sentences': sentences}
    other_reports = Report.objects.filter(task=task).exclude(user=student)
    similar_pairs = []
    if len(other_reports) > 0:
        stopwords_file_path = os.path.join(STATIC_ROOT, 'stopwords.txt')
        stopwords_file = open(stopwords_file_path, encoding='utf-8')
        stopwords = {}.fromkeys([line.rstrip() for line in stopwords_file])
        stopwords_file.close()
        for other_report in other_reports:
            compare_sentences = read_pdf(other_report.report.path)
            for sentence in sentences:
                max_similarity = 0
                similar_sentence = ''
                for compare_sentence in compare_sentences:
                    cur_sim = get_similarity(sentence, compare_sentence, stopwords)
                    if cur_sim > 0.5 and cur_sim > max_similarity:
                        max_similarity = cur_sim
                        similar_sentence = compare_sentence
                if max_similarity > 0.5:
                    similar_pairs.append(SimilarPair(sentence, similar_sentence))
        context = {'similar_pairs': similar_pairs}
    return render(request, 'tasks/teacher_only/report_detail.html', context)
