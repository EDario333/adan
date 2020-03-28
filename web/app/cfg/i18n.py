from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import os

LANGUAGES = [
	('en', _('English')),
	('es', _('Spanish')),
]

LOCALE_PATHS = [
	os.path.join(settings.BASE_DIR, 'i18n'), 
]