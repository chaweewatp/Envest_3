
from django.shortcuts import render

# Create your views here.


def createTimeSlot():
    """
        This function generate string value of time slot for each hour in a day

        example
        input: None
        return: ## 140007092020 (start-hour + date + month + year)
    """

    return "140007092020"