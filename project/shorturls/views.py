from django import http
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.views import shortcut
from django.contrib.sites.models import Site
from django.utils.decorators import method_decorator
from django.utils.log import getLogger
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .models import Hit
from .utils import token_decode

logger = getLogger('django.request')


class ShortURLView(View):
    """
    A view that provides a redirect on any GET request.
    """
    url = None

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ShortURLView, self).dispatch(*args, **kwargs)

    def get_obj_ids(self, **kwargs):
        if 'token' in kwargs:
            return token_decode(kwargs['token'])

    def get(self, request, *args, **kwargs):
        obj_ids = self.get_obj_ids(**kwargs)
        if obj_ids:
            ret = shortcut(request, *obj_ids)

            # Track the hit
            hit = Hit(
                content_type=ContentType.objects.get_for_id(obj_ids[0]),
                object_pk=obj_ids[1],
                site=Site.objects.get_current(),
                headers=None,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            if request.user.is_authenticated():
                hit.user = request.user
            hit.save()

            return ret
        else:
            raise http.Http404('The requested short url does not exist.')

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
