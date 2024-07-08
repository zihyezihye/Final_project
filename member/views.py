# from django.shortcuts import render

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from django.contrib.auth import login as django_login, logout as django_logout
# from django.contrib.auth import get_user_model
# from .serializers import CustomRegisterSerializer, CustomUserDetailSerializer, PostListSerializer
# from board.models import Board  

# User = get_user_model()

# @api_view(['POST'])
# def register(request):
#     serializer = CustomRegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save(request=request)
#         return Response({'message': 'Signed up successfully!', 'user': CustomUserDetailSerializer(user).data}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     user = User.objects.filter(username=username).first()
#     if user is None or not user.check_password(password):
#         return Response({'message': 'Account not found.'}, status=status.HTTP_401_UNAUTHORIZED)

#     django_login(request, user)
#     return Response({'message': 'Signed in successfully!'})

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     django_logout(request)
#     return Response({'message': '로그아웃이 성공적으로 완료되었습니다.'})

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_detail(request):
#     serializer = CustomUserDetailSerializer(request.user)
#     return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_posts(request):
#     user = request.user
#     posts = Board.objects.filter(user=user)
#     serializer = PostListSerializer(posts, many=True)
#     return Response(serializer.data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .serializers import CustomRegisterSerializer, CustomUserDetailSerializer
from board.serializers import PostListSerializer
from board.models import Board

User = get_user_model()

@api_view(['POST']) #회원가입
def register(request):
    serializer = CustomRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(request=request)

        # 로그인 처리
        django_login(request, user)

        # 액세스 토큰과 리프레시 토큰 생성
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # 사용자 정보를 시리얼라이즈
        user_serializer = CustomUserDetailSerializer(user)

        return Response({
            'access': access_token,
            'refresh': str(refresh),
            'user': user_serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request): #로그인
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.filter(username=username).first()
    if user is None or not user.check_password(password):
        return Response({'message': '로그인 실패'}, status=status.HTTP_401_UNAUTHORIZED)

    # 로그인 처리
    django_login(request, user)

    # 액세스 토큰과 리프레시 토큰 생성
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # 사용자 정보를 시리얼라이즈
    user_serializer = CustomUserDetailSerializer(user)

    return Response({
        'access': access_token,
        'refresh': str(refresh),
        'user': user_serializer.data
    })

@api_view(['POST']) #로그아웃
@permission_classes([IsAuthenticated])
def logout(request):
    django_logout(request)
    return Response({'message': '로그아웃 되었습니다.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 마이페이지 (유저 정보 조회)
def user_info(request):
    user = request.user

    # 사용자 정보를 시리얼라이즈
    user_serializer = CustomUserDetailSerializer(user)

    return Response({
        'id': user.id,
        'nickname': user.nickname,
        'university': user.university
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_posts(request): #유저가 작성한 게시글 목록 조회
    user = request.user

    # 해당 사용자가 작성한 게시물들을 가져옵니다.
    user_posts = Board.objects.filter(user=user)

    # 게시물들을 시리얼라이즈합니다.
    post_serializer = PostListSerializer(user_posts, many=True)

    return Response(post_serializer.data)
