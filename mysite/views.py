from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .forms import LoginForm
from .models import Poll, PollItem, VoteCheck
import datetime

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST['username'].strip()
            login_password = request.POST['password']
            user = authenticate(username = login_name, password = login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, "Successfully Login")
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, "The user is not found")
            else:
                messages.add_message(request, messages.WARNING, "Login Failed")
            #except:
                #messages.add_message(request, messages.WARNING, "The user is not found")
        else:
            messages.add_message(request, messages.INFO, "Please check the fields")
    else:
        login_form = LoginForm()

    return render(request, 'login.html', locals())

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "Successfully Logout")
    return redirect('/')

def index(request):
    all_polls = Poll.objects.all().order_by('-created_at')
    paginator = Paginator(all_polls, 5)
    p = request.GET.get('p')
    try:
        polls = paginator.page(p)
    except PageNotAnInteger:
        polls = paginator.page(1)
    except EmptyPage:
        polls = paginator.page(paginator.num_pages)
    return render(request, 'index.html', locals())

@login_required
def poll(request, pollid):
    try:
        poll = Poll.objects.get(id = pollid)
    except:
        poll = None
    if poll is not None:
        pollitems = PollItem.objects.filter(poll=poll).order_by('-vote')
    return render(request, 'poll.html', locals())

@login_required
def vote(request, pollid, pollitemid):
    target_url = '/poll/{}'.format(pollid)
    if VoteCheck.objects.filter(userid=request.user.id, pollid=pollid,vote_date=datetime.date.today()):
        return redirect(target_url)
    else:
        vote_rec = VoteCheck(userid=request.user.id, pollid=pollid,vote_date=datetime.date.today())
        vote_rec.save()
    try:
        pollitem = PollItem.objects.get(id = pollitemid)
    except:
        pollitem = None
    if pollitem is not None:
        pollitem.vote = pollitem.vote + 1
        pollitem.save()

    return redirect(target_url)

@login_required
def govote(request):
    if request.method == "GET" and request.is_ajax():
        pollitemid = request.GET.get('pollitemid')
        pollid = request.GET.get('pollitemid')
        bypass = False
        if VoteCheck.objects.filter(userid=request.user.id, pollid=pollid,vote_date=datetime.date.today()):
            bypass = True
        else:
            vote_rec = VoteCheck(userid=request.user.id, pollid=pollid,vote_date=datetime.date.today())
            vote_rec.save()
        try:
            pollitem = PollItem.objects.get(id = pollitemid)
            if not bypass:
                pollitem.vote = pollitem.vote+1
                pollitem.save()
            votes = pollitem.vote
        except:
            votes = 0
    else:
        votes = 0
    return HttpResponse(votes)







