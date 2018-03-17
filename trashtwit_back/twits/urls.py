from django.conf.urls import url

from . import views

app_name = "twits"

urlpatterns = [
    url(
        regex=r'^$',
        view=views.Feed.as_view(),
        name='list'
    ),
    url(
        regex=r'^$',
        view=views.TwitDetail.as_view(),
        name='list'
    ),
]

