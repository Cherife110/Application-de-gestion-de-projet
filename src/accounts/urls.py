from django.conf import settings
from django.urls import  path
from .views import ProjectDeleteView, ProjectUpdateView, UserDeleteView, UserUpdateView, add_project, add_subject, home_student, logout_view, register, Customlogin, home_admin, home_teacher
from django.conf.urls.static import static

urlpatterns = [
    #path("", index,name="home"),
    
    path("", Customlogin, name="login_page"),
    path('logout/', logout_view, name='logout'), # associez l'URL à la vue
    path("home_admin", home_admin, name="home_admin"),
    path("home_teacher", home_teacher , name="home_teacher"),
    path("home_student", home_student, name="home_student"),
    path("home_teacher/add_project", add_project, name="add_project"),
    path("home_admin/add_subject", add_subject, name="add_subject"),
     path("home_admin/register", register, name="register_page"),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'), # met à jour un projet existant
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'), # supprime un projet existant
    path('<int:pk>/user_update/', UserUpdateView.as_view(), name='user_update'), # met à jour un projet existant
    path('<int:pk>/user_delete/', UserDeleteView.as_view(), name='user_delete') # supprime un projet existant

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
