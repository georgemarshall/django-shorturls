from django.contrib import admin

from .models import URL


class URLAdmin(admin.ModelAdmin):
    list_filter = ('site',)
    search_fields = ('url',)
    radio_fields = {'site': admin.VERTICAL}

admin.site.register(URL, URLAdmin)