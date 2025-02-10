from config import settings
from .users import UserAdmin

from django.contrib.admin import site
from django.contrib.auth.models import Group as DjangoGroup

site.unregister(DjangoGroup)

site.site_title = settings.SITE_TITLE
site.index_title = settings.INDEX_TITLE
site.site_header = settings.SITE_HEADER
site.site_url = settings.SITE_URL
