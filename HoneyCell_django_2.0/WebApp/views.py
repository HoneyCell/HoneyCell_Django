from django.shortcuts import render

from django.conf import settings

# allow us to redirect
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.http import Http404
from django.template import RequestContext, loader

# import the User class in models.py
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# import the auth.models User
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from WebApp.models import *

import requests

import threading


# registration is normal route, and login is login is "django.contrib.views.login"
def registration(request):
    errors = []
    context = {}
    if request.method == "GET":
        return render(request, 'WebApp/register.html', context)

    # add 'errors' attribute to the context
    context['errors'] = errors

    password1 = request.POST['password']
    password2 = request.POST['password_confirmation']

    if password1 != password2:

        print("Passwords did not match.")

        # error1 happens
        errors.append("Passwords did not match.")

    if len(User.objects.all().filter(username = request.POST['user_name'])) > 0:
        print("Username is already taken.")

        # error2 happens
        errors.append("Username is already taken.")

    if len(User.objects.all().filter(email = request.POST['email'])):
        print("The email already register.")

        errors.append("The email already register.")

    if errors:
        return render(request, 'WebApp/register.html', context)

    # create a new user from the valid form data, using create_user function with 2 arguments, 'username' and 'password'
    new_user = User.objects.create_user(username=request.POST['user_name'],
                                        password=request.POST['password'],
                                        first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        email=request.POST['email'])
    new_user.save()

    # using 'authenticate' function
    new_user = authenticate(username = request.POST['user_name'],
                            password = request.POST['password'],)

    new_activity_instance = Activity(user=new_user)


    # add activity description
    new_activity_instance.description = "<a href='http://127.0.0.1:8000/all_profile/" \
                                        + str(new_user.id) \
                                        + "'>" \
                                        + new_user.username \
                                        + "</a>"\
                                        + " register an account."
    new_activity_instance.save()

    # create Profile object for the user
    new_profile_instance = Profile(user=new_user,
                                   )
    new_profile_instance.save()

    # create default folder
    new_folder_instance = Folder(user=new_user,
                                 folder_name="Default",
                                 )
    new_folder_instance.save()
    print("Already save new_folder_instance.")

    # using 'login' function
    login(request, new_user)

    # using 'redirect' function
    return redirect(reverse('index'))


# def logout view
def my_logout(request):
    logout(request)
    return redirect(reverse('index'))


# go to index page
@login_required
def index(request):
    print("in the index function")
    context = {}
    user = request.user
    context['user'] = user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self


    return render(request, 'WebApp/index.html', context)


# go to new task page
@login_required
def newTask(request):
    print("in the newTask function")
    context = {}
    user = request.user
    context['user'] = user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self

    folders = Folder.objects.filter(user=user)
    context['folders'] = folders

    labels = []
    for tempEntry in LABEL_CHOICES:
        labels.append(tempEntry[1])
    context['labels'] = labels

    algorithms = []
    for tempEntry in ALGORITHM_CHOICES:
        algorithms.append(tempEntry[1])
    context['algorithms'] = algorithms

    return render(request, 'WebApp/newTask.html', context)


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# go to task history page
@login_required
def historyTask(request):
    print("in the historyTask function")
    context = {}
    user = request.user
    context['user'] = user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self

    tasks = Task.objects.filter(user=request.user).order_by("id").reverse().order_by("id").reverse()

    paginator = Paginator(tasks, 8)
    page = request.GET.get('page')

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    context['tasks'] = tasks

    if len(tasks) == 0:
        context['empty'] = True

    context['LABEL_CHOICES'] = LABEL_CHOICES
    context['ALGORITHM_CHOICES'] = ALGORITHM_CHOICES
    context['STATUS_CHOICES'] = STATUS_CHOICES

    print("%" * 30)
    print(STATUS_CHOICES)
    print("%" * 30)

    return render(request, 'WebApp/historyTask.html', context)


# go to file manage page
@login_required
def fileManage(request):
    print("in the fileManage function")
    context = {}
    user = request.user
    context['user'] = user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self

    all_folders = Folder.objects.filter(user=request.user)
    context['all_folders'] = all_folders

    folders = Folder.objects.filter(user=request.user)
    paginator = Paginator(folders, 8)
    page = request.GET.get('page')
    try:
        folders = paginator.page(page)
    except PageNotAnInteger:
        folders = paginator.page(1)
    except EmptyPage:
        folders = paginator.page(paginator.num_pages)
    context['folders'] = folders

    print("%" * 30)
    print(folders)
    for folder in folders:
        print(folder)
        print(folder.folder_name)
        print(folder.id)
        print("*" * 10)
    print("%" * 30)

    return render(request, 'WebApp/fileManage.html', context)


# go to file management task page.
@login_required
def fileManage_tasks(request, folder_id):
    print("in the fileManage_tasks function")
    context = {}
    user = request.user
    context['user'] = user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self


    folders = Folder.objects.filter(user=request.user)
    context['folders'] = folders

    folder = Folder.objects.get(id=folder_id)
    context['folder'] = folder

    tasks = Task.objects.filter(task_folder=folder)
    paginator = Paginator(tasks, 8)
    page = request.GET.get('page')

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    context['tasks'] = tasks

    context['LABEL_CHOICES'] = LABEL_CHOICES
    context['ALGORITHM_CHOICES'] = ALGORITHM_CHOICES
    context['STATUS_CHOICES'] = STATUS_CHOICES

    return render(request, 'WebApp/fileManage_tasks.html', context)

# go to the profile to show all followers
@login_required
def profile_allFollowers(request):
    print("in the profile_allFollowers function.")
    context = {}
    user = request.user
    context['user'] = user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self

    activities = Activity.objects.all()
    context['activities'] = activities

    followers = Followship.objects.filter(follower=request.user)
    context['followers'] = followers

    return render(request, 'WebApp/profile_allFollowers.html', context)


# go to profile to show all followings
@login_required
def profile_allFollowings(request):
    print("in the profile_allFollowings function.")
    context = {}
    user = request.user
    context['user'] = user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self

    activities = Activity.objects.all()
    context['activities'] = activities

    return render(request, 'WebApp/profile_allFollowings.html', context)



from WebApp.forms import *
from django.utils import timezone

# create new task
@login_required
def create_new_task(request):
    print("in the create_new_task function")

    context = {}
    context['user'] = request.user

    errors = []
    context['errors'] = errors

    user = request.user
    task_name = request.POST['task_name']
    task_algorithm = request.POST['task_algorithm']
    task_description = request.POST['task_description']
    task_folder = request.POST['task_folder']
    task_label = request.POST['task_label']

    training_docfile = request.FILES['training_docfile']
    testing_docfile = request.FILES['testing_docfile']

    print("%" * 30)
    print(training_docfile)
    print(testing_docfile)
    print("%" * 30)

    task_folder_object = Folder.objects.get(user=request.user, folder_name=task_folder)


    context['user'] = user
    context['task_name'] = task_name
    context['task_algorithm'] = task_algorithm
    context['task_description'] = task_description
    context['task_folder'] = task_folder
    context['task_label'] = task_label

    context['training_docfile'] = training_docfile
    context['testing_docfile'] = testing_docfile

    context['folders'] = Folder.objects.filter(user=request.user)

    labels = []
    for tempEntry in LABEL_CHOICES:
        labels.append(tempEntry[1])
    context['labels'] = labels

    algorithms = []
    for tempEntry in ALGORITHM_CHOICES:
        algorithms.append(tempEntry[1])
    context['algorithms'] = algorithms

    if not task_name:
        errors.append("Please type in the task name.")

    if not training_docfile:
        errors.append("Please upload a training file for the task.")

    if not testing_docfile:
        errors.append("Please upload a testing file for the task.")

    if len(Task.objects.filter(user=user, task_name=task_name)):
        errors.append("The task_name for this user already exist.")

    # Do not select a task algorithm
    if task_algorithm == "None":
        errors.append("Please select the task algorithm.")

    if errors:
        return render(request, 'WebApp/newTask.html', context)

    task_label_index = 0
    for tempEntry in LABEL_CHOICES:
        if task_label == tempEntry[1]:
            task_label_index = tempEntry[0]
        else:
            # do nothing
            pass

    print("%" * 30)
    print(task_label_index)
    print("%" * 30)

    task_algorithm_index = 0
    for tempEntry in ALGORITHM_CHOICES:
        if task_algorithm == tempEntry[1]:
            task_algorithm_index = tempEntry[0]
        else:
            # do nothing
            pass

    print("%" * 30)
    print(task_algorithm_index)
    print("%" * 30)

    new_task_instance = Task(user=user,
                             task_name=task_name,
                             task_algorithm=task_algorithm_index,
                             task_description=task_description,
                             task_label=task_label_index,
                             task_folder=task_folder_object,

                             training_docfile=training_docfile,
                             testing_docfile=testing_docfile,

                             # default status is pending
                             task_status=STATUS_CHOICES[0][0]
                             )
    new_task_instance.save()
    print("Already save the new_task_instance.")


    print(ALGORITHM_CHOICES[new_task_instance.task_algorithm - 1][1])

    new_activity_instance = Activity(user=request.user,
                                     task=new_task_instance,
                                     )




    new_activity_instance.description = "<a href='http://127.0.0.1:8000/all_profile/" \
                                        + str(request.user.id) \
                                        + "'>" \
                                        + request.user.username\
                                        + "</a>" \
                                        + "create a new task " \
                                        + "<a href='http://127.0.0.1:8000/taskDetail/" \
                                        + str(new_task_instance.id) \
                                        + "'>" \
                                        + new_task_instance.task_name \
                                        + ".</a>"

    new_activity_instance.save()
    print("Already save new_activity_instance.")


    backend_url = 'http://128.2.7.38:32768/'
    address_prefix = '/home/honeycomb/DEMODAY/honeycell/HoneyCell_Django/HoneyCell_django_2.0/media/documents/' + str(context['user']) + '/' + str(context['task_folder'])
    tranining_address = address_prefix+'/trainings/'+str(training_docfile)
    testing_address = address_prefix+'/testings/'+str(testing_docfile)
    algorithm_chosen = ALGORITHM_CHOICES[new_task_instance.task_algorithm - 1][1]

    print ('preparing to send task creation request to honey')
    print ('user: ' + str(context['user']))
    print ('task_id: ' + str(new_task_instance.id))
    print ('training data address: ' + tranining_address)
    print ('testing data address: ' + testing_address)
    print ('sending task creation request to: ' + backend_url)
    print ('algorithm choose is :' + algorithm_chosen)
    print ('')

    
    print ('sending task creation request to: ' + backend_url)
    print ('')

    my_json = {'task_id':new_task_instance.id, 'train_address': tranining_address, 'test_address': testing_address, 'algorithm': algorithm_chosen}

    # create a new thread to request for HoneyComb
    new_thread = threading.Thread(target = new_thread_for_new_task, kwargs={'my_json': my_json})
    new_thread.daemon = True
    new_thread.start()

    return HttpResponseRedirect(reverse('taskDetail', kwargs={'task_id': new_task_instance.id}))


import time

def new_thread_for_new_task(my_json):

    print("in the new_thread_for_new_task function.")

    backend_url = 'http://128.2.7.38:32768/'
    r_call_backend = requests.post(backend_url, data=my_json)
    print(r_call_backend.content)
    # time.sleep(5)
    print("new_thread_for_new_task Done")




# go to guide page
@login_required
def guide(request):
    print("in the guide function")
    return render(request, 'WebApp/guide.html')

# go to settings page
@login_required
def settings(request):
    print("in the settings function")
    context = {}
    user = request.user
    context['user'] = user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self


    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    context['public_profile'] = True
    context['password'] = False

    return render(request, 'WebApp/settings.html', context)


# go to global page
@login_required
def global_page(request):
    print("in the global function.")
    context = {}
    user = request.user

    users = User.objects.all()
    context['users'] = users

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self


    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    activities = Activity.objects.all().order_by("time_created").reverse()
    context['activities'] = activities

    print("%" * 30)
    for activity in activities:
        print(activity.description)
        comments = Comment.objects.filter(activity=activity)
        print(activity.comment_set.all())
        print(comments)
    print("%" * 30)

    print("%" * 30)
    print(Comment.objects.all())
    for comment in Comment.objects.all():
        print(comment.user)
        print(comment.activity.description)
        print(comment.text)
    print("%" * 30)

    return render(request, 'WebApp/global_page.html', context)


# view to follow other user
@login_required
def follow(request, user_id):
    print("in the follow function.")

    print(request)
    print(user_id)

    context = {}
    context['current_user'] = request.user

    errors = []
    context['errors'] = errors

    other_user = User.objects.get(id=user_id)

    if Followship.objects.filter(following=request.user,
                                 follower=other_user):
        errors.append("The followship already exist.")

        return HttpResponseRedirect(reverse('global_page'))

    new_followship_instance = Followship(following=request.user,
                                         follower=other_user)
    new_followship_instance.save()
    print("Already save new_followship_instance.")

    new_activity_instance = Activity(user=request.user)
    new_activity_instance.description = "<a href='http://127.0.0.1:8000/all_profile/" \
                                        + str(request.user.id) \
                                        + "'>" \
                                        + request.user.username\
                                        + "</a>" \
                                        + " follow "\
                                        + "<a href='http://127.0.0.1:8000/all_profile/" \
                                        + str(other_user.id) + "'>"\
                                        + other_user.username\
                                        + ".</a>"
    new_activity_instance.save()


    return HttpResponseRedirect(reverse("other_profile", kwargs={'user_id': other_user.id}))


# view to unfollow other user
@login_required
def unfollow(request, user_id):
    print("in the unfollow function.")

    print(request)
    print(user_id)

    context = {}
    context['current_user'] = request.user

    other_user = User.objects.get(id=user_id)

    followship = Followship.objects.get(following=request.user,
                                        follower=other_user)
    followship.delete()
    print("The Followship object already delete.")

    new_activity_instance = Activity(user=request.user)
    new_activity_instance.description = "<a href='http://127.0.0.1:8000/all_profile/" \
                                        + str(request.user.id) \
                                        + "'>" \
                                        + request.user.username\
                                        + "</a>" \
                                        + " follow "\
                                        + "<a href='http://127.0.0.1:8000/all_profile/" \
                                        + str(other_user.id) + "'>"\
                                        + other_user.username\
                                        + ".</a>"
    new_activity_instance.save()


    return HttpResponseRedirect(reverse("other_profile", kwargs={'user_id': other_user.id}))


from django.http import Http404
from mimetypes import guess_type

# get back the user picture
@login_required
def get_user_picture(request, user_id):
    print("in the get_user_picture function.")
    context = {}
    errors = []
    context['errors'] = errors
    try:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
    except Exception:
        errors.append("profile not existed")
    content_type = guess_type(profile.image.name)
    return HttpResponse(profile.image, content_type=content_type)


# view to update profile information
@login_required
def update_profile(request):
    print("in the update_profile function.")
    context = {}

    errors = []
    context['errors'] = errors

    context['user'] = request.user
    profile = Profile.objects.get(user=request.user)

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    company = request.POST['company']
    location = request.POST['location']
    website = request.POST['website']

    if request.FILES.__contains__('user_image'):
        user_image = request.FILES['user_image']
    else:
        user_image = profile.image

    request.user.first_name = first_name
    request.user.last_name = last_name
    request.user.email = email

    request.user.save()

    profile.company = company
    profile.location = location
    profile.website = website
    profile.image = user_image

    profile.save()
    print("Already update the profile.")

    new_activity_instance = Activity(user=request.user)
    new_activity_instance.description = "<a href='http://127.0.0.1:8000/all_profile/" \
                                        + str(request.user.id) \
                                        + "'>" \
                                        + request.user.username\
                                        + "</a>" \
                                        + " update the profile."
    new_activity_instance.save()


    return HttpResponseRedirect(reverse('profile'))


# view to change_password
@login_required
def change_password(request):
    print("in the change_password function.")
    context = {}

    user = request.user
    context['user'] = user

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    errors = []
    context['errors'] = errors

    new_password1 = request.POST['new_password1']
    new_password2 = request.POST['new_password2']

    print("%" * 30)
    print(request.user.password)
    print(new_password1)
    print(new_password2)
    print("%" * 30)

    if new_password1 != new_password2:
        errors.append("Two password did not match, please type in again.")
        context['public_profile'] = False
        context['password'] = True
        return render(request, 'WebApp/settings.html', context)
    else:
        user.set_password(new_password1)
        user.save()
        print("Already reset the password.")

        new_activity_instance = Activity(user=request.user)
        new_activity_instance.description = "<a href='http://127.0.0.1:8000/all_profile/" \
                                            + str(request.user.id) \
                                            + "'>" \
                                            + request.user.username\
                                            + "</a>" \
                                            + " change the password."
        new_activity_instance.save()

        user = authenticate(username = user.username,
                            password = new_password1,)
        login(request, user)
        return HttpResponseRedirect(reverse('settings'))



import os.path
from django.http import JsonResponse


# go to task detail page
@login_required
def taskDetail(request, task_id):
    print("in the taskDetail function")
    context = {}
    user = request.user
    context['user'] = user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self


    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    task = Task.objects.get(id=task_id)
    context['task'] = task

    context['task_algorithm'] = ALGORITHM_CHOICES[task.task_algorithm - 1][1]
    context['task_status'] = STATUS_CHOICES[task.task_status - 1][1]
    context['task_label'] = LABEL_CHOICES[task.task_label - 1][1]

    print(task)

    context['task_id'] = task_id

    return render(request, 'WebApp/taskDetail.html', context)



from django.db import connections
from django.http import JsonResponse
from django.db.models import Count

import os.path

import csv

# function to load json file
def get_json_result(request, task_id):

    print(task_id)
    print("in the get_json_result function.")

    # try:
    finished_task = Task.objects.get(id = task_id)

    json_url = ""

    print(finished_task)

    # get result address
    if finished_task.output_file_address:
        json_url = finished_task.output_file_address
    
    print(json_url)


    if json_url != "":
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        try:
            json_data = open(os.path.join(BASE_DIR, json_url))
            data = json_data.read()
            print(data)
            return JsonResponse((data), safe=False)

        # file path has problem hard code
        except (OSError, IOError) as e:

            print("Read local JSON file.")


            algorithm_string = ALGORITHM_CHOICES[finished_task.task_algorithm][1]

            if algorithm_string == "RandomForest":
                # get local json result file for RandomForest algorithm
                json_url = 'WebApp/static/WebApp/json/RandomForest.json'
            else:
                # get local json result file for LogisticRegression algorithm
                json_url = 'WebApp/static/WebApp/json/LogisticRegression.json'



            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_data = open(os.path.join(BASE_DIR, json_url))
            data = json_data.read()
            return JsonResponse((data), safe=False)

    # task is still running (no task finish address in db)
    else:
        pass




# view to update task
@login_required
def update_task(request, task_id):
    print("in the update_task function.")
    context = {}
    context['user'] = request.user

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    errors = []
    context['errors'] = errors

    task = Task.objects.get(id=task_id)
    context['task'] = task

    task_name = request.POST['task_name']
    task_description = request.POST['task_description']


    if ( task.task_name != task_name and len(Task.objects.filter(task_name=task_name))):
        # The way to return back the error message needs to be changed later
        errors.append("The task name already exist, please type in another task name.")
        print("The task name already exist, please type in another task name.")
        return HttpResponseRedirect(reverse('taskDetail', kwargs={'task_id': task_id}))


    if ( task.task_description != task_description and len(Task.objects.filter(task_description=task_description)) ):
        # The way to return back the error message needs to be changed later
        errors.append("The task description already exist, please type in another task description.")
        print("The task description already exist, please type in another task description.")
        return HttpResponseRedirect(reverse('taskDetail', kwargs={'task_id': task_id}))

    task.task_name = task_name
    task.task_description = task_description
    task.save()
    print("Already update task's information.")

    new_activity_instance = Activity(user=request.user)
    new_activity_instance.description = request.user.username + " update " + task.task_name + "'s information."
    new_activity_instance.save()


    return HttpResponseRedirect(reverse('taskDetail', kwargs={'task_id': task_id}))


# go to new folder page
@login_required
def new_folder(request):
    print("in the new_folder function.")

    context = {}
    context['user'] = request.user

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    errors = []
    context['errors'] = errors

    folder_name = request.POST['folder_name']

    if(Folder.objects.filter(folder_name=folder_name)):
        # The way to return back the error message needs to be changed later
        errors.append("This folder name already exist, please type in another folder name.")
        print("This folder name already exist, please type in another folder name.")
        return HttpResponseRedirect(reverse('fileManage'))

    new_folder_instance = Folder(user=request.user,
                                 folder_name=folder_name)
    new_folder_instance.save()
    print("Already save the new_folder_instance.")

    new_activity_instance = Activity(user=request.user)
    new_activity_instance.description = "<a href='http://127.0.0.1:8000/all_profile/" \
                                        + str(request.user.id) \
                                        + "'>" \
                                        + request.user.username\
                                        + "</a>"\
                                        + " create a new folder " \
                                        + "<a href='http://127.0.0.1:8000/fileManage_tasks/" \
                                        + str(new_folder_instance.id) \
                                        + "'>" \
                                        + new_folder_instance.folder_name \
                                        + "</a>."
    new_activity_instance.save()


    return HttpResponseRedirect(reverse('fileManage'))


# view to update folder information
@login_required
def update_folder(request, folder_id):
    print("in the update_folder function.")
    print("folder_id: " + folder_id);
    context = {}
    context['user'] = request.user

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    errors = []
    context['errors'] = errors

    folder = Folder.objects.get(id=folder_id)

    old_folder_name = folder.folder_name

    folder_name = request.POST['folder_name']
    # folder_description = request.POST['folder_description']

    if ( (folder.folder_name != folder_name) and len(Folder.objects.filter(folder_name=folder_name)) ):
        # The way to return back the error message needs to be changed later
        errors.append("The folder name already exists, please type in another folder name.")
        print("The folder name already exists, please type in another folder name.")
        return HttpResponseRedirect(reverse('fileManage'))


    folder.folder_name = folder_name
    # folder.folder_description = folder_description
    folder.save()
    print("Already update folder's information")

    new_activity_instance = Activity(user=request.user)
    new_activity_instance.description = "<a href='http://127.0.0.1:8000/all_profile/" \
                                        + str(request.user.id) \
                                        + "'>" \
                                        + request.user.username\
                                        + "</a>" \
                                        + " change folder name from"\
                                        + "<i>" \
                                        + old_folder_name \
                                        + "</i>"\
                                        + " to "\
                                        + "<a href='http://127.0.0.1:8000/fileManage_tasks/" \
                                        + str(folder.id) \
                                        + "'>" \
                                        + folder.folder_name \
                                        + "</a>."
    new_activity_instance.save()


    return HttpResponseRedirect(reverse('fileManage'))



@login_required
def delete_folder(request, folder_id):
    print("in the delete_folder function.")
    context = {}
    context['user'] = request.user

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    folder = Folder.objects.get(id=folder_id)
    context['folder'] = folder

    folder_name = folder.folder_name

    tasks_inside_folder = Task.objects.filter(task_folder=folder)

    for task in tasks_inside_folder:
        task.delete()
        print("Successfully delete one task inside folder.")

    folder.delete()
    print("Successfully delete the folder.")

    new_activity_instance = Activity(user=request.user)
    new_activity_instance.description = "<a href='http://127.0.0.1:8000/all_profile/" \
                                        + str(request.user.id) \
                                        + "'>" \
                                        + request.user.username\
                                        + "</a>" \
                                        + " delete folder "\
                                        + "<i>"\
                                        + folder_name\
                                        + "</i>."
    new_activity_instance.save()


    return HttpResponseRedirect(reverse('fileManage'))


@login_required
def important_tasks(request):
    print("in the important_tasks function.")
    context = {}
    context['user'] = request.user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self


    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    context['important_label'] = True

    task_label_important = LABEL_CHOICES[1][1];
    context['label'] = task_label_important

    task_label_important_index = LABEL_CHOICES[1][0]

    tasks = Task.objects.filter(user=request.user, task_label=task_label_important_index).order_by("id").reverse()
    paginator = Paginator(tasks, 8)
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    context['tasks'] = tasks

    if len(tasks) == 0:
        context['empty'] = True

    context['LABEL_CHOICES'] = LABEL_CHOICES
    context['ALGORITHM_CHOICES'] = ALGORITHM_CHOICES
    context['STATUS_CHOICES'] = STATUS_CHOICES

    return render(request, 'WebApp/label_task.html', context)


@login_required
def warning_tasks(request):
    print("in the warning_tasks function.")
    context = {}
    context['user'] = request.user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    context['warning_label'] = True

    task_label_warning = LABEL_CHOICES[2][1]
    context['label'] = task_label_warning

    task_label_warning_index = LABEL_CHOICES[2][0]

    tasks = Task.objects.filter(user=request.user, task_label=task_label_warning_index).order_by("id").reverse()
    paginator = Paginator(tasks, 8)
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    context['tasks'] = tasks

    context['LABEL_CHOICES'] = LABEL_CHOICES
    context['ALGORITHM_CHOICES'] = ALGORITHM_CHOICES
    context['STATUS_CHOICES'] = STATUS_CHOICES

    return render(request, 'WebApp/label_task.html', context)



@login_required
def information_tasks(request):
    print("in the information_tasks function.")
    context = {}
    context['user'] = request.user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self


    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    context['information_label'] = True

    task_label_information = LABEL_CHOICES[3][1]
    context['label'] = task_label_information

    task_label_information_index = LABEL_CHOICES[3][0]

    tasks = Task.objects.filter(user=request.user, task_label=task_label_information_index).order_by("id").reverse()
    paginator = Paginator(tasks, 8)
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    context['tasks'] = tasks

    context['LABEL_CHOICES'] = LABEL_CHOICES
    context['ALGORITHM_CHOICES'] = ALGORITHM_CHOICES
    context['STATUS_CHOICES'] = STATUS_CHOICES

    return render(request, 'WebApp/label_task.html', context)




@login_required
def followers(request):
    print("in the followers function.")
    context = {}
    context['user'] = request.user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self


    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    followers = Followship.objects.filter(follower=request.user)

    paginator = Paginator(followers, 5)
    page = request.GET.get('page')
    try:
        followers = paginator.page(page)
    except PageNotAnInteger:
        followers = paginator.page(1)
    except EmptyPage:
        followers = paginator.page(paginator.num_pages)

    context['followers'] = followers

    if len(followers) == 0:
        context['empty'] = True;


    return render(request, 'WebApp/profile_allFollowers.html', context)



@login_required
def followings(request):
    print("in the followings function.")
    context = {}
    context['user'] = request.user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self
    

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    followings = Followship.objects.filter(following=request.user)

    paginator = Paginator(followings, 5)
    page = request.GET.get('page')
    try:
        followings = paginator.page(page)
    except PageNotAnInteger:
        followings = paginator.page(1)
    except EmptyPage:
        followings = paginator.page(paginator.num_pages)


    context['followings'] = followings


    if len(followings) == 0:
        context['empty'] = True;

    return render(request, 'WebApp/profile_allFollowings.html', context)



from django.shortcuts import get_object_or_404

@login_required
def profile(request):
    print("in the profile function")
    context = {}
    user = request.user
    context['user'] = user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self
    

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    # check own profile
    context['self'] = True

    profile = Profile.objects.get(user=user)
    context['profile'] = profile

    # go to profile page, default recent tab is my_activities
    context['recent_tab'] = "my_activities"

    number_of_followers = len(Followship.objects.filter(follower=request.user))
    number_of_followings = len(Followship.objects.filter(following=request.user))

    context['number_of_followers'] = number_of_followers
    context['number_of_followings'] = number_of_followings


    my_activities = Activity.objects.filter(user=request.user).order_by("time_created").reverse()
    # reverse order my_activities by time_created
    context['my_activities'] = sorted(my_activities, key=lambda activity: activity.time_created, reverse=True)

    followings_activities = []
    followings = Followship.objects.filter(following=request.user)

    for temp_followings in followings:
        for temp_activity in Activity.objects.filter(user=temp_followings.follower).order_by("time_created").reverse():
            followings_activities.append(temp_activity)
    # reverse order followings_activities by time_created
    context['followings_activities'] = sorted(followings_activities, key=lambda activity: activity.time_created, reverse=True)
    print(followings_activities)

    print("%" * 30)

    followers_activities = []
    followers = Followship.objects.filter(follower=request.user)
    for temp_followers in followers:
        for temp_activity in Activity.objects.filter(user=temp_followers.following).order_by("time_created").reverse():
            followers_activities.append(temp_activity)
    # reverse order followers_activities by time_created
    context['followers_activities'] = sorted(followers_activities, key=lambda activity: activity.time_created, reverse=True)

    print(followers_activities)

    return render(request, 'WebApp/profile.html', context)


@login_required
def other_profile(request, user_id):
    print("in the other_profile function.")
    context = {}
    context['user'] = request.user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self
    

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    other_user = User.objects.get(id=user_id)

    if(request.user == other_user):
        print("Enter myself profile page.")

        # check own profile
        context['self'] = True

        profile = Profile.objects.get(user=request.user)
        context['profile'] = profile

        number_of_followers = len(Followship.objects.filter(follower=request.user))
        number_of_followings = len(Followship.objects.filter(following=request.user))

        context['number_of_followers'] = number_of_followers
        context['number_of_followings'] = number_of_followings

        return render(request, 'WebApp/profile.html', context)

    else:
        print("Enter others' profile page.")
        context['other_user'] = other_user

        # check own profile
        context['self'] = False

        other_profile = Profile.objects.get(user=other_user)
        context['other_profile'] = other_profile

        other_activities = Activity.objects.filter(user=other_user).order_by("time_created").reverse()
        context['other_activities'] = other_activities

        number_of_followers = len(Followship.objects.filter(follower=other_user))
        number_of_followings = len(Followship.objects.filter(following=other_user))

        context['number_of_followers'] = number_of_followers
        context['number_of_followings'] = number_of_followings


        if len(Followship.objects.filter(following=request.user,
                                         follower=other_user)):
            is_followed = True
            context['is_followed'] = is_followed
            print("is_followed equals to true.")
        else:
            is_followed = False
            context['is_followed'] = is_followed
            print("is_followed equals to false.")

        return render(request, 'WebApp/other_profile.html', context)


@login_required
def add_comment(request, activity_id):
    print("in the add_comment function.")
    context = {};

    user = request.user
    context['user'] = user

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    activity = Activity.objects.get(id=activity_id)

    comment_text = request.POST['comment_text']

    new_comment_instance = Comment(user=user,
                                   activity=activity,
                                   text=comment_text)
    new_comment_instance.save()
    print("Successfully save new_comment_instance.")


    # if the comment target activity has task, we add into activities
    if new_comment_instance.activity.task:
        new_activity_instance = Activity(user=request.user)
        new_activity_instance.description = "<a href='http://127.0.0.1:8000/all_profile/" \
                                            + str(request.user.id) \
                                            + "'>" \
                                            + request.user.username\
                                            + "</a>" \
                                            + " add a comment to " \
                                            + "<a href='http://127.0.0.1:8000/taskDetail/" \
                                            + str(new_comment_instance.activity.task.id) \
                                            + "'>" \
                                            + new_comment_instance.activity.task.task_name \
                                            + "</a>."
        new_activity_instance.save()



    return HttpResponseRedirect(reverse('global_page'))



from django.views.decorators.csrf import csrf_exempt

# called when backend Honeycomb team finish running task
@csrf_exempt
def task_finished(request):
    print("in the task_finished function.")


    # check POST content
    if 'error' in request.POST:
        error = str(request.POST['error'])
        print (type(error))

    else:
        return HttpResponseNotFound("task_id not found in POST request")

    # not succeed
    if error == '1':
        return HttpResponseNotFound("Has error in honeycomb")


    # check POST content
    if 'task_id' in request.POST:
        task_id = request.POST['task_id']
    else:
        return HttpResponseNotFound("task_id not found in POST request")

    # check POST content
    if 'result_address' in request.POST:
        result_address = request.POST['result_address']
    else:
        return HttpResponseNotFound("result_address not found in POST request")

    
    print("task_id: %s" %(task_id))



    try:
        task = Task.objects.get(id=task_id)
        user = task.user

        print(request.POST['task_id'])

        print(task)

        completed_status = STATUS_CHOICES[1][0]

        # this task has been completed before
        if task.task_status == completed_status:
            return HttpResponseNotFound("Task with id: %s has been completed before" %(task_id))

        # set task status to be completed
        task.task_status = completed_status

        print(task.task_status)

        # save the task result address
        task.output_file_address = result_address

        print(task.output_file_address)

        task.save()
        print("Task table modify success")
        print(task)

        # add completed task to Pending2CompletedTask table
        taskCompleted = Pending2CompletedTask(user=user,
                                                task=task)
        taskCompleted.save()
        print("Pending2CompletedTask table add success")
        print(taskCompleted)

        return HttpResponse("Successfully received by Honeycell")

    # task does not exist
    except ObjectDoesNotExist:
        return HttpResponse("Task_id not not exist in Honeycell")




def task_finished_ajax_check_database(request):
    context = {}
    messageString = ""

    if request.user:
      context['user'] = request.user
      curr_user = request.user

    try:
        completed_tasks = Pending2CompletedTask.objects.filter(user=curr_user)
        # print("completed_tasks: ")
        # print(completed_tasks)

        # no task completed for this user
        if not completed_tasks:
            return HttpResponse(messageString)

        # detect task complete flag
        for t in completed_tasks:
            # temp = '<h2> Your task <a href=" {% ' 
            # temp += "url " + "'taskDetail'"
            # temp += " %d " %(t.task.id)
            # temp += ' %}"' + '> %s </a> has been completed. <h2> \n' %(t.task.task_name)
            temp = '<h2> Your task "' 
            temp += '%s" has been completed. <h2> \n' %(t.task.task_name)
            messageString += temp

        print("messageString: \n %s") %(messageString)


        # delete completed task in Pending2CompletedTask
        for t in completed_tasks:
            t.delete()

        print("completed_tasks has been deleted")

        return HttpResponse(messageString)

    except ObjectDoesNotExist:
      context['errors'] = ["task_finished_popup fail"]

    return HttpResponse()







@login_required
def profile_comment(request, recent_tab):
    print("in the profile_comment function")
    context = {}
    user = request.user
    context['user'] = user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self
    

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    # check own profile
    context['self'] = True

    profile = Profile.objects.get(user=user)
    context['profile'] = profile

    # go to profile page, default recent tab is my_activities
    context['recent_tab'] = recent_tab

    number_of_followers = len(Followship.objects.filter(follower=request.user))
    number_of_followings = len(Followship.objects.filter(following=request.user))

    context['number_of_followers'] = number_of_followers
    context['number_of_followings'] = number_of_followings

    my_activities = Activity.objects.filter(user=request.user).order_by("time_created").reverse()
    # reverse order my_activities by time_created
    context['my_activities'] = sorted(my_activities, key=lambda activity: activity.time_created, reverse=True)

    followings_activities = []
    followings = Followship.objects.filter(following=request.user)

    for temp_followings in followings:
        for temp_activity in Activity.objects.filter(user=temp_followings.follower).order_by("time_created").reverse():
            followings_activities.append(temp_activity)
    # reverse order followings_activities by time_created
    context['followings_activities'] = sorted(followings_activities, key=lambda activity: activity.time_created, reverse=True)
    print(followings_activities)

    followers_activities = []
    followers = Followship.objects.filter(follower=request.user)
    for temp_followers in followers:
        for temp_activity in Activity.objects.filter(user=temp_followers.following).order_by("time_created").reverse():
            followers_activities.append(temp_activity)
    # reverse order followers_activities by time_created
    context['followers_activities'] = sorted(followers_activities, key=lambda activity: activity.time_created, reverse=True)


    print(context)


    return render(request, 'WebApp/profile.html', context)





@login_required
def profile_add_comment(request, activity_id):
    print("in the profile_add_comment function.")
    print(request)
    print(activity_id)
    print(request.POST['comment_text'])
    context = {}

    user = request.user
    context['user'] = user

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    print("%" * 30)
    context['recent_tab'] = request.POST['recent_tab']
    print(context['recent_tab'])

    context['current_tab'] = request.POST['current_tab']
    print(context['current_tab'])
    print("%" * 30)


    # update the recent_tab to be current_tab
    context['recent_tab'] = context['current_tab']

    activity = Activity.objects.get(id=activity_id)

    comment_text = request.POST['comment_text']

    new_comment_instance = Comment(user=user,
                                   activity=activity,
                                   text=comment_text)
    new_comment_instance.save()
    print("Successfully save new_comment_instance.")

    # if the comment target activity has task, we add into activities
    if new_comment_instance.activity.task:
        new_activity_instance = Activity(user=request.user)
        new_activity_instance.description = "<a href='http://127.0.0.1:8000/all_profile/" \
                                            + str(request.user.id) \
                                            + "'>" \
                                            + request.user.username\
                                            + "</a>" \
                                            + " add a comment to " \
                                            + "<a href='http://127.0.0.1:8000/taskDetail/" \
                                            + str(new_comment_instance.activity.task.id) \
                                            + "'>" \
                                            + new_comment_instance.activity.task.task_name \
                                            + "</a>."
        new_activity_instance.save()


    return HttpResponseRedirect(reverse('profile_comment', kwargs={'recent_tab': context['recent_tab']}))






@login_required
def other_profile_comment(request, user_id):
    print("in the other_profile_comment function.")

    context = {}
    context['user'] = request.user

    # user Control Sidebar in base.html
    num_followers_self = len(Followship.objects.filter(follower=request.user))
    num_followings_self = len(Followship.objects.filter(following=request.user))
    context['num_followers_self'] = num_followers_self
    context['num_followings_self'] = num_followings_self
    

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    other_user = User.objects.get(id=user_id)

    print("Enter others' profile page.")
    context['other_user'] = other_user

    # check own profile
    context['self'] = False

    other_profile = Profile.objects.get(user=other_user)
    context['other_profile'] = other_profile

    other_activities = Activity.objects.filter(user=other_user).order_by("time_created").reverse()
    context['other_activities'] = other_activities

    number_of_followers = len(Followship.objects.filter(follower=other_user))
    number_of_followings = len(Followship.objects.filter(following=other_user))

    context['number_of_followers'] = number_of_followers
    context['number_of_followings'] = number_of_followings


    if len(Followship.objects.filter(following=request.user,
                                     follower=other_user)):
        is_followed = True
        context['is_followed'] = is_followed
        print("is_followed equals to true.")
    else:
        is_followed = False
        context['is_followed'] = is_followed
        print("is_followed equals to false.")

    return render(request, 'WebApp/other_profile.html', context)



@login_required
def other_profile_add_comment(request, activity_id):
    print("in the other_profile_add_comment function.")
    context = {}

    user = request.user
    context['user'] = user

    activity = Activity.objects.get(id=activity_id)
    comment_text = request.POST['comment_text']
    other_user_id = request.POST['other_user_id']

    new_comment_instance = Comment(user=user,
                                   activity=activity,
                                   text=comment_text)
    new_comment_instance.save()
    print("Successfully save new_comment_instance.")

    if new_comment_instance.activity.task:
        new_activity_instance = Activity(user=request.user)
        new_activity_instance.description = "<a href='http://127.0.0.1:8000/all_profile/" \
                                            + str(request.user.id) \
                                            + "'>" \
                                            + request.user.username\
                                            + "</a>" \
                                            + " add a comment to " \
                                            + "<a href='http://127.0.0.1:8000/taskDetail/" \
                                            + str(new_comment_instance.activity.task.id) \
                                            + "'>" \
                                            + new_comment_instance.activity.task.task_name \
                                            + "</a>."
        new_activity_instance.save()


    return HttpResponseRedirect(reverse('other_profile_comment', kwargs={'user_id': other_user_id}))





@login_required
def all_profile(request, user_id):
    print("in the all_profile function.")

    context = {}

    print("%" * 50)
    print(request.user.id)
    print(user_id)
    print("%" * 50)

    user = User.objects.get(id=user_id)

    if request.user.username == user.username:
        print("equal")
        return profile(request)
    else:
        print("not equal")
        return other_profile(request, user_id)






















