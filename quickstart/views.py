from quickstart.serializers import SnippetSerializer, CreateUserSerializer, UserSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet, Signup


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
        user = Signup.objects.get(user_id=pid)
    except Signup.DoesNotExist:
        response_data = {'message': 'No User found'}
        return JsonResponse(response_data, status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)

        response_data = {'message': 'User details by user_id', 'user': serializer.data}
        return JsonResponse(response_data, status=200)


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