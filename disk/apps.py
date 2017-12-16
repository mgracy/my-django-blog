from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DiskConfig(AppConfig):
    name = 'disk'
    verbose_name= _('disk')

    def ready(self):
    	import disk.signals
