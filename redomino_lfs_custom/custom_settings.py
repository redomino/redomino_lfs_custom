from django.conf import settings
from django.utils.translation import ugettext as _

settings.POSTAL_ADDRESS_STATE = getattr(settings, 'POSTAL_ADDRESS_STATE', (_("Province"), True))
settings.SHOW_VAT = getattr(settings, 'SHOW_VAT', False)
