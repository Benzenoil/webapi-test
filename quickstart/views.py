from quickstart.serializers import UserSerializer
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from .models import User
import base64


@csrf_exempt
def rest_signup(request):
    if request.method == 'POST':
        data = request.POST
        user_id = data.get('user_id', None)
        password = data.get('password', None)
        nickname = data.get('nickname', None)

        if user_id is None or password is None:
            return JsonResponse({'message': 'Account creation failed', 'cause': 'required user_id and password'},
                                status=400)
        elif len(user_id) < 6:
            return JsonResponse({'message': 'Account creation failed', 'cause': 'The length of user_id is not enough'},
                                status=400)
        elif len(password) < 8:
            return JsonResponse({'message': 'Account creation failed', 'cause': 'The length of password is not enough'},
                                status=400)

        serializer = UserSerializer(data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            response_data = {'message': 'Account successfully created', 'user': serializer.data}
            response_data['user'].pop('password', None)
            response_data['user'].pop('comment', None)
            if nickname is None:
                response_data['user']['nickname'] = user_id
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

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = {'message': 'User successfully updated', 'recipt':[serializer.data]}
            return JsonResponse(response_data, status=200)


@csrf_exempt
def rest_user_delete(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    token_type, _, credentials = auth_header.partition(' ')
    auth_str = base64.b64decode(credentials).decode('utf-8')
    user_pw = auth_str.split(':')
    try:
        user = User.objects.get(user_id=user_pw[0])
    except User.DoesNotExist:
        # To "prevent" user to check whether the user is exist, use 401 instead of user not found
        return JsonResponse({'message': 'Authentication Failed'}, status=401)

    target = bytes('{0}:{1}'.format(user.user_id, user.password), 'utf-8')
    expected = base64.b64encode(target).decode()
    if token_type != 'Basic' or credentials != expected:
        return JsonResponse({'message': 'Authentication Failed'}, status=401)
    elif user_pw[0] == user.user_id:
        user.delete()
        return JsonResponse({'message': 'Account and user successfully removed'}, status=200)
