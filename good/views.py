from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.


class GoodDetail(APIView):
    def get(self, request):
        return render(request, 'good_detail.html', locals())