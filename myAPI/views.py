from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework import status
import json

from django.contrib.auth.models import User
from mymeter.models  import accounts, sub_area


# Create your views here.

@api_view(['POST'])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated

def getEnergyData(request):
    """
    This function provides API for client.
    :param request: meter id
    :return: meter id, vspp and grid energy on current month and day
    """
    try:
        print('someone')
        data = json.loads(str(request.body, encoding='utf-8'))
        print(data['date'])

        return Response([{"meter_id": "1",
                          "month": {"text": data['month'],
                                    "vspp": [130, 230, 400, 550, 200, 500, 300, 200, 100, 200, 40, 50, 600, 10, 230, 40,
                                             200, 40, 50, 600, 10, 230, 40],
                                    "grid": [130, 230, 400, 550, 200, 500, 300, 200, 100, 200, 40, 50, 600, 10, 230, 40,
                                             200, 40, 50, 600, 10, 230, 40]},
                          "day": {"text": data['date'],
                                  "vspp": [0, 0, 0, 0, 0, 0, 0, 1, 7, 20, 4, 5, 60],
                                  "grid": [13, 23, 40, 55, 20, 50, 30, 0, 0, 0, 0, 0, 0, ]},
                          "year": {"text": data['year']}
                          }])
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated

def getEnergyDataMonth(request):
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        return Response([{"meter_id": "1",
                          "month": {"text": data['month'],
                                    "vspp": [130, 230, 400, 550, 200, 500, 300, 200, 100, 200, 40, 50, 600, 10, 230, 40,
                                             200, 40, 50, 600, 10, 230,
                                             230, 40, 200, 40, 50, 600, 10, 230],
                                    "grid": [130, 230, 400, 550, 200, 500, 300, 200, 100, 200, 40, 50, 600, 10, 230, 40,
                                             200, 40, 50, 600, 10, 230,
                                             400, 400, 550, 200, 500, 40, 50, 600]},
                          "year": {"text": data['year']}
                          }])

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated

def getEnergyDataDay(request):
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        return Response([{"meter_id": "1",
                          "day": {"text": data['date'],
                                  "vspp": [0, 0, 0, 0, 0, 0, 0, 0, 5, 20, 4, 5, 60, 13, 23, 40, 55, 0, 0, 0, 0, 0, 0,
                                           0],
                                  "grid": [13, 23, 40, 55, 20, 50, 30, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 40, 20, 30,
                                           10, 20, 20]
                                  },
                          "month": {"text": data['month']},
                          "year": {"text": data['year']}
                          }])
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def loginUser(request):
    data = json.loads(str(request.body, encoding='utf-8'))
    print(data)
    try:
        user = User.objects.get(username=data['username'])
        if user.check_password(data['password']):
            # TODO: Valid password, insert your code here
            return Response('Password is valid')
        else:
            # TODO: Password not valid, handle it here
            return Response('Password is not valid')
    except User.DoesNotExist:
        # TODO: Your error handler goes here
        return Response('No user')



from django.contrib.auth import authenticate, login


@api_view(['POST'])
def loginUser2(request):
    # username = request.POST['username']
    # password = request.POST['password']
    data = json.loads(str(request.body, encoding='utf-8'))
    user = authenticate(request, username=data['username'], password=data['password'])
    if user is not None:
        print('login success')
        login(request, user)
        # Redirect to a success page.
        return Response('Login success')
    else:
        print('login fail')

        # Return an 'invalid login' error message.
        return Response('Login fail')



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.


from rest_framework.authtoken.models import Token
from .authentication import token_expire_handler, expires_in
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from .serializers import UserSerializer, UserSigninSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated

def signin(request):
    signin_serializer = UserSigninSerializer(data = request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status = HTTP_400_BAD_REQUEST)

    user = authenticate(
            username = signin_serializer.data['username'],
            password = signin_serializer.data['password']
        )

    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)

    #TOKEN STUFF
    token, _ = Token.objects.get_or_create(user = user)
    #token_expire_handler will check, if the token is expired it will generate new one
    is_expired, token = token_expire_handler(token)     # The implementation will be described further
    user_serialized = UserSerializer(user)

    return Response({
        'user': user_serialized.data,
        'expires_in': expires_in(token),
        'token': token.key
    }, status=HTTP_200_OK)


@api_view(["GET"])
def user_info(request):
    return Response({
        'user': request.user.username,
        'expires_in': expires_in(request.auth)
    }, status=HTTP_200_OK)
