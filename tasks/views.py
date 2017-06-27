import re
import datetime
from itertools import chain

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.db.models import Count

from .models import Task


def index(request):
    ''' タスク一覧の並び順を指定し, indexビューを返す '''
    latest_task_list = Task.objects.filter(finishing=False).order_by('deadline').annotate(null_deadline=Count('deadline')).order_by('-null_deadline', 'deadline', 'pub_date')[:100]
    context = {
        'latest_task_list': latest_task_list,
        'switch_text': 'Show Completed Tasks',
        'display_completed_tasks': 0,
    }
    return render(request, 'tasks/index.html', context)


def show_completed_tasks(request):
    ''' 完了したタスクを一覧に表示 '''
    uncompleted_task_list = Task.objects.filter(finishing=False).order_by('deadline').annotate(null_deadline=Count('deadline')).order_by('-null_deadline', 'deadline', 'pub_date')[:100]
    # = Task.objects.order_by('deadline').annotate(null_deadline=Count('deadline')).order_by('finishing', '-null_deadline', 'deadline', 'pub_date')[:100]
    completed_task_list = Task.objects.filter(finishing=True).order_by('-completion_date')[:100]
    latest_task_list = list(chain(uncompleted_task_list, completed_task_list))
    context = {
        'latest_task_list': latest_task_list,
        'switch_text': 'Hide Completed Tasks',
        'display_completed_tasks': 1,
    }
    return render(request, 'tasks/index.html', context)


def switch_display_completed_tasks(request, display_completed_tasks):
    ''' 完了したタスクを一覧に表示する/しない　を切り替える '''
    if display_completed_tasks == '0':
        return HttpResponseRedirect(reverse('tasks:show_completed_tasks'))
    else:
        return HttpResponseRedirect(reverse('tasks:index'))


def switch_finishing(request, task_id):
    ''' タスクに完了チェックを付ける/外す '''
    task = get_object_or_404(Task, pk=task_id)
    if task.finishing == False:
        task.finishing = True
        task.completion_date = timezone.now()
    else:
        task.finishing = False
    task.save()
    return HttpResponseRedirect(reverse('tasks:index'))


def add(request):
    ''' タスク追加フォームのデータをチェックし, タスクを追加 '''
    posted_task_text = request.POST['task_text']

    if re.match('\S+', posted_task_text):
        task_text = posted_task_text
        if request.POST['deadline']:
            deadline = request.POST['deadline']
        else:
            deadline = None            

        new_task = Task(task_text=task_text, pub_date=timezone.now(), deadline=deadline, finishing=False)
        new_task.save()

        return HttpResponseRedirect(reverse('tasks:index'))
    else:
        #Redisplay the add form.
        latest_task_list = Task.objects.filter(finishing=False).order_by('deadline').annotate(null_deadline=Count('deadline')).order_by('-null_deadline', 'deadline', 'pub_date')[:100]
        context = {
            'latest_task_list': latest_task_list,
            'switch_text': 'Show Completed Tasks',
            'display_completed_tasks': 0,
            'error_message': "You didn't set task.",
        }
        return render(request, 'tasks/index.html', context)


def edit(request, task_id):
    ''' 選択したタスクの編集画面を返す '''
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/edit.html', {'task': task})


def apply_edit(request, task_id):
    ''' タスクの編集フォームのデータをチェックし, 編集を反映させる '''
    task = get_object_or_404(Task, pk=task_id)

    if request.POST['task_text'] != task.task_text:
        posted_task_text = request.POST['task_text']
        if re.match('\S+', posted_task_text):
            task.task_text = posted_task_text
        else:
            #Redisplay the add form.
            return render(request, 'tasks/index.html', {
                'error_message': "You didn't set task.",
                })
    else:
        task_text = task.task_text

    # 以下のif節がごちゃごちゃしている気がするので, 直したい
    if request.POST['deadline']:
        if request.POST['deadline'] != task.deadline:
            task.deadline = request.POST['deadline']
        else:
            deadline = task.deadline
    else:
        deadline = task.deadline

    task.save()
    return HttpResponseRedirect(reverse('tasks:index'))


def delete(request, task_id):
    ''' 選択したタスクを削除 '''
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return HttpResponseRedirect(reverse('tasks:index'))
