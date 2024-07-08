from django.urls import path
from .views import *


app_name = 'board'

urlpatterns = [
    path('', board_list), #전체 게시글 목록 조회
    path('', board_list), #게시글 작성
    path('<int:post_id>/', board_detail), #특정 게시글 조회,
    path('<int:post_id>/', board_detail), #특정 게시글 수정,
    path('<int:post_id>/', board_detail), #특정 게시글 삭제,
    path('<int:post_id>/comment/', comment_detail), #특정 게시글의 전체 댓글 목록 조회,
    path('<int:post_id>/comment/', comment_detail), #특정 게시글에 댓글 작성,
    path('<int:post_id>/comment/<int:comment_id>/', del_comment), #특정 게시글의 댓글 삭제
]