from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework import status
import json

from django.contrib.auth.models import User
from mymeter.models import accounts, sub_area, meters


import numpy as np


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
        data = json.loads(str(request.body, encoding='utf-8'))
        return Response([{"meter_id": "1",
                          "month": {"text": data['month'],
                                    "vspp":list(np.random.randint(low=2003, high=2334, size=31)),
                                    "grid":list(np.random.randint(low=409, high=899, size=31))},
                          "day": {"text": data['date'],

                                  "vspp": [0, 0, 0, 0, 0, 0, 0, 0] + list(np.random.randint(low=20, high=60, size=4)),
                                  "grid": list(np.random.randint(low=20, high=60, size=8))+[0, 0, 0, 0, 0, 0, ]},
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
                                    "vspp":list(np.random.randint(low=2003, high=2334, size=31)),
                                    "grid":list(np.random.randint(low=409, high=899, size=31))},
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
                                  "vspp": [0, 0, 0, 0, 0, 0, 0, 0]+list(np.random.randint(low=20, high=60, size=9))+[0, 0, 0, 0, 0, 0,
                                           0],
                                  "grid": list(np.random.randint(low=0, high=30, size=8))+list(np.random.randint(low=0, high=20, size=9))+list(np.random.randint(low=0, high=30, size=7))
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
def register(request):
    try:

        pass
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def signin(request):
    try:
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
        print(token)
        return Response({
            'user': user_serialized.data,
            'expires_in': expires_in(token),
            'token': token.key,
            'userDetail' : {}
        }, status=HTTP_200_OK)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def user_info(request):
    try:
        data = request.data
        header = request.headers
        user=User.objects.get(username=data['username'])
        token, _ = Token.objects.get_or_create(user=user)
        if (str(token) == header['Authorization'].split(' ')[1]):
            return Response({
                'user': request.user.username,
                'expires_in': expires_in(request.auth)
            }, status=HTTP_200_OK)
        else:
            return Response('Error on authentication')
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_package(request):
    """
    this function updates user's package  {"username":"PEA001", "method":"update_package", "detail":{"new_package":"2"}}
    :param package name
    """
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        header = request.headers
        if (data['method']=='update_package'):
            user = User.objects.get(username=data['username'])
            acc = accounts.objects.get(owner=user)
            old_package = str(acc.package_type)
            acc.changePackage(package=data['detail']['new_package'])
            user = User.objects.get(username=data['username'])
            token, _ = Token.objects.get_or_create(user=user)
            if (str(token) == header['Authorization'].split(' ')[1]):
                return Response({
                    'text': 'okay',
                    'user': data['username'],
                    'old_package': old_package,
                    'new_package': data['detail']['new_package']
                }, status=HTTP_200_OK)
            else:
                return Response('Error on authentication')
        else:
            return Response('Error method')
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def getCarbonReduce(request):
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        header = request.headers
        if (data['method']=='getCarbonReduce'):
            user = User.objects.get(username=data['username'])
            token, _ = Token.objects.get_or_create(user=user)
            if (str(token) == header['Authorization'].split(' ')[1]):
                acc = accounts.objects.get(owner=user)
                met = meters.objects.get(owner=acc)
                return Response({
                    'text': 'okay',
                    'user': data['username'],
                    'carbonReduce': met.carbonReduce,
                }, status=HTTP_200_OK)
            else:
                return Response('Error on authentication')
        else:
            return Response('Error method')
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def getUsage(request):
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        header = request.headers
        if (data['method']=='getUsage'):
            user = User.objects.get(username=data['username'])
            token, _ = Token.objects.get_or_create(user=user)
            if (str(token) == header['Authorization'].split(' ')[1]):
                acc = accounts.objects.get(owner=user)
                met = meters.objects.get(owner=acc)
                return Response({
                    'text': 'okay',
                    'user': data['username'],
                    'lastMonth': 'พฤศจิกายน',
                    'total':2039,
                    'grid':1392,
                    'vspp':2039-1392,
                }, status=HTTP_200_OK)
            else:
                return Response('Error on authentication')
        else:
            return Response('Error method')
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def getRemainPackage(request):
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        header = request.headers
        if (data['method']=='getRemainPackage'):
            user = User.objects.get(username=data['username'])
            token, _ = Token.objects.get_or_create(user=user)
            if (str(token) == header['Authorization'].split(' ')[1]):
                acc = accounts.objects.get(owner=user)
                met = meters.objects.get(owner=acc)
                return Response({
                    'text': 'okay',
                    'user': data['username'],
                    'used': 1239,
                    'remain': 320
                }, status=HTTP_200_OK)
            else:
                return Response('Error on authentication')
        else:
            return Response('Error method')
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def getPackage(request):
    """
    this function updates user's package  {"username":"PEA001", "method":"update_package", "detail":{"new_package":"2"}}
    :param package name
    """
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        header = request.headers
        if (data['method']=='getPackage'):
            user = User.objects.get(username=data['username'])
            acc = accounts.objects.get(owner=user)
            package = str(acc.package_type)
            user = User.objects.get(username=data['username'])
            token, _ = Token.objects.get_or_create(user=user)
            if (str(token) == header['Authorization'].split(' ')[1]):
                return Response({
                    'text': 'okay',
                    'user': data['username'],
                    'package': package,
                }, status=HTTP_200_OK)
            else:
                return Response('Error on authentication')
        else:
            return Response('Error method')
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def getProfile(request):
    """
    this function updates user's package  {"username":"PEA001", "method":"update_package", "detail":{"new_package":"2"}}
    :param package name
    """
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        header = request.headers
        if (data['method']=='getProfile'):
            user = User.objects.get(username=data['username'])
            token, _ = Token.objects.get_or_create(user=user)
            if (str(token) == header['Authorization'].split(' ')[1]):
                if str(user)=='PEA001':
                    return Response({
                        'text': 'okay',
                        'user': data['username'],
                        'place':'Inthanin',
                        'CA':'20299491023',
                        'name':'คุณเส็ง',
                        'tel':'092838482',
                        'email':'seng.@inthanin.com'
                }, status=HTTP_200_OK)
                elif str(user)=='PEA002':
                    return Response({
                        'text': 'okay',
                        'user': data['username'],
                        'place':'PEA innovatin hub',
                        'CA':'2399481012',
                        'name':'คุณมุก',
                        'tel':'0923329123',
                        'email':'mizkaimook@ihub.com'
                }, status=HTTP_200_OK)
                elif str(user)=='PEA003':
                    return Response({
                        'text': 'okay',
                        'user': data['username'],
                        'place':'PEA Coop',
                        'CA':'2399488501',
                        'name':'ผจก.',
                        'tel':'092838482',
                        'email':'xxx@PEACOOP.com'
                }, status=HTTP_200_OK)
                else:
                    return Response({
                        'text': 'okay',
                        'user': data['username'],
                        'place':'Inthanin',
                        'CA':'20299491023',
                        'name':'คุณเส็ง',
                        'tel':'092838482',
                        'email':'seng.@inthanin.com'
                }, status=HTTP_200_OK)
            else:
                return Response('Error on authentication')
        else:
            return Response('Error method')
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def getUsage2(request):
    """
    this function updates user's package  {"username":"PEA001", "method":"update_package", "detail":{"new_package":"2"}}
    :param package name
    """
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        header = request.headers
        if (data['method']=='getUsage2'):
            user = User.objects.get(username=data['username'])
            token, _ = Token.objects.get_or_create(user=user)
            if (str(token) == header['Authorization'].split(' ')[1]):
                if str(user)=='PEA001':
                    return Response({
                        'text': 'okay',
                        'user': data['username'],
                        'total' : [2093,2291,2729,2842,2923,2349,2212,2324,2192,1992],
                        'vspp' : [1093,1291,1329,1442,1123,1342,1312,1224,1292,1092],
                }, status=HTTP_200_OK)
                elif str(user)=='PEA002':
                    return Response({
                        'text': 'okay',
                        'user': data['username'],
                        'total':[493,691,829,942,1223,1249,812,724,892,992],
                        'vspp':[239,212,322,422,223,123,323,332,233,232],
                }, status=HTTP_200_OK)

                elif str(user)=='PEA003':
                    return Response({
                        'text': 'okay',
                        'user': data['username'],
                        'total':[4493,4691,4829,4942,4223,4249,4812,4724,4892,4992],
                        'vspp':[2239,2212,2322,2422,2223,2123,2323,2332,2233,2232],
                }, status=HTTP_200_OK)

                else:
                    return Response({
                        'text': 'okay',
                        'user': data['username'],
                        'total': [4493, 4691, 4829, 4942, 4223, 4249, 4812, 4724, 4892, 4992],
                        'vspp': [2239, 2212, 2322, 2422, 2223, 2123, 2323, 2332, 2233, 2232],
                    }, status=HTTP_200_OK)
            else:
                return Response('Error on authentication')
        else:
            return Response('Error method')
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)