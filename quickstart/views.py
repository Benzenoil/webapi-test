from quickstart.serializers import SnippetSerializer, CreateUserSerializer, UserSerializer, UpdateUserSerializer
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet, User
import base64


@csrf_exempt
def rest_signup(request):
    if request.method == 'POST':
        serializer = CreateUserSerializer(data=request.POST)

        if serializer.is_valid():
            serializer.save()
            response_data = {'message': 'Account successfully created', 'user': serializer.data}
            response_data['user'].pop('password', None)
            return JsonResponse(response_data, status=200)

        response_data = {'message': 'Account creation failed', 'cause': serializer.errors}
        return JsonResponse(response_data, status=400)


@csrf_exempt
def rest_getuser_detail(request, pid):
    try:
        user = User.objects.get(user_id=pid)
    except User.DoesNotExist:
        response_data = {'message': 'No User found'}
        return JsonResponse(response_data, status=404)

    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    token_type, _, credentials = auth_header.partition(' ')

    target = bytes('{0}:{1}'.format(user.user_id, user.password), 'utf-8')
    expected = base64.b64encode(target).decode()
    if token_type != 'Basic' or credentials != expected:
        return JsonResponse({'message': 'Authentication Failed'}, status=401)

    if request.method == 'GET':
        serializer = UserSerializer(user)

        response_data = {'message': 'User details by user_id', 'user': serializer.data}
        return JsonResponse(response_data, status=200)
    elif request.method == 'PATCH':
        data = QueryDict(request.body)

        user_id = data.get('user_id', None)
        password = data.get('password', None)
        nickname = data.get('nickname', None)
        comment = data.get('comment', None)

        response_cause = None
        if user_id or password:
            response_cause = 'not updatable user_id and password'
        elif nickname is None and comment is None:
            response_cause = 'required nickname or comment'

        if response_cause:
            response_data = {'message': 'User updation failed', 'cause': response_cause}
            return JsonResponse(response_data, status=400)

        serializer = UpdateUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            response_data = {'message': 'User successfully updated', 'recipt':[serializer.data]}
            return JsonResponse(response_data, status=200)


@csrf_exempt
def rest_user_update(request, pid):
    try:
        user = User.objects.get(user_id=pid)
    except User.DoesNotExist:
        response_data = {'message': 'No User found'}
        return JsonResponse(response_data, status=404)

    if request.method == 'PATCH':

        serializer = UpdateUserSerializer(data=request.POST)
        serializer_exist = UpdateUserSerializer(user)

        if serializer.is_valid():
            user_id = serializer.data.get('user_id', None)
            password = serializer.data.get('password', None)
            nickname = serializer.data.get('nickname', None)
            comment = serializer.data.get('comment', None)

            if user_id or password:
                response_cause = 'not updatable user_id and password'
            elif nickname is None and comment is None:
                response_cause = 'required nickname or comment'

            if response_cause:
                response_data = {'message': 'User updation failed', 'cause':response_cause}
                return JsonResponse(response_data, status=400)
                return JsonResponse()



            serializer.save()




@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':

        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)