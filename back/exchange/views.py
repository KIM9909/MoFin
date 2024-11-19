import requests
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from django.conf import settings

class ExchangeRateAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # API 키 및 기본 URL
        api_key = settings.EXIMBANK_API_KEY  # settings.py에 저장된 API 키
        url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"

        # 요청 파라미터
        params = {
            "authkey": api_key,
            "searchdate": request.query_params.get('date', '20241119'),  # YYYYMMDD 형식
            "data": "AP01"  # 환율 데이터 타입
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            target_currency = request.query_params.get('target', 'USD')  # 목표 통화
            for item in data:
                if item['cur_unit'] == target_currency:
                    return Response({
                        'currency': target_currency,
                        'base': "KRW",
                        'rate': item['deal_bas_r']  # 매매기준율
                    })
            return Response({'error': 'Invalid target currency'}, status=400)
        return Response({'error': 'API request failed'}, status=500)
