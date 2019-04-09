from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
# Create your views here.
from order.pay import AliPay


class GoodDetail(APIView):
    def get(self, request):
        return render(request, 'good_detail.html', locals())


