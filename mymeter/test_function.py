import numpy as np
from .models import time_slot
def allocate(consumption_data, generation_data):
    """
        Take array of consumption and generation data,
        and return array of matched renewable energy,
        grid energy and amount of renewable energy feed back to grid

        i.e.
        input =
        output =
    """
    vspp_consumption=np.zeros(consumption_data.shape)
    grid_consumption=np.zeros(consumption_data.shape)
    remaining_vspp_energy=np.copy(generation_data)
    for i in np.arange(remaining_vspp_energy.size): # each time period
        # print('time period :' + str(i))
        for j in np.arange(len(consumption_data[:,i])): # each consumption
            # print('consumption data : '+ str(consumption_data[j,i]) + ' remaining vspp energy : '+ str(remaining_vspp_energy[i]))
            if consumption_data[j,i] <= remaining_vspp_energy[i]:
                vspp_consumption[j,i]=np.copy(consumption_data[j,i])
                remaining_vspp_energy[i]=np.copy(remaining_vspp_energy[i])-np.copy(vspp_consumption[j,i])
            elif consumption_data[j,i] > remaining_vspp_energy[i]:
                vspp_consumption[j, i] = np.copy(remaining_vspp_energy[i])
                remaining_vspp_energy[i]=0
                grid_consumption[j,i]=np.copy(consumption_data[j,i])-np.copy(vspp_consumption[j, i])
    return vspp_consumption, grid_consumption,remaining_vspp_energy

def get_random_consumption():
    """
        Return an array of consumption data that is generated by random function
    """
    return True

# user1_consumption=[50,40,50,20,50]
# user2_consumption=[100,40,20,10,5]
# user3_consumption=[300,200, 100, 500,200]
# user4_consumption=[40,23,9,10,30]
# generation1 = [100,60,40,50,10]
# generation2 = [30,80,40,20,10]
# generation3 = [32,75,44,22,30]
# generation4 = [35,64,37,23,50]
#
# vspp, grid, remaining_vsppp = allocate(consumption_data=np.array([user1_consumption,user2_consumption,user3_consumption,user4_consumption]),
#                                                    generation_data=np.sum(np.array([generation1,generation2,generation3,generation4]), axis=0))
#
# print(vspp)
# print(grid)
# print(remaining_vsppp)



import requests
import re
from bs4 import BeautifulSoup
import urllib.request as urllib2
import json


def getConsumptinData(date, mid, id):

    # URL = "http://172.30.200.233/bems/manage/report_energy_day.php?date=2020-09-03&mid=41&_=1597134897931"
    URL = "http://172.30.200.233/bems/manage/report_energy_day.php?date={}&mid={}&_={}".format(date, mid, id)

    oururl= urllib2.urlopen(URL).read()
    soup = BeautifulSoup(oururl,  "html.parser")
    script = soup.find('script', type='text/javascript').string

    data = script.replace(" ","")
    consumption = data[data.find('data:')+5:data.find(',]', data.find('data:'))+2]
    period = data[data.find('categories:')+11:data.find(',]', data.find('categories:'))+2]
    return consumption, period

# x,y = getConsumptinData(date='2020-09-03', mid='41', id='1597134897931')
# print(x)
# print(y)


def autoGenerateTimeSlot(time_slot):
    for item1 in ["0{}".format(x) for x in range(0, 10)] + ["1{}".format(x) for x in range(0, 3)]:
        for item2 in ["0{}".format(x) for x in range(0, 10)] + ["1{}".format(x) for x in range(0, 10)] + ["2{}".format(x) for x in range(0, 10)]+ ["3{}".format(x) for x in range(0, 2)]:
            for item3 in ["0{}".format(x) for x in range(0, 10)] + ["1{}".format(x) for x in range(0, 10)] + ["2{}".format(x) for x in range(0, 4)]:
                t = time_slot(text_time="{}00{}{}2020".format(item3, item2, item1))
                t.save()
