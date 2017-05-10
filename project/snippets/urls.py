from django.conf.urls import url, include
from snippets import views
from django.views.generic import TemplateView

app_name= 'snippets'

urlpatterns = [
    #-------------USING GENERIC VIEWS----------------------#
    # url(r'^readProjects/$', views.ProjectlistAPIView.as_view() ) ,
    # url(r'^createProjects/$', views.ProjectlistCreateAPIView.as_view()),
    # url(r'^FetchClients/$', views.ClientlistAPIView.as_view()),
    # url(r'^CreateClients/$', views.ClientlistCreateAPIView.as_view()),
    # url(r'^FetchAdmin/$', views.AdminlistAPIView.as_view()),
    # url(r'^CreateAdmin/$', views.AdminlistCreateAPIView.as_view()),

    #----------------USING CUSTOM VIEWS------------------- #
    url(r'^userslist$', views.UserList.as_view()),
    url(r'^projectlist$', views.ProjectList.as_view()),
    url(r'^projectinstance$', views.ProjectInstance.as_view()),
    url(r'^userinstance$', views.UserInstance.as_view()),
    url('^userlogin$', views.LoginAPIView.as_view(),),
    url('^userlogout$', views.Logout.as_view()),
    url('^projectstatus$', views.SetProjectStatus.as_view()),
    url(r'^hello/',views.hello,name='hello'),
    url(r'^login/',views.login,name='login'),
    url(r'^admin/',views.admin,name="admin-page"),
    url(r'^client/',views.Client,name='client'),
    url(r'^employee/',views.employee,name='employee'),
    url(r'^createProject/', views.CreateProject.as_view(), name='createProject'),
    url(r'^createUser$', views.CreateUser.as_view(), name='createUser'),
    url(r'^deleteuser/', views.DeleteUser.as_view(), name='deleteuser'),
    url(r'^userLogList$', views.UserLogList.as_view()),
    url(r'^GetCount$', views.GetCount.as_view()),
]