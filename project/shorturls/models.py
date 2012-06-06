from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from picklefield.fields import PickledObjectField


class Hit(models.Model):
    # Content-object field
    content_type = models.ForeignKey(ContentType,
        verbose_name=_('content type'),
        related_name='content_type_set_for_%(class)s'
    )
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field='content_type', fk_field='object_pk')

    # Metadata about the comment
    site = models.ForeignKey(Site)

    headers = PickledObjectField(_('headers'), blank=True, null=True)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)
    date = models.DateTimeField(_('date'), auto_now_add=True)

    class Meta:
        verbose_name = _('hit')
        verbose_name_plural = _('hits')

    def __unicode__(self):
        return '%d' % self.id


class URL(models.Model):
    site = models.ForeignKey(Site)
    url = models.URLField(_('url'), max_length=200, blank=True,
        help_text=_("This can be either an absolute path or a full URL starting with 'http://'."))

    class Meta:
        verbose_name = _('url')
        verbose_name_plural = _('urls')
        unique_together = (('site', 'url'),)

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return self.url
