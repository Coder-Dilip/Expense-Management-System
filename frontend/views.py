from django.shortcuts import render,redirect

from school.models import DailySaving, SchoolForm
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,JsonResponse
from .models import School,Posts
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.core import serializers
def index(request):
    return render(request,"frontend/index.html")



@csrf_exempt
def login_view(request):
    form = forms.LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if School.objects.filter(user=user).exists():
                   school_form = School.objects.get(user=user)
                   try:
                    form_details=SchoolForm.objects.get(username=school_form.user.username)
                    status = school_form.status
                    if status=='new':
                        return redirect('/school-form')
                    else:
                            return redirect(f'/school-dashboard?key={school_form.user.username+"-"+str(form_details.image_file)}') # Redirect to home page
                   except:
                    return redirect('/school-form')
                else:
                    return redirect("/admin-dashboard")
                
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    
    

    return render(request, "frontend/home/login.html", {"form": form, "msg": msg})



@csrf_exempt
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            status = "new" # set default status
            answer = request.POST.get('security_question')
            School.objects.create(user=user, status=status,security_question="first word of the school if you want to rename your school",security_answer=answer)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True


        else:
            msg = 'Form is not valid'
    else:
        form = forms.SignUpForm()

    return render(request, "frontend/home/register.html", {"form": form, "msg": msg, "success": success})

from decouple import config
def contact(request):
    reply="hello"
    
    # reply=reply.replace("\n", "<br>")
    
    # Return the JSON response
    # return HttpResponse(response.choices[0].text)
    # Save the generated text to a file
    dat={"reply":reply}

    return render(request, "frontend/home/contact.html",dat)


def forgot_password(request):
    if request.method=="POST":
        username=request.POST.get('username')
        print("username")
        return redirect(f"/forgot-password2?key={username}")

    return render(request, "frontend/home/forgot_password.html")

def forgot_password2(request):
    message=''
    if request.method=="POST":
        username=request.POST.get('username')
        answer=request.POST.get("answer")
        curr_user=User.objects.get(username=username)
        school_user=School.objects.get(user=curr_user)
        if school_user.security_answer==answer:

         return redirect(f"/forgot-password3?key={username}")
        else:
            print("Security answer invalid")
            message="Security answer invalid"

    return render(request, "frontend/home/forgot_password2.html",{'data':message})

def forgot_password3(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get("password")
        user = User.objects.get(username=username)

    # Set the new password for the user

        user.set_password(password)

    # Save the user object to update the password in the database
        user.save()
        return redirect("/login")
    

    return render(request, "frontend/home/forgot_password3.html")

def budget_calculator(req):
    return render(req, 'frontend/home/calculator.html')


def blog(req):
    return render(req,'frontend/home/blog.html')


def about(req):
    return render(req,'frontend/home/about.html')


@login_required(login_url="/login/")
def posts(req):
    return render(req,'frontend/home/posts.html')


def create_post(request):
    if request.method == 'POST':
        user = request.user
        description = request.POST.get('description')
        image_file = request.FILES.get('image')
        post = Posts(user=user, description=description, image_file=image_file)
        post.save()
        return JsonResponse({'success': True})
    return redirect('/posts')



def posts_json(request):
    posts = Posts.objects.all()
    data = []
    for post in posts:
        # Serialize the Posts instance to a dictionary
        post_dict = serializers.serialize('python', [post])[0]['fields']
        # Get the User object associated with the post and serialize it to a dictionary
        user_dict = serializers.serialize('python', [post.user])[0]['fields']
        # Add the username from the User object to the Posts dictionary
        post_dict['username'] = user_dict['username']
        # Add the updated Posts dictionary to the data list
        data.append(post_dict)
    # Serialize the data list to JSON and return it
    return JsonResponse(data, safe=False)


def leaderboard(request):
    return render(request, 'frontend/home/leaderboard.html')






