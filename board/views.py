from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Board
from .serializers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsOwnerOrReadOnly

'''
전체 게시글 목록 불러오기 
'''
@api_view(['GET', 'POST']) # @는 데코레이터, 특정 요청만 받겠다는 의미=> 여기서는 GET요청만 받겠다
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def board_list(request):
    if request.method == 'GET':
        posts = Board.objects.all() #DB에서 블로그 모델의 객체를 가져오겠음. all()하면 전부 다 가져옴.
        serializer = PostListSerializer(posts, many=True) #여러개 객체를 바꿀때는 many=True 필수 #여기까진 파이썬 딕셔너리로 바뀜 #직렬화 순서 : 파이썬 클래스 - 파이썬 딕셔너리 - 제이슨
        return Response(serializer.data, status=status.HTTP_200_OK) #이 단계에서 딕셔너리-> 제이슨으로 바뀜

    elif request.method == "POST": 
        serializer = PostRequestSerializer(data=request.data) #제이슨-> 파이썬 객체로 가는 역직렬화
        if serializer.is_valid(): #데이터 저장하기 전에 꼭 거쳐야 하는 유효성 검사
            post = serializer.save() #데이터가 DB에 저장됨
            response = PostResponseSerializer(post)
            return Response(response.data, status = status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
'''
게시글 작성하기 / 상세페이지 불러오기 / 게시글 수정하기 / 삭제하기
'''
@api_view(['GET', 'PUT', 'DELETE']) 
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerOrReadOnly])
def board_detail(request, post_id):
    try:
        post = Board.objects.get(pk=post_id) #.get() : 괄호안에 있는 이름에 맞는 객체들을 불러오겠다 #왼쪽의 pk : 블로그의 기본키 명칭(id)/ 오른쪽의 pk: 인자로 받은 pk
        if request.method == 'GET':
            serializer = PostDetailSerializer(post)
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            serializer = PostRequestSerializer(post, data=request.data)
            if serializer.is_valid():
                put = serializer.save()
                response = PostResponseSerializer(put)
                return Response(response.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == "DELETE":
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    except Board.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST', 'GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_detail(request, post_id):
    post = Board.objects.get(pk=post_id)
    if request.method == 'POST':
        serializer = CommentRequestSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(post=post) #왼쪽 post: Comment 모델의 필드중 하나
            response = CommentResponseSerializer(comment)
            return Response(response.data, status = status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        comments = Comment.objects.filter(post=post) #오른쪽 post : 위에서 선언한 post객체 / filter : get과 다르게 여러개 불러올수있음
        serializer = CommentResponseSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['GET'])
# def get_comments(request, post_id):
#     post = Board.objects.get(pk=post_id)
#     comments = Comment.objects.filter(post=post) #오른쪽 post : 위에서 선언한 post객체 / filter : get과 다르게 여러개 불러올수있음
#     serializer = CommentResponseSerializer(comments, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

#특정 게시물의 댓글 삭제하기
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerOrReadOnly])
def del_comment(request, post_id, comment_id):
    post = Board.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post)
    comment = comments.get(pk=comment_id) #이렇게 특정 댓글 불러오는거 맞나?? 헷갈려유
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)