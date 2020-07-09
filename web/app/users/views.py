# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib import messages

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse, HttpResponseRedirect

from django.contrib.auth import logout as logout_django

from django.utils.translation import pgettext
from django.utils.translation import gettext as _

from .forms import SiginForm

from .models import Users, Ratings

from datetime import datetime,timedelta

def __verify_free_version__(request,user):
	year_approved = user.email_approved_when.year
	month_approved = user.email_approved_when.month
	day_approved = user.email_approved_when.day

	hour_approved = user.email_approved_at.hour
	minute_approved = user.email_approved_at.minute

	supported = datetime(year_approved, month_approved, day_approved, hour_approved, minute_approved)
	supported = supported + timedelta(days=15)
	today=datetime.now()

	return today<supported
	#if today > supported:
		#messages.error(request, _('Your free version has expired'))
		#return render(request, 'site/login.html', context={'form': form})

	#return True

'''
def login_page(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/admin/')
	elif request.method == 'GET':
		form = LoginForm()
	else:
		form = LoginForm(request=request, data=request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user=authenticate(request, username=username, password=password)
			if user is not None:
				if user.dropped:
					messages.error(request, _('User account does not exist'))
					return render(request, 'site/login.html', context={'form': form})

				if not user.email_confirmed:
					messages.error(request, _('The email address is not confirmed yet'))
					return render(request, 'site/login.html', context={'form': form})

				if not user.email_approved:
					messages.error(request, _('The email address is not approved yet'))
					return render(request, 'site/login.html', context={'form': form})

				# Check if still active the 'Free version'
				__verify_free_version__(request)

				login(request, user)
				return HttpResponseRedirect('/dashboard/')
				#return admin(request)
			else:
				messages.error(request, _('Invalid username or password'))
				return render(request, 'site/login.html', context={'form': form})
		else:
			email=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user=authenticate_via_email(email,password)
			if user is not None:
				if user.dropped:
					messages.error(request, _('User account does not exist'))
					return render(request, 'site/login.html', context={'form': form})

				if not user.email_confirmed:
					messages.error(request, _('The email address is not confirmed yet'))
					return render(request, 'site/login.html', context={'form': form})

				if not user.email_approved:
					messages.error(request, _('The email address is not approved yet'))
					return render(request, 'site/login.html', context={'form': form})

				# Check if still active the 'Free version'
				__verify_free_version__(request)

				login(request, user)
				return HttpResponseRedirect('/admin/')
			else:
				return render(request, 'site/login.html', context={'form': form})

			#return render(request, 'site/login.html', context={'form': form})

	return render(request, 'site/login.html', context={'form': form})
'''

def signin(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/dashboard/')
	elif request.method == 'GET':
		form = SiginForm()
	else:
		form = SiginForm(request.POST)
		if form.is_valid():
			created,msg=form.sigin(request)
			if created:
				messages.success(request,msg)
				return HttpResponseRedirect('/login/')
			else:
				messages.error(request,msg)
				return render(request, 'admin/signin.html', context={'form': form})
		else:
			return render(request, 'admin/signin.html', context={'form': form})

	return render(request, 'admin/signin.html', context={'form': form})

def logout(request):
	has_rated=True
	email_sent=True
	user_id=None
	comments=''
	stars=0
	if request.user.is_authenticated:
		has_rated=request.user.has_rated()
		if has_rated:
			r=Ratings.objects.get(user=request.user)
			email_sent=r.email_sent
			comments=r.comments
			stars=r.stars
		user_id=request.user.id

	context={
		'has_rated': has_rated, 'userid': user_id,
		'email_sent': email_sent, 'comments': comments,
		'stars': stars
	}
	logout_django(request)
	return render(request,'admin/logout.html',context=context)

def save_rating(request):
	if request.method == 'POST':
		userid=request.POST.get('user', None)
		if not request.user.is_authenticated and userid is None:
			return JsonResponse({'status': 'error', 'msg': _('You do not have permission to perform this request')})

		stars=request.POST.get('rating', None)
		comments=request.POST.get('comments', None)

		if stars is None or len(stars.strip())<1:
			stars=None

		try:
			user=Users.objects.get(pk=userid)
			user.has_rated=True

			try:
				rating=Ratings.objects.get(user=user)
			except ObjectDoesNotExist:
				rating=Ratings(user=user)

			rating.stars=stars
			rating.comments=comments

			from .utils import send_email_user_has_rated
			email_sent,error=send_email_user_has_rated(request, user, stars, comments)
			rating.email_sent=email_sent>0

			with transaction.atomic():
				user.save()
				rating.save()

				if rating.email_sent:
					return JsonResponse({'status': 'success', 'msg': _('Thank you so much for your comments and for rate the app')})
				return JsonResponse({'status': 'warning', 'msg': _('Thank you so much for your comments and for rate the app'), 'error': error})

		except ObjectDoesNotExist:
			return JsonResponse({'status': 'error', 'msg': _('The user you are trying to update does not exist')})

		return JsonResponse({'status': 'success', 'msg': _('The user has been updated successfully')})

	return JsonResponse({'status': 'error', 'msg': _('You do not have permission to perform this request')})

def donate(request):
	return render(request,'donate/donate.html')

def donate_frm(request):
	return render(request,'donate/donate-frm.html')

def donate_charge(request):
	if request.method=='POST':
		amount=request.POST.get("amount", None)
		if amount is None:
			messages.error(request,pgettext('stripe donations', 'The amount is missed'))
			return HttpResponseRedirect('/donate-frm/')

		input_amount=request.POST.get("amount", None)

		exp_month=request.POST.get("exp-month", None)
		if exp_month is None:
			messages.error(request,pgettext('stripe donations', 'The expiration month is missed'))
			return HttpResponseRedirect('/donate-frm/')

		exp_year=request.POST.get("exp-year", None)
		if exp_year is None:
			messages.error(request,pgettext('stripe donations', 'The expiration year is missed'))
			return HttpResponseRedirect('/donate-frm/')

		address_zip=request.POST.get("address-zip", None)
		if address_zip is None:
			messages.error(request,pgettext('stripe donations', 'The address zip is missed'))
			return HttpResponseRedirect('/donate-frm/')

		receipt_email=request.POST.get("receipt_email", None)

		decimal_pos=0
		dec_separator=False
		try:
			dec_separator=amount.index('.')+1
		except ValueError:
			pass

		if dec_separator:
			decimal_pos=len(amount[dec_separator:])
		if decimal_pos==1:
			amount=amount.replace('.','')+'0'
		elif decimal_pos==0:
			amount=amount+'00'
		elif decimal_pos==2:
			amount=amount.replace('.','')
		#amount=int(round(amount))*100
		amount=int(amount)

		from api.stripe import cfg
		import stripe

		session = stripe.checkout.Session.create(
			submit_type='donate',
		  payment_method_types=['card'],
		  line_items=[{
		    'name': _('App name'),
		    'description': _('App name'),
		    'amount': amount,
		    'currency': 'mxn',
		    'quantity': 1,
		  }],
		  success_url='https://localhost:8000/donate-confirm?session_id=dummy',
		  cancel_url='https://localhost:8000/donate-cancel?session_id=dummy',
		)
		#print("******session*****")
		#print(session)
		context={
			'session': session,
			'confirm_url': 'https://localhost:8000/donate-confirm?session_id='+session['id'],
			'stripe_amount': amount, 'input_amount': input_amount,
			'exp_month': exp_month, 'exp_year': exp_year, 
			'address_zip': address_zip,
			'receipt_email': receipt_email
		}
		#return render(request,'donate-charge.html',context=context)
		return render(request,'donate/donate-confirmation.html',context=context)

	return render(request,'donate/donate-charge.html')

#test card: 4242 4242 4242 4242
#https://dashboard.stripe.com/account/details

def donate_confirm(request):
	if request.method=='POST':
		from api.stripe import cfg

		amount=request.POST.get("amount", None)
		input_amount=request.POST.get("input_amount", None)

		if amount is None or input_amount is None:
			messages.error(request,pgettext('stripe donations', 'The amount is missed'))
			return HttpResponseRedirect('/donate-frm/')

		exp_month=request.POST.get("exp-month", None)
		if exp_month is None:
			messages.error(request,pgettext('stripe donations', 'The expiration month is missed'))
			return HttpResponseRedirect('/donate-frm/')

		exp_year=request.POST.get("exp-year", None)
		if exp_year is None:
			messages.error(request,pgettext('stripe donations', 'The expiration year is missed'))
			return HttpResponseRedirect('/donate-frm/')

		address_zip=request.POST.get("address-zip", None)
		if address_zip is None:
			messages.error(request,pgettext('stripe donations', 'The address zip is missed'))
			return HttpResponseRedirect('/donate-frm/')

		#session=request.POST.get('session_id', None)

		receipt_email=request.POST.get("receipt_email", None)
		cardnumber=request.POST.get("cardnumber", None)
		exp_month=request.POST.get("exp-month", None)
		exp_year=request.POST.get("exp-year", None)
		cvc=request.POST.get("cvc", None)

		import stripe
		from stripe.error import InvalidRequestError

		try:
			pm=stripe.PaymentMethod.create(
				type='card',
				card={
					'number': cardnumber,
					'exp_month': exp_month,
					'exp_year': exp_year,
					'cvc': cvc,
				},
			)

			result=False
			if receipt_email is not None:
				result=stripe.PaymentIntent.create(
					amount=int(amount),
					currency='mxn',
					payment_method_types=['card'],
					confirm=True,
					receipt_email=receipt_email,
					payment_method=pm
				)
			else:
				result=stripe.PaymentIntent.create(
					amount=int(amount),
					currency='mxn',
					payment_method_types=['card'],
					confirm=True,
					payment_method=pm
				)
		except InvalidRequestError as e:
			if 'Invalid email address' in e.args[0]:
				result=stripe.PaymentIntent.create(
					amount=int(amount),
					currency='mxn',
					payment_method_types=['card'],
					confirm=True,
					payment_method=pm
				)
			else:
				messages.error(request,e.args[0])
				return HttpResponseRedirect('/donate-frm/')

		context={'result': result, 'amount': input_amount}
		return render(request,'donate/donate-completed.html',context=context)

	return render(request,'donate/donate-confirmation.html')

from django.contrib.auth.views import LoginView

class MyLoginView(LoginView):
	def form_valid(self, form):
		user=form.get_user()

		if user is not None:
			if user.dropped:
				messages.error(self.request, _('User account does not exist'))
				return HttpResponseRedirect('/login/')

			if not user.email_confirmed:
				messages.error(self.request, _('The email address is not confirmed yet'))
				return HttpResponseRedirect('/login/')

			if not user.email_approved:
				messages.error(self.request, _('The email address is not approved yet'))
				return HttpResponseRedirect('/login/')

			# Check if still active the 'Free version'
			if __verify_free_version__(self.request,user):
				return super(MyLoginView,self).form_valid(form)
			else:
				messages.error(self.request, _('Your free version has expired'))
				return HttpResponseRedirect('/login/')