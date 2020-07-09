from django.shortcuts import render

def terms_conditions(request):
	return render(request,'legal/terms-conditions.html')

def privacy(request):
	return render(request,'legal/privacy.html')

def license(request):
	return render(request,'legal/license.html')

def join_us(request):
	return render(request,'legal/joinus.html')