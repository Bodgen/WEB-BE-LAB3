from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from blog.models import Post, Person
from blog.serializers import PostSerializer, CommentSerializer, PersonSerializer


@api_view(['POST'])
def share_post(request, profile_id):
    try:
        person = Person.objects.get(profile_id=profile_id)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    post = Post.objects.get(identifier=request['data'].get('identifier'))
    serializer = PostSerializer(post)
    post.sharedTo = person

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=PersonSerializer)
@api_view(['POST'])
def register_user(request):
    serializer = PersonSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=PersonSerializer)
@api_view(['POST'])
def login_user(request):
    person = get_object_or_404(Person, username=request.data.get('username'))

    if person.check_password(request.data.get('password')):
        return Response({
            "profileId": person.profileId,
            "birthdate": person.birthdate,
            "email": person.email,
            "username": person.username,
        }, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def post_list(request, profile_id):
    author = get_object_or_404(Person, profileId=profile_id)
    posts = Post.objects.filter(author=author)
    serializer = PostSerializer(posts, many=True)
    result = []

    for post in Post.objects.filter(shared_to=author):
        result.append({
            "identifier": post.identifier,
            "description": post.description,
            "deadline": post.deadline
        })

    return Response({'result': serializer.data})


@swagger_auto_schema(method='post', request_body=PostSerializer)
@api_view(['POST'])
def add_post_list(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: PostSerializer()})
@swagger_auto_schema(method='put', request_body=PostSerializer, responses={200: PostSerializer(), 400: 'Invalid data'})
@swagger_auto_schema(method='delete', responses={204: 'No content'})
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='post', request_body=CommentSerializer)
@api_view(['POST'])
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(post=post, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Add a user to the 'online_users' group
def user_online(profile_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_add)('online_users', str(profile_id))


# Remove a user from the 'online_users' group
def user_offline(profile_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_discard)('online_users', str(profile_id))


# View to get the count of online users (only accessible to superuser)
def online_users(request):
    if request.user.is_superuser:
        channel_layer = get_channel_layer()
        online_users = async_to_sync(channel_layer.group_channels)('online_users')
        return JsonResponse({'online_users': online_users})
    else:
        return JsonResponse({'error': 'Only superuser can access this endpoint'}, status=401)
