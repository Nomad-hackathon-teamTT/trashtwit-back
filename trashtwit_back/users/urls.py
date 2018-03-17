from django.conf.urls import url

from . import views

app_name = "users"

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ProfilePage.as_view(),
        name='list'
    ),
    url(
        regex=r'^(?P<username>\w+)/$',
        view=views.ProfilePage.as_view(),
        name='users'
    )
]

