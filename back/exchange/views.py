import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

class ExchangeRateAPIView(APIView):
    def get(self, request, format=None):
        from datetime import datetime, timedelta
        
        api_key = settings.EXIMBANK_API_KEY
        url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
        
        # 요청된 날짜 가져오기
        requested_date = request.query_params.get('date')
        
        # 현재 날짜
        today = datetime.now()
        
        # 주말인 경우 이전 금요일의 날짜를 사용
        if today.weekday() == 5:  # 토요일
            today = today - timedelta(days=1)
        elif today.weekday() == 6:  # 일요일
            today = today - timedelta(days=2)
            
        # 요청 날짜가 오늘보다 미래인 경우 오늘 날짜 사용
        if requested_date > today.strftime('%Y%m%d'):
            search_date = today.strftime('%Y%m%d')
        else:
            search_date = requested_date
            
        params = {
            "authkey": api_key,
            "searchdate": search_date,
            "data": "AP01"
        }

        try:
            response = requests.get(url, params=params, verify=False)
            if response.status_code == 200:
                data = response.json()
                
                # API 응답이 비어있거나 에러인 경우
                if not data or isinstance(data, dict):
                    # 하루 전 날짜로 재시도
                    yesterday = (datetime.strptime(search_date, '%Y%m%d') - timedelta(days=1))
                    params['searchdate'] = yesterday.strftime('%Y%m%d')
                    response = requests.get(url, params=params, verify=False)
                    if response.status_code == 200:
                        data = response.json()
                
                target_currency = request.query_params.get('target', 'USD')
                
                for item in data:
                    if item['cur_unit'] == target_currency:
                        return Response({
                            'currency': target_currency,
                            'base': "KRW",
                            'rate': item['deal_bas_r'],
                            'date': params['searchdate']  # 실제 조회된 날짜 반환
                        })
                        
                return Response({'error': 'Invalid target currency'}, status=400)
            return Response({'error': 'API request failed'}, status=500)
        except Exception as e:
            return Response({'error': str(e)}, status=500)