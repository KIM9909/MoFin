import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

class ExchangeRateAPIView(APIView):
    def get(self, request, format=None):
        api_key = settings.EXIMBANK_API_KEY
        url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
        params = {
            "authkey": api_key,
            "searchdate": request.query_params.get('date', '20241119'),
            "data": "AP01"
        }

        try:
            response = requests.get(url, params=params, verify=True)
            if response.status_code == 200:
                data = response.json()
                target_currency = request.query_params.get('target', 'USD')

                for item in data:
                    if item['cur_unit'] == target_currency:
                        return Response({
                            'currency': target_currency,
                            'base': "KRW",
                            'rate': item['deal_bas_r']
                        })
                return Response({'error': 'Invalid target currency'}, status=400)
            return Response({'error': 'API request failed'}, status=500)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
