"""
======
Models
======
Provides base models for other django.model subclass
"""
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from django.conf import settings
from django.contrib.gis.db.models import Manager, Model


class ExManager(Manager):
    """
    Removing archived items from querysets
    """
    def get_queryset(self):
        return super(ExManager, self).get_queryset().exclude(status='archived')


class ExModel(Model):
    """
    Adds default permissions and some common methods
    .. note:: Always use this class instead of django.db.models.Model
    """
    created_at = AutoCreatedField(_('Updated at'))
    updated_at = AutoLastModifiedField(_('Updated at'))
    status = models.CharField(default='active', choices=settings.AVAILABLE_CHOICES, max_length=10)

    objects = ExManager()

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')
        abstract = True

    def delete(self, force=False, **kwargs):
        if force is True:
            return super(ExModel, self).delete(**kwargs)
        self.status = 'archived'
        self.save()


class AbstractExModel(Model):
    """
    Adds default permissions and some common methods
    .. note:: Always use this class instead of django.db.models.Model
    """
    created_at = AutoCreatedField(_('Updated at'))
    updated_at = AutoLastModifiedField(_('Updated at'))

    objects = ExManager()

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')
        abstract = True
