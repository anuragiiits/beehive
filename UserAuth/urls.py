from django.urls import include, path
from .views import AddUser, ChangePermission

app_name = 'UserAuth'

urlpatterns = [
    path('adduser/', AddUser.as_view(), name="userauth"),
    path(
        'changepermission/',
        ChangePermission.as_view(),
        name="change_user_permission")
]
