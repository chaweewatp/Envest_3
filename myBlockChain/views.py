from django.shortcuts import render

# Create your views here.
from Crypto.Signature import DSS
from Crypto.Hash import SHA3_256
from Crypto.PublicKey import ECC
from Crypto import Random
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
