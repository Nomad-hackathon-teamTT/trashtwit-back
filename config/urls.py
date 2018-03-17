from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from trashtwit_back import views


# app_name = "trashtwits_back"

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # url(r'^api/v1/', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    # url(r'^api/v1/about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    # User management
    url(r'^api/v1/twits/', include('trashtwit_back.twits.urls', namespace='twits')),

    url(r'^api/v1/users/', include('trashtwit_back.users.urls', namespace='users')),
    url(r'^api/v1/accounts/', include('allauth.urls')),
    url(r'^api/v1/rest-auth/', include('rest_auth.urls')),
    url(r'^api/v1/rest-auth/registration((\/\w+)+|\/?)$', include('rest_auth.registration.urls')),

    url(r'^', view=views.ReactAppView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
