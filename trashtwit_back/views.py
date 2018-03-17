from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os

class ReactAppView(View):
    def get(self, request, format=None):

        try:
            with open(os.path.join(str(settings.ROOT_DIR), 'frontend', 'build', 'index.html')) as f:
                return HttpResponse(f.read())
        except:
            return HttpResponse(
                """
                index.html was not found. Run 'yarn build' in the React App directory.
                {}
                """.format(os.path.join(str(settings.ROOT_DIR), 'frontend', 'build', 'index.html')),
                status=501,
            )
