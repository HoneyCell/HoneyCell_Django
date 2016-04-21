__author__ = 'jianheluo'

from django.conf.urls import include, url
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # empty url
    url(r'^$', 'WebApp.views.index', name='index'),

    # index page
    url(r'^index/$', 'WebApp.views.index', name='index'),

    # new argument 'template_name'
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'WebApp/login.html'}, name='login'),

    # url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'WebApp.views.my_logout', name='logout'),

    # registration is normal route
    url(r'^registration/$', 'WebApp.views.registration', name='registration'),

    # new task page
    url(r'^newTask/$', 'WebApp.views.newTask', name='newTask'),

    #create new task instance
    url(r'^create_new_task/$', 'WebApp.views.create_new_task', name='create_new_task'),

    # history tasks page
    url(r'^historyTask/$', 'WebApp.views.historyTask', name='historyTask'),

    # folder Management page
    url(r'^fileManage/$', 'WebApp.views.fileManage', name='fileManage'),

    # go to specific folder
    url(r'^fileManage_tasks/(?P<folder_id>\d+)$', 'WebApp.views.fileManage_tasks', name='fileManage_tasks'),



    # profile tasks page
    url(r'^profile/$', 'WebApp.views.profile', name='profile'),

    url(r'^profile_comment/(?P<recent_tab>.*)$', 'WebApp.views.profile_comment', name='profile_comment'),

    url(r'^profile_allFollowers/$', 'WebApp.views.profile_allFollowers', name='profile_allFollowers'),
    url(r'^profile_allFollowings/$', 'WebApp.views.profile_allFollowings', name='profile_allFollowings'),


    # settings page
    url(r'^settings/$', 'WebApp.views.settings', name='settings'),

    # follow other users
    url(r'^add_followship/(?P<user_id>\d+)$', 'WebApp.views.follow', name='follow'),

    # unfollow other users
    url(r'^delete_followship/(?P<user_id>\d+)$', 'WebApp.views.unfollow', name='unfollow'),

    # new user guide page
    url(r'^guide/$', 'WebApp.views.guide', name='guide'),

    # global_page
    url(r'^global_page/$', 'WebApp.views.global_page', name='global_page'),

    # to get user's picture
    url(r'^get_user_picture/(?P<user_id>\d+)$', 'WebApp.views.get_user_picture', name='get_user_picture'),

    # to update user's profile
    url(r'^update_profile/$', 'WebApp.views.update_profile', name='update_profile'),

    # to change user's password
    url(r'^change_password/$', 'WebApp.views.change_password', name='change_password'),

    # task detail page
    url(r'^taskDetail/(?P<task_id>\d+)$', 'WebApp.views.taskDetail', name='taskDetail'),

    # to update the task's name and description
    url(r'^update_task/(?P<task_id>\d+)$', 'WebApp.views.update_task', name='update_task'),

    # to create a new folder
    url(r'^new_folder/$', 'WebApp.views.new_folder', name='new_folder'),

    # to update folder's name and description
    url(r'^update_folder/(?P<folder_id>\d+)$', 'WebApp.views.update_folder', name='update_folder'),

    # to delete the folder
    url(r'^delete_folder/(?P<folder_id>\d+)$', 'WebApp.views.delete_folder', name='delete_folder'),

    url(r'^important_tasks/$', 'WebApp.views.important_tasks', name='important_tasks'),

    url(r'^warning_tasks/$', 'WebApp.views.warning_tasks', name='warning_tasks'),

    url(r'^information_tasks/$', 'WebApp.views.information_tasks', name='information_tasks'),

    url(r'^followers/$', 'WebApp.views.followers', name='followers'),

    url(r'^followings/$', 'WebApp.views.followings', name='followings'),

    url(r'^other_profile/(?P<user_id>\d+)$', 'WebApp.views.other_profile', name='other_profile'),

    url(r'^other_profile_comment/(?P<user_id>\d+)$', 'WebApp.views.other_profile_comment', name='other_profile_comment'),


    url(r'^add_comment/(?P<activity_id>\d+)$', 'WebApp.views.add_comment', name='add_comment'),

    url(r'^task_finished/$', 'WebApp.views.task_finished', name='task_finished'),

    # url(r'^alert/$', 'WebApp.views.alert', name='alert'),








    # task running in honeycomb(backend) finished
    # url(r'^task_finished/(?P<task_id>\d+)$', 'WebApp.views.task_finished', name='task_finished'),
    url(r'^task_finished/$', 'WebApp.views.task_finished', name='task_finished'),
    url(r'^task_finished_ajax_check_database/$', 'WebApp.views.task_finished_ajax_check_database', name='task_finished_ajax_check_database'),



    url(r'^profile_add_comment/(?P<activity_id>\d+)$', 'WebApp.views.profile_add_comment', name='profile_add_comment'),

    url(r'^other_profile_add_comment/(?P<activity_id>\d+)$', 'WebApp.views.other_profile_add_comment', name='other_profile_add_comment'),



    # function to laod the html template
    # url(r'^graph/$', 'WebApp.views.graph', name='graph'),

    # function to load json file
    url(r'^get_json_result/(?P<task_id>\d+)$', 'WebApp.views.get_json_result', name='get_json_result'),


    url(r'all_profile/(?P<user_id>\d+)$', 'WebApp.views.all_profile', name='all_profile'),



    url(r'^add_comment_taskDetail/(?P<activity_id>\d+)$', 'WebApp.views.add_comment_taskDetail', name='add_comment_taskDetail'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)