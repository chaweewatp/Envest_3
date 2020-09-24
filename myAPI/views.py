from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

from django.contrib.auth.models import User
from mymeter.models  import accounts, sub_area


# Create your views here.

@api_view(['POST'])
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
def getEnergyDataDay(request):
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        return Response([{"meter_id": "1",
                          "day": {"text": data['date'],
                                  "vspp": [0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 4, 5, 60, 13, 23, 40, 55, 20, 0, 0, 0, 0, 0,
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

