from django.shortcuts import render,redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

@login_required(login_url="/login/")
def index(request):
    return render(request,"moe/index.html")


def logOut(request):
    logout(request)
    return redirect("/")
    
@login_required(login_url="/login/")
def profile(request):
    return render(request,"moe/profile.html")

@login_required(login_url="/login/")
def icons(request):
    return render(request,"moe/icons.html")

@login_required(login_url="/login/")
def table(request):
    return render(request,"moe/tables.html")





# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template

#         html_template = loader.get_template('moe/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('moe/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('moe/page-500.html')
#         return HttpResponse(html_template.render(context, request))
    
