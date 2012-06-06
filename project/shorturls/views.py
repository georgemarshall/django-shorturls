import base64
import struct

from django import http
from django.contrib.contenttypes.views import shortcut
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_str
from django.utils.log import getLogger
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

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
            data = base64.urlsafe_b64decode(smart_str(kwargs['token']) + '==')

            # Get the sizes of our values
            offset = 0
            format = '!B'

            (sizes,) = struct.unpack_from(format, data, offset)

            type_len = sizes >> 4
            obj_len = sizes - (type_len << 4)

             # Get the content type and object id
            offset += struct.calcsize(format)
            format = '!%ds%ds' % (type_len, obj_len)

            type_id, obj_id = struct.unpack_from(format, data, offset)

            # Add pad bytes and unpack ``unsigned long long`` values
            format = '!QQ'

            type_id, obj_id = struct.unpack(format, '%s%s' % (
                type_id.rjust(8, '\0'), obj_id.rjust(8, '\0')
            ))

            return type_id, obj_id


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
