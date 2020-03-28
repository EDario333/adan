# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

#from cities_light.abstract_models import AbstractCity, AbstractRegion, AbstractCountry
#from cities_light.receivers import connect_default_signals

from django.utils.translation import pgettext
from django.utils.translation import gettext as _

from datetime import datetime,date

from utils import utils

'''
class Country(AbstractCountry):
  class Meta:
    verbose_name = pgettext('country model', 'Country')
    verbose_name_plural = pgettext('country model', 'Countries')

connect_default_signals(Country)

class Region(AbstractRegion):
  pass

connect_default_signals(Region)

class City(AbstractCity):
  timezone = models.CharField(max_length=40)

connect_default_signals(City)
'''

class MyModel(models.Model):
	def __init__(self, *args, **kwargs):
		super(MyModel, self).__init__(*args, **kwargs)

	#created_by_user = models.ForeignKey('users.Users', editable = False, on_delete=models.PROTECT, default=1, blank=False, null=False, db_column='created_by_user', verbose_name=_('Created by'), related_name='%(class)s_created_by')
	created_by_user = models.ForeignKey('users.Users', on_delete=models.PROTECT, default=1, blank=False, null=False, db_column='created_by_user', verbose_name=_('Created by'), related_name='%(class)s_created_by')
	created_at = models.TimeField(editable=False,default=datetime.now(), blank=False, null=False)
	created_when = models.DateField(editable=False,default=datetime.now(), blank=False, null=False)

	disabled = models.BooleanField(editable=False,default=False)
	disabled_at = models.TimeField(editable = False, default=None, blank=True, null=True)
	disabled_when = models.DateField(editable = False, default=None, blank=True, null=True)
	disabled_reason = models.CharField(editable=False,max_length=1024, default=None, blank=True, null=True, verbose_name=_('Specify the reason to disable this product'))

	dropped = models.BooleanField(editable=False,default=False)
	dropped_at = models.TimeField(editable = False, default=None, blank=True, null=True)
	dropped_when = models.DateField(editable = False, default=None, blank=True, null=True)
	dropped_reason = models.CharField(editable=False,max_length=1024, default=None, blank=True, null=True, verbose_name=_('Specify the reason to drop this object'))

	def undrop(self):
		self.dropped = False
		self.dropped_at = None
		self.dropped_when = None
		self.dropped_reason = None
		self.save()

	def drop(self, reason=None):
		full_time = datetime.now()
		self.dropped = True
		self.dropped_at = full_time
		self.dropped_when = full_time
		self.dropped_reason = reason
		self.save()

	@property
	def created_when_fmt_mx(self):
		year = self.created_when.year
		month = str(self.created_when.month)
		day = str(self.created_when.day)
		if len(day)<2:
			day='0'+day
		if len(month)<2:
			month='0'+month
		result = str(day) + '/' + str(month) + '/' + str(year)
		return result

	class Meta:
		#proxy = True
		abstract = True

class MyModelWithDescriptionNotesComments(MyModel):
	description = models.TextField(max_length=1024, default=None, blank=True, null=True, verbose_name=_('Description'))
	notes = models.TextField(max_length=1024, default=None, blank=True, null=True, verbose_name=_('Notes'))
	comments = models.TextField(max_length=1024, default=None, blank=True, null=True, verbose_name=_('Comments'))

	class Meta:
		abstract = True

class MyModelWithDescription(MyModel):
	description = models.TextField(max_length=1024, default=None, blank=True, null=True, verbose_name=_('Description'))

	class Meta:
		abstract = True

class MyModelWithNotes(MyModel):
	#notes = models.CharField(max_length=1024, default=None, blank=True, null=True, verbose_name=_('Notes'))
	notes = models.TextField(max_length=1024, default=None, blank=True, null=True, verbose_name=_('Notes'))

	class Meta:
		abstract = True
	
class MyModelWithComments(MyModel):
	comments = models.TextField(max_length=1024, default=None, blank=True, null=True, verbose_name=_('Comments'))

	class Meta:
		abstract = True

class Person(MyModel):
	last_name = models.CharField(max_length=254, default=None, blank=False, null=False, verbose_name=pgettext('person model', 'Last name')+'*')
	mothers_last_name = models.CharField(max_length=254, default=None, blank=True, null=True, verbose_name=pgettext('person model', 'Mothers last name'))
	first_name = models.CharField(max_length=254, default=None, blank=False, null=False, verbose_name=pgettext('person model', 'First name')+'*')
	middle_name = models.CharField(max_length=254, default=None, blank=True, null=True, verbose_name=pgettext('person model', 'Middle name'))

	gender = models.CharField(max_length=1, choices=utils.GENDERS, default=None, blank=False, null=False, verbose_name=pgettext('person model', 'Gender'))
	dob = models.DateField(default=None, blank=False, null=False, verbose_name=pgettext('person model', 'Date of birth')+'*')

	email = models.CharField(max_length=254, default=None, blank=True, null=True, verbose_name=_('Email'), unique=True)

	#city = models.ForeignKey(City, on_delete=models.PROTECT, default=None, blank=True, null=True, db_column='city_id', verbose_name=_('City'))
	address_line1 = models.CharField(max_length=1024, default=None, blank=True, null=True, verbose_name=_('Address line 1'))
	address_line2 = models.CharField(max_length=1024, default=None, blank=True, null=True, verbose_name=_('Address line 2'))

	cell_phone = models.CharField(max_length=10, default=None, blank=True, null=True, verbose_name=_('Cell phone'))
	home_phone = models.CharField(max_length=10, default=None, blank=True, null=True, verbose_name=_('Home phone'))
	other_phone = models.CharField(max_length=10, default=None, blank=True, null=True, verbose_name=_('Other phone'))

	@property
	def full_name(self):
		result=self.first_name
		if self.middle_name and self.middle_name is not None and len(self.middle_name.strip()) > 0:
			result+=' ' + str(self.middle_name)
		result+=' ' + str(self.last_name)
		if self.mothers_last_name and self.mothers_last_name is not None and len(self.mothers_last_name.strip()) > 0:
			result+=' ' + str(self.mothers_last_name)
		return result

	@property
	def gender_full_str(self):
		if self.gender=='M':
			return _('Male')
		return _('Female')
	
	@property
	def email_readable(self):
		if self.email is not None:
			return self.email
		return ''

	@property
	def cell_phone_readable(self):
		if self.cell_phone is not None:
			return self.cell_phone
		return ''

	@property
	def age(self):
		dummy=pgettext('person model', 'Age')
		'''
		Code taken from https://www.geeksforgeeks.org/python-program-to-calculate-age-in-year/
		Approach 3: Efficient datetime approach,
		deal with a special case i.e. when birth date is February 29 
		and the current year is not a leap year.
		'''
		today = date.today() 
		try:  
			birthday = self.dob.replace(year = today.year) 
			# raised when birth date is February 29 
			# and the current year is not a leap year 
		except ValueError:  
			birthday = self.dob.replace(\
				year = today.year, \
					month = self.dob.month + 1, \
						day = 1) 

		if birthday > today: 
			return today.year - self.dob.year - 1
		else: 
			return today.year - self.dob.year
	
	def __str__(self):
		return self.full_name

	class Meta:
		abstract = True
		#unique_together = ('last_name', 'mothers_last_name', 'first_name', 'middle_name', 'gender', 'dob', 'city', 'address_line1')

class ObjectWithAddress(MyModel):
	def __init__(self, *args, **kwargs):
		super(ObjectWithAddress, self).__init__(*args, **kwargs)

	#city = models.ForeignKey(City, on_delete=models.PROTECT, default=None, blank=False, null=False, db_column='city_id', verbose_name=_('City'))
	address_line1 = models.CharField(max_length=1024, default=None, blank=False, null=False, verbose_name=_('Address line 1'))
	address_line2 = models.CharField(max_length=1024, default=None, blank=True, null=True, verbose_name=_('Address line 2'))

	email = models.CharField(max_length=254, default=None, blank=False, null=False, verbose_name=_('Email'), unique=True)
	cell_phone = models.CharField(max_length=10, default=None, blank=False, null=False, verbose_name=_('Cell phone'))
	home_phone = models.CharField(max_length=10, default=None, blank=True, null=True, verbose_name=_('Home phone'))
	other_phone = models.CharField(max_length=10, default=None, blank=True, null=True, verbose_name=_('Other phone'))

	class Meta:
		abstract = True