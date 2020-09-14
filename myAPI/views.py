from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
# Create your views here.

@api_view(['POST'])
def getEnergyData(request):
    """
    This function provides API for client.
    :param request: meter id
    :return: meter id, vspp and grid energy on current month and day
    """
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        return Response({"meter_id" : "1",
                         "month":{
                             "vspp":[13, 23,40, 55, 20,50,30,20,10,20,4,5,60,1,23,4,20,4,5,60,1,23,4],
                             "grid":[13, 23,40, 55, 20,50,30,20,10,20,4,5,60,1,23,4,20,4,5,60,1,23,4]},
                         "day":{
                             "vspp": [3, 5, 5, 6, 2, 3, 2, 1, 7, 20, 4, 5, 60],
                             "grid": [13, 23, 40, 55, 20, 50, 30, 20, 10, 20, 4, 5, 60,]}
                         })
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def getEnergyDataMonth(request):
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        return Response({"meter_id" : "1",
                         "month": {
                             "vspp": [13, 23, 40, 55, 20, 50, 30, 20, 10, 20, 4, 5, 60, 1, 23, 4, 20, 4, 5, 60, 1, 23,
                                      23, 4, 20, 4, 5, 60, 1, 23,
                                      ],
                             "grid": [13, 23, 40, 55, 20, 50, 30, 20, 10, 20, 4, 5, 60, 1, 23, 4, 20, 4, 5, 60, 1, 23,
                                      4, 40, 55, 20, 50, 4, 5, 60]}
                         })

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def getEnergyDataDay(request):
    try:
        data = json.loads(str(request.body, encoding='utf-8'))
        return Response({"meter_id" : "1",
                         "day":{
                             "vspp": [3, 5, 5, 6, 2, 3, 2, 1, 7, 20, 4, 5, 60, 13, 23, 40, 55, 20, 50, 30, 20, 10, 20, 4],
                             "grid": [13, 23, 40, 55, 20, 50, 30, 20, 10, 20, 4, 5, 60,3, 5, 5, 6, 2, 3, 2, 1, 7, 20, 4 ]}
                         })
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
