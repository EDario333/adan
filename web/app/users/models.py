from django.db import models

from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ObjectDoesNotExist

from django.utils.translation import pgettext
from django.utils.translation import gettext as _

from catalogues.models import MyModel

from utils import utils

import os

class Users(AbstractUser, MyModel):
	def uploads_dir(instance, filename):
		# We must to create its upload dir...
		path = os.getcwd() + '/static/admin/uploads/users/'
		try:
			os.makedirs(path)
		except OSError:  
			print("Creation of the directory %s failed" % path)
		else:  
			print ("Successfully created the directory %s " % path)
		return path + str(instance.id) + '-filename-' + filename

	mothers_last_name = models.CharField(max_length=254, default=None, blank=True, null=True, verbose_name=pgettext('users model', 'Mothers last name'))
	middle_name = models.CharField(max_length=254, default=None, blank=True, null=True, verbose_name=pgettext('users model', 'Middle name'))

	phishing = models.BooleanField(default=False, editable = False, blank=False, null=False)
	phishing_at = models.TimeField(editable = False, default=None, blank=True, null=True)
	phishing_when = models.DateField(editable = False, default=None, blank=True, null=True)

	email_confirmed = models.BooleanField(default=False, editable=False)
	email_confirmed_at = models.TimeField(editable = False, default=None, blank=True, null=True)
	email_confirmed_when = models.DateField(editable = False, default=None, blank=True, null=True)

	email_approved = models.BooleanField(default=False, editable=False)
	email_approved_at = models.TimeField(editable = False, default=None, blank=True, null=True)
	email_approved_when = models.DateField(editable = False, default=None, blank=True, null=True)

	'''
	has_paid = models.BooleanField(default=False)
	paid_at = models.TimeField(editable = False, default=None, blank=True, null=True)
	paid_when = models.DateField(editable = False, default=None, blank=True, null=True)

	payment_detail_bank_key = models.CharField(max_length=254, default=None, blank=True, null=True)
	payment_details = models.CharField(max_length=254, default=None, blank=True, null=True)
	payment_comments = models.CharField(max_length=1024, default=None, blank=True, null=True)

	paid_service_expires_at = models.TimeField(editable = False, default=None, blank=True, null=True)
	paid_service_expires_when = models.DateField(editable = False, default=None, blank=True, null=True)
	'''

	first_time_login = models.BooleanField(default=False)
	show_dlg_first_tutorial_not_completed = models.BooleanField(default=True)
	first_tutorial_completed = models.BooleanField(default=False)
	current_step_first_tutorial = models.PositiveSmallIntegerField(default=0)
	created_with_fb = models.BooleanField(default=False, editable=False)
	fb_id = models.CharField(max_length=1024, default=None, blank=True, null=True, editable=False)
	created_with_google = models.BooleanField(default=False, editable=False)
	google_id = models.CharField(max_length=1024, default=None, blank=True, null=True, editable=False)

	profile_picture = models.ImageField(default=None, blank=True, null=True, verbose_name=pgettext('users model', 'Profile picture'),upload_to=uploads_dir, max_length=500)

	gender = models.CharField(max_length=1, choices=utils.GENDERS, default=None, blank=True, null=True, verbose_name=pgettext('users model', 'Gender'))
	dob = models.DateField(default=None, blank=True, verbose_name=pgettext('users model', 'Date of birth'), null=True)
	fb = models.CharField(max_length=255, default=None, blank=True, null=True, unique=True, verbose_name=pgettext('users model', 'FB account'))
	twitter = models.CharField(max_length=255, default=None, blank=True, null=True, unique=True, verbose_name=pgettext('users model', 'Twitter account'))
	instagram = models.CharField(max_length=255, default=None, blank=True, null=True, unique=True, verbose_name=pgettext('users model', 'Instagram account'))

	has_rated = models.BooleanField(default=False, editable=False)

	permissions = None
	plain_password = None

	def __check_field_value__(self, value):
		if value and value is not None and len(value.strip()) > 0:
			return value + ' '
		return ''

	def get_full_name(self):
		result = self.__check_field_value__(self.first_name)
		result += self.__check_field_value__(self.middle_name)
		result += self.__check_field_value__(self.last_name)
		result += self.__check_field_value__(self.mothers_last_name)

		return result

	@property
	def full_name(self):
		return self.get_full_name()

	def get_expires_free_version(self):
		from datetime import timedelta
		return self.email_approved_when + timedelta(days=15)

	@property
	def static_profile_picture(self):
		result = '/static/imgs/user.png'

		if self.profile_picture.name and self.profile_picture.name is not None and len(self.profile_picture.name) > 0:
			result = self.profile_picture.name[self.profile_picture.name.index('/static'):]

		return result

	def has_rated(self):
		has_rated=True
		if self.is_authenticated:
			try:
				has_rated=Ratings.objects.filter(user=self).first() is not None
			except ObjectDoesNotExist:
				pass

		return has_rated

	class Meta:
		verbose_name = pgettext('users model', 'User')
		verbose_name_plural = pgettext('users model', 'Users')

class Ratings(models.Model):
	user = models.OneToOneField(Users, on_delete=models.PROTECT, default=None, db_column='user_id', verbose_name=_('User'))
	stars = models.PositiveSmallIntegerField(default=None, blank=True, null=True)
	comments = models.CharField(max_length=1024, default=None, blank=True, null=True, verbose_name=_('Comments'))
	email_sent = models.BooleanField(default=False, editable = False, blank=False, null=False)