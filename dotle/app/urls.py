from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("classic/", views.index, name="index"),
    path("classic/<str:date>", views.classic_by_date, name="classic_by_date"),
    path("ranked/", views.ranked, name="ranked"),
    path("ranked/<str:date>", views.ranked_by_date, name="ranked_by_date"),
    path("api/get_heroes/", views.get_heroes, name="get_heroes"),
    path("api/reroll_hero/", views.reroll_hero, name="reroll_hero"),
    path("api/generate_hero/", views.generate_hero, name="generate_hero"),
    path("api/get_date_range/", views.get_date_range, name="get_date_range"),
    path('api/login_ajax/', views.login_ajax, name='login_ajax'),
    path('profile', views.profile, name='profile'),
]
