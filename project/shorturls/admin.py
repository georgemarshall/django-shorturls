from django.contrib import admin

from .models import Hit, URL


class HitAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_pk', 'ip_address', 'date')
    list_filter = ('date', 'site',)
    ordering = ('-date',)
    raw_id_fields = ('user',)
    search_fields = ('user__username', 'ip_address')
    radio_fields = {'site': admin.VERTICAL}


class URLAdmin(admin.ModelAdmin):
    list_filter = ('site',)
    search_fields = ('url',)
    radio_fields = {'site': admin.VERTICAL}


admin.site.register(Hit, HitAdmin)
admin.site.register(URL, URLAdmin)
