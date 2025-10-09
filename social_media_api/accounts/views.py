from rest_framework import generics, permissions
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email
            })
        return Response({'error': 'Invalid credentials'}, status=400)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user




@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Authenticated user follows user with id=user_id.
    Idempotent — following twice does nothing.
    """
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({'detail': "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    request.user.following.add(target)
    return Response({'detail': f'Now following {target.username}'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Authenticated user unfollows user with id=user_id.
    Idempotent.
    """
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({'detail': "You can't unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    request.user.following.remove(target)
    return Response({'detail': f'Unfollowed {target.username}'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def following_list(request):
    """
    List users the current user is following.
    """
    following_qs = request.user.following.all()
    data = [{'id': u.pk, 'username': u.username} for u in following_qs]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def followers_list(request, user_id=None):
    """
    If user_id provided, list followers of that user. Otherwise, list followers of current user.
    """
    if user_id:
        user = get_object_or_404(User, pk=user_id)
    else:
        user = request.user
    followers_qs = user.followers.all()
    data = [{'id': u.pk, 'username': u.username} for u in followers_qs]
    return Response(data, status=status.HTTP_200_OK)

