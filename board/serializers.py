from rest_framework import serializers
from .models import Board, Comment
from django.utils import timezone

class PostResponseSerializer(serializers.ModelSerializer): #게시물 업로드한 결과값 직렬화
    created_at = serializers.SerializerMethodField()
    #nickname = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id', 'user', 'nickname', 'title', 'body', 'created_at', 'comments'] #nickname 일단 여기 넣음
    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')


class PostListSerializer(serializers.ModelSerializer): #전체 블로그 목록 (list) 불러올때 직렬화
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id', 'user', 'nickname', 'created_at', 'title'] 
    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')


class PostRequestSerializer(serializers.ModelSerializer): #새로운 게시물 post할 때 직렬화
    class Meta:
        model = Board
        fields = ['title', 'body']

class CommentRequestSerializer(serializers.ModelSerializer): #댓글 post할때 직렬화
    class Meta:
        model = Comment
        fields = ['comment']
        
class CommentResponseSerializer(serializers.ModelSerializer): #댓글 post/get할때 response(결괏값)를 직렬화
    created_at = serializers.SerializerMethodField()
    # nickname = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'user', 'nickname', 'comment', 'created_at']
    def get_created_at(self, obj): #함수이름을 'get_[변경하고싶은필드명]' 형식으로 적고 선언해서 필드값을 변환할 수 있음.
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')
    #def get_nickname(self, obj):

class PostDetailSerializer(serializers.ModelSerializer): #상세 게시글 불러올때 직렬화 => 댓글도 같이 불려와야하므로 댓글도 직렬화 필요!
    created_at = serializers.SerializerMethodField()
    # nickname = serializers.SerializerMethodField()
    comments = CommentResponseSerializer(many=True, read_only=True) #read_only를 안 걸면 유저가 코멘트의 필드를 안채울경우 오류가 발생해버림
    class Meta:
        model = Board
        fields = ['id', 'user', 'nickname', 'title', 'body', 'created_at', 'comments']
    def get_created_at(self, obj): #함수이름을 'get_[변경하고싶은필드명]' 형식으로 적고 선언해서 필드값을 변환할 수 있음.
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')





