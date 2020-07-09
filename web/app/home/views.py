# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
#from django.contrib import messages

#from django.utils.translation import gettext as _
#from django.utils.translation import pgettext

#from utils.utils import get_main_url

def index(request):
	lang=request.META['HTTP_ACCEPT_LANGUAGE'].split(',')[1]
	request.session['LANGUAGE_COOKIE_NAME'] = lang[:2]
	return render(request, 'site/index.html')