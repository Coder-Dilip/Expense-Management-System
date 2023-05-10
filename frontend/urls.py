from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
path("",views.index),
path("login/",views.login_view),
path('register/',views.register_user),
path("contact/",views.contact),
path("forgot-password/",views.forgot_password),
path("forgot-password2/",views.forgot_password2),
path("forgot-password3/",views.forgot_password3),
path('budget-calculator/',views.budget_calculator),
path('blog',views.blog),
path('about',views.about),
path('posts',views.posts),
path('create-post',views.create_post),
    path('posts-json/', views.posts_json, name='posts-json'),
    path('leaderboard/',views.leaderboard),
    path('services/',views.services),
    path("nepal_budget_status/",views.nepal_budget_status)
]