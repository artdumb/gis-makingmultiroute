from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators    .csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from . import siutang_module


@method_decorator(csrf_exempt, name='dispatch')
class makingrouteAPI(APIView):

    def post(self, request):
        data = json.loads(request.body)
        # 첫번째 결과는 경로에 대하여 상세정보 리스트
        # 두번째 결과는 모든 위치와 경로의 소요시간 및 다른 속성정보 리스트
        all_result = siutang_module.eachpointrout(data)
        M = dict(zip(range(1, len(all_result) + 1), all_result))
        return JsonResponse(M, status=200)
