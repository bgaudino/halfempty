from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

from datetime import date, datetime, timedelta

from .models import Task, User, SharedTask, Friend, Tag

COLORS = ['#FF6633', '#FFB399', '#FF33FF', '#00B3E6', '#E6B333', '#3366E6', '#999966', '#B34D4D','#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC','#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399','#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933','#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Create your views here.
def login_view(request):
    if request.method == "POST":
    
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "todo/login.html", {
                "message": "Invalid username and/or password."
            })

    else:
        return render(request, "todo/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        if "terms" not in request.POST:
            return render(request, "todo/register.html", {
                "message": "You must agree to the terms and conditions to register for an account."
            })
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "todo/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "todo/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "todo/register.html")



@login_required(login_url='/login')
def index(request):
    day = date.today()
    return HttpResponseRedirect(reverse('view_tasks', args=[day, 'all']))
    


@login_required(login_url='/login')
def add(request):
    if request.method == 'POST':
        next = request.POST.get('next', '/')
        new_tag = False
        if request.POST['tag']:
            tags = Tag.objects.filter(user=request.user)
            if Tag.objects.filter(name=request.POST['tag']).first():
                new_tag = Tag.objects.filter(name=request.POST['tag']).first()
            else:
                new_tag = Tag.objects.create(name=request.POST['tag'], user=request.user, color=COLORS[len(tags)])
        task = Task.objects.create(user=request.user, title=request.POST['title'], description=request.POST['notes'], date=request.POST['date'])
        if new_tag:
            task.label = new_tag
        task.save()
        share = request.POST['recipient']
        if share:
            recipient = User.objects.filter(username=request.POST['recipient']).first()
            if recipient:
                if recipient == request.user:
                    return HttpResponse('You cannot share with yourself!')  
                friend = Friend.objects.filter(requester=request.user, requestee=recipient).first()
                if not friend:
                    new_friend = Friend.objects.create(requester=request.user, requestee=recipient)
                shared_task = SharedTask.objects.create(sender=request.user, recipient=recipient, task=task)
                if friend:
                    if friend.confirmed:
                        shared_task.accepted = True
                if shared_task:
                    shared_task.save()
            else:
                return HttpResponse(f"{request.POST['recipient']} is not a valid username")
            return HttpResponseRedirect(next)
    return HttpResponseRedirect(next)


@csrf_exempt
@login_required(login_url='/login')
def update(request, task_id):
    if request.method == 'POST':
        next = request.POST.get('next', '/')
        task = Task.objects.filter(id=task_id).first()
        task.title = request.POST['title']
        task.date = request.POST['date']
        task.description = request.POST['description']
        if request.POST['tag']:
            label = Tag.objects.filter(user=request.user, name=request.POST['tag']).first()
            if not label:
                label = Tag.objects.create(user=request.user, name=request.POST['tag'], color=COLORS[Tag.objects.filter(user=request.user).distinct().count()])
            task.label = label
        task.save()
        share = request.POST['recipient']
        recipient = User.objects.filter(username=request.POST['recipient']).first()
        if recipient and recipient != request.user:
            friend = Friend.objects.filter(requester=request.user, requestee=recipient).first()
            if not friend:
                friend = Friend.objects.create(requester=request.user, requestee=recipient)
            shared_task = SharedTask.objects.filter(sender=request.user, recipient=recipient, task=task).first()
            if not shared_task:
                shared_task = SharedTask.objects.create(sender=request.user, recipient=recipient, task=task)

        return HttpResponseRedirect(next)
    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
@login_required(login_url='/login')
def not_today(request, task_id):

    task = Task.objects.filter(id=task_id).first()
    print(task.date)
    task.date = task.date + timedelta(days=1)
    print(task.date)
    task.save()
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/login')
def view_tasks(request, day, tag):
    day = day.split('-')
    day = date(year=int(day[0]), day=int(day[2]), month=int(day[1]))
    if day == date.today():
        today = True 
    else: 
        today = False
    tomorrow = day + timedelta(days=1)
    yesterday = day + timedelta(days=-1)

    labels = Tag.objects.filter(user=request.user).distinct()

    if today:
        if tag == 'all':
            todo = Task.objects.filter(user=request.user, done=False, date__lte=day).order_by('date')
        else:
            tag_filter = Tag.objects.get(user=request.user, name=tag)
            todo = Task.objects.filter(user=request.user, done=False, date__lte=day, label=tag_filter).order_by('date')
    else:
        if tag == 'all':
            todo = Task.objects.filter(user=request.user, done=False, date=day).order_by('date')
        else:
            tag_filter = Tag.objects.filter(user=request.user, name=tag).first()
            todo = Task.objects.filter(user=request.user, done=False, date=day, label=tag_filter).order_by('date')

    
    for task in todo:
        if day == date.today() and task.date != day:
            task.overdue = True 
        else:
            task.overdue = False
        shared_with = SharedTask.objects.filter(task=task)
        task.shares = []
        if shared_with:
            for share in shared_with:
                task.shares.append(share.recipient.username)
    
    for task in todo:
        if len(task.shares) > 1:
                for i in range(len(task.shares) - 1):
                    task.shares[i] = f"{task.shares[i]},"

    this_week = []
    last_week = []
    i = 2
    while i < 7:
        this_week.append(date.today() + timedelta(days=i))
        last_week.append(date.today() - timedelta(days=i))
        i += 1
    if day == date.today():
        display_day = 'Today'
    elif day == date.today() + timedelta(days=1):
        display_day = 'Tomorrow'
    elif day == date.today() + timedelta(days=-1):
        display_day = 'Yesterday'
    elif day in this_week:
        display_day = WEEKDAYS[day.weekday()]
    elif day in last_week:
        display_day = f'Last {WEEKDAYS[day.weekday()]}'
    else:
        display_day = day

    shared_tasks = SharedTask.objects.filter(recipient=request.user)

    counter = 0
    for task in shared_tasks:
        if task.task.done:
            counter += 1
    if counter != len(shared_tasks):
        shared_header = True
    else:
        shared_header = False

    for task in todo:
        task.date = date.strftime(task.date, "%Y-%m-%d")
    
    for task in shared_tasks:
        task.task.date = date.strftime(task.task.date, "%Y-%m-%d")
    
    friend_requests = Friend.objects.filter(requestee=request.user, confirmed=False)

    friends = Friend.objects.filter(requestee=request.user, confirmed=True).distinct()
    friends_list = []
    for friend in friends:
        friends_list.append(friend.requester)
    confirmed_shares = []
    for shared_task in shared_tasks:
        if shared_task.sender in friends_list:
            confirmed_shares.append(shared_task)

    return render(request, "todo/index.html", {
        "tasks": todo,
        "labels": labels,
        "complete": False,
        "date": date.strftime(day, "%Y-%m-%d"),
        "tomorrow": tomorrow,
        "yesterday": yesterday,
        "shared_tasks": confirmed_shares,
        "display_day": display_day,
        "friend_requests": friend_requests,
        "shared_header": shared_header,
        "friends": friends,
        "friends_list": friends,
        "today": today                                                                                                                                                                                                                        
    })


@login_required(login_url='/login')
def bother_us(request):
    return render(request, "todo/bother_us.html")


@login_required(login_url='/login')
def date_picker(request):
    return HttpResponseRedirect(reverse('view_tasks', args=[request.POST['date'], 'all']));


@login_required(login_url='/login')
def logbook(request):
    tasks = Task.objects.filter(user=request.user, done=True).order_by('-date')
    if tasks:
        for task in tasks:
            task.formatted_date = date.strftime(task.date, "%Y-%m-%d")
        tasks[0].date_header = tasks[0].date
        i = 1
        while i < len(tasks):
            if tasks[i].date != tasks[i - 1].date:
                tasks[i].date_header = tasks[i].date
            i += 1
    paginator = Paginator(tasks, 12)

    labels = Tag.objects.filter(user=request.user)
    friends = Friend.objects.filter(requestee=request.user, confirmed=True)

    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)
    return render(request, "todo/logbook.html", {
        "tasks": pages,
        "labels": labels,
        "friends": friends
    })


@login_required(login_url='/login')
def open_page(request, task_id):
    task = Task.objects.filter(id=task_id).first()
    task.formatted_date = date.strftime(task.date, "%Y-%m-%d")
    return render(request, 'todo/page.html', {
        "task": task
    })


@login_required(login_url='/login')
def confirm(request):
    if request.method == 'POST':
        friend = Friend.objects.filter(id=request.POST['request_id']).first()
        friend.confirmed = True
        friend.save()
        new_friend = Friend.objects.create(requester=request.user, requestee=friend.requester, confirmed=True)
        new_friend.save()
    
        shared_tasks = SharedTask.objects.filter(sender=friend.requester, recipient=request.user)
        for task in shared_tasks:
            task.accepted = True
            task.save()

    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/login')
def decline(request):
    if request.method == 'POST':
        friend = Friend.objects.filter(id=request.POST['request_id']).first()
        friend.delete()

    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/login')
def account(request):
    user = request.user
    friends = Friend.objects.filter(requester=request.user).distinct()

    tags = Tag.objects.filter(user=request.user)
    return render(request, 'todo/account.html', {
        "friends": friends,
        "labels": tags
    })


@login_required(login_url='/login')
def check_off(request, id):
    task = Task.objects.get(id=id)
    if request.method == 'PUT':
        data = json.loads(request.body)
        task.done = data['done']
        task.save()
    return HttpResponse('')


@login_required(login_url='/login')
def quick_add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.create(title=data['task'], date=data['date'], user=request.user)
        task.save()
    return JsonResponse([task.serialize()], safe=False)


@login_required(login_url='/login')
def edit_tag(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        tag = Tag.objects.get(id=data['id'])
        tag.name = data['name']
        tag.color = data['color']
        tag.save()
        return JsonResponse([tag.serialize()], safe=False)
    return HttpResponseRedirect(reverse('account'))


@login_required(login_url='/login')
def delete_tag(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        tag = Tag.objects.get(id=data['id'])
        tag.delete()
        return HttpResponse('')

    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/login')
def delete_friend(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        requestee = User.objects.get(id=data['requestee_id'])
        requester = User.objects.get(id=data['requester_id'])
        friend1 = Friend.objects.get(requestee=data['requestee_id'], requester=data['requester_id'])
        friend2 = Friend.objects.filter(requestee=data['requester_id'], requester=data['requestee_id']).first()
        friend1.delete()
        if friend2:
            friend2.delete()
        return HttpResponse('')
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/login')
def add_friend(request):
    if request.method == 'POST':
        username = request.POST['friend']
        if username == request.user.username:
            return HttpResponse('You cannot share tasks with yourself')
        requestee = User.objects.filter(username=username).first()
        if requestee:
            is_friend = Friend.objects.filter(requestee=requestee, requester=request.user).first()
            if not is_friend:
                new_request = Friend.objects.create(requestee=requestee, requester=request.user)
                new_request.save()

    return HttpResponseRedirect(reverse('account'))


@login_required(login_url='/login')
def add_tag(request):
    if request.method == 'POST':
        tag_count = Tag.objects.filter(user=request.user).count()
        name = request.POST['name']
        tag = Tag.objects.filter(name=name, user=request.user).first()
        if not tag:
            new_tag = Tag.objects.create(name=name, user=request.user, color=COLORS[tag_count])
            new_tag.save()

    return HttpResponseRedirect(reverse('account'))


@login_required(login_url='/login')
def delete_account(request):
    if request.method == 'POST':
        account = User.objects.get(id=request.user.id)
        account.delete()
        return HttpResponseRedirect(reverse('login'))
    return HttpResponseRedirect(reverse('account'))


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        username = request.user.username
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if not user:
            return HttpResponse('invalid password')
        new_password = request.POST['new_password']
        confirmation = request.POST["confirmation"]
        if new_password != confirmation:
            return HttpResponse('passwords do not match')
        user = User.objects.get(id=request.user.id)
        user.password = make_password(new_password, salt=None, hasher='default')
        user.save()
        return render(request, "todo/login.html", {
            "message": "You have successfully changed your password. Please login with the new password."
        })
    return HttpResponseRedirect(reverse('account'))


@login_required(login_url='login')
def change_theme(request):
    if request.method == 'POST':
        user = request.user
        user.light_color = request.POST['light_color']
        user.dark_color = request.POST['dark_color']
        user.save()
    return HttpResponseRedirect(reverse('account'))


@login_required(login_url='login')
def default_theme(request):
    user = request.user
    user.light_color = None
    user.dark_color = None
    user.save()
    return HttpResponseRedirect(reverse('account'))


def privacy_policy(request):
    return render(request, 'todo/privacy.html')