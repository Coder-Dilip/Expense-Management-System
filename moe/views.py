from django.shortcuts import render,redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from frontend.models import School
from school.models import SchoolBudget, SchoolForm
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


@login_required(login_url="/login/")
def verify_school(request, username):
    current_logged_in=request.user
    if School.objects.filter(user=current_logged_in).exists():
        return redirect('/')
    else:
        school_form = SchoolForm.objects.get(username=username)
        usr=User.objects.get(username=username)
        school=School.objects.get(user=usr)
        school.status="old"
        school_form.status = 1
        new_budget = SchoolBudget(school_username=username)
        new_budget.save()
        school_form.save()
        school.save()
        return redirect('/admin-dashboard')

def distribute_budget(request, username):
    school = SchoolForm.objects.get(username=username)
    context = {
        'school': school
    }
    return render(request, 'moe/distribute.html', context)



def school_budget_table(request):
    # Get all SchoolBudget instances where 'distributed' is False
    budgets = SchoolBudget.objects.filter(distributed=False)
    print(budgets)
    # Create a list of dictionaries with required fields for each instance
    budget_data = []
    for budget in budgets:
        budget_data.append({
            'username': budget.school_username,
            'image': SchoolForm.objects.get(username=budget.school_username).image_file.url,
            'distributed': 'pending'
        })

    print(budget_data)
    # Render the data in a template
    return render(request, 'moe/school_budget_table.html', {'budget_data': budget_data})
    

def school_distribute(request, username):
    if request.method=="POST":
        print('lol')
        total=int(request.POST.get('total_budget'))
        total=total-0.01*total
        food = int(request.POST.get('food'))
        school_items = int(request.POST.get('school_items'))
        health = int(request.POST.get('health'))
        transportation = int(request.POST.get('transportation'))
        clothes = int(request.POST.get('clothes'))
        bills = int(request.POST.get('bills'))
        sports = int(request.POST.get('sports'))
        extra_curricular = int(request.POST.get('extra_curricular'))
        s=food+school_items+health+transportation+clothes+bills+sports+extra_curricular
        if s!=100:
            return render(request,'moe/school_distribute.html',{'username':username,'message':'The total percentage is either greather than 100 or less than 100. please make it exact 100 in total'})
        sb=SchoolBudget.objects.filter(school_username=username).first()
        
        sb.school_username = username
        sb.school_items = (school_items/100)*total   # computer marker desk table pen paper etc  
        sb.food=(food/100)*total
        sb.health = (health/100)*total  #first aid kit sanitary pads
        sb.transportation = (transportation/100)*total  # buses
        sb.clothes = (clothes/100)*total  # uniform shoes tie
        sb.bills = (bills/100)*total   # electricity water gas internet
        sb.sports = (sports/100)*total  # sports related 
        sb.extra_curricular = (extra_curricular/100)*total  #events, programs
        sb.distributed = True #whether distributed or not
        
        sb.save()
        # return render(request,"moe/school_distribute.html",{'username':username,'message':"connect ips gateway"})
        return redirect(f"https://connect-ips.web.app?username={username}&amount={total}")

    return render(request,"moe/school_distribute.html",{'username':username,'message':""})



