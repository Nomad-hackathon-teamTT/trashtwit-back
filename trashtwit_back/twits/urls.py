from django.conf.urls import url

from . import views

app_name = "twits"

urlpatterns = [
    url(
        regex=r'^$',
        view=views.Feed.as_view(),
        name='feed'
    ),
    url(
        regex=r'^post',
        view=views.Twit.as_view(),
        name='twit'
    ),
    # url(
    #     regex=r'^(?P<twit_id>[0-9]+)$',
    #     view=views.Twit.as_view(),
    #     name='Feed',
    # ),
    url(
        regex=r'^(?P<twit_id>\w+)/$',
        view=views.TwitDetail.as_view(),
        name='twit_detail'
    ),
]

