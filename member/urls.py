from django.urls import path
from .views import *

app_name = "member"

urlpatterns = [
    path('signup', register), #회원가입
    path('login', login), #로그인
    path('logout', logout), #로그아웃
    path('info', user_info), #유저 정보 조회
    path('post', user_posts), #유저가 작성한 게시글 목록 조회 
]