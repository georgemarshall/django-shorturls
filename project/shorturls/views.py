import base64
import struct

from django import http
from django.contrib.contenttypes.views import shortcut
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_str
from django.utils.log import getLogger
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

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
            return shortcut(request, *obj_ids)
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
