import os
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


def get_spa_html():
    with open(
        os.path.join(os.path.dirname(__file__),
                     '../frontend/dist/index.html', 'rb')
    ) as index:
        retval = index.read()
    return retval


SPA_HTML = get_spa_html()


@login_required
@require_http_methods(['GET'])
def main(request):
    if settings.DEBUG:
        return HttpResponse(get_spa_html())
    else:
        return HttpResponse(SPA_HTML)
