# recommendations/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from savings.models import DepositProducts, SavingsProducts, DepositOptions, SavingsOptions
from django.db.models import Max, F
from .utils import (
    calculate_age,
    get_life_cycle_recommendation,
    get_income_level_recommendation,
    get_asset_based_recommendation
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    """사용자 맞춤 금융상품 추천 API"""
    try:
        user = request.user
        
        # 필수 정보 확인
        if not all([user.birth, user.annual_income, user.total_assets]):
            return Response({
                'error': '추천을 위해 생년월일, 연소득, 총자산 정보가 필요합니다.'
            }, status=400)
        
        # 나이 계산 및 각 기준별 추천 정보 가져오기
        age = calculate_age(user.birth)
        life_cycle = get_life_cycle_recommendation(age)
        income_level = get_income_level_recommendation(user.annual_income)
        asset_based = get_asset_based_recommendation(user.total_assets)

        # 예금 상품 추천 (소득 수준에 따른 필터링)
        deposit_products = DepositProducts.objects.all()
        if income_level['level'] == '서민층':
            deposit_products = deposit_products.filter(join_deny__in=[1, 2])
        else:
            deposit_products = deposit_products.filter(join_deny=1)

        # 적금 상품 추천
        savings_products = SavingsProducts.objects.all()
        if income_level['level'] == '서민층':
            savings_products = savings_products.filter(join_deny__in=[1, 2])
        else:
            savings_products = savings_products.filter(join_deny=1)

        # 예금 상품 금리 정보 포함
        deposits_with_rates = []
        for deposit in deposit_products:
            max_rate = 0
            options = DepositOptions.objects.filter(product=deposit)
            if options.exists():
                for option in options:
                    rate = option.intr_rate2 if option.intr_rate2 is not None else option.intr_rate
                    if rate and rate > max_rate:
                        max_rate = rate
                
                deposits_with_rates.append({
                    'product': {
                        'fin_prdt_cd': deposit.fin_prdt_cd,
                        'kor_co_nm': deposit.kor_co_nm,
                        'fin_prdt_nm': deposit.fin_prdt_nm,
                        'join_way': deposit.join_way,
                        'etc_note': deposit.etc_note
                    },
                    'max_rate': max_rate
                })

        # 적금 상품 금리 정보 포함
        savings_with_rates = []
        for savings in savings_products:
            max_rate = 0
            options = SavingsOptions.objects.filter(product=savings)
            if options.exists():
                for option in options:
                    rate = option.intr_rate2 if option.intr_rate2 is not None else option.intr_rate
                    if rate and rate > max_rate:
                        max_rate = rate
                
                savings_with_rates.append({
                    'product': {
                        'fin_prdt_cd': savings.fin_prdt_cd,
                        'kor_co_nm': savings.kor_co_nm,
                        'fin_prdt_nm': savings.fin_prdt_nm,
                        'join_way': savings.join_way,
                        'etc_note': savings.etc_note
                    },
                    'max_rate': max_rate
                })

        # 금리 순으로 정렬
        deposits_with_rates.sort(key=lambda x: x['max_rate'], reverse=True)
        savings_with_rates.sort(key=lambda x: x['max_rate'], reverse=True)

        response_data = {
            'life_cycle': life_cycle,
            'income_level': income_level,
            'asset_based': asset_based,
            'recommended_deposits': deposits_with_rates[:5],
            'recommended_savings': savings_with_rates[:5],
            'investment_suggestion': {
                'monthly_savings': income_level['recommended_amount'] // 12,
                'deposit_ratio': asset_based['investment_ratio']['deposits'],
                'savings_ratio': asset_based['investment_ratio']['savings']
            }
        }

        return Response(response_data)

    except Exception as e:
        import traceback
        print("Error in get_recommendations:", str(e))
        print(traceback.format_exc())
        return Response({
            'error': f'추천 정보 생성 중 오류가 발생했습니다: {str(e)}'
        }, status=500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_personal_finance_status(request):
    """사용자의 재무상태 분석 API"""
    user = request.user
    
    if not all([user.birth, user.annual_income, user.total_assets]):
        return Response({
            'error': '분석을 위해 생년월일, 연소득, 총자산 정보가 필요합니다.'
        }, status=400)
    
    age = calculate_age(user.birth)
    
    # 연령대별 평균 자산과 비교 (예시 데이터)
    age_group_assets = {
        '20대': 5000,
        '30대': 15000,
        '40대': 30000,
        '50대': 50000,
        '60대 이상': 70000
    }
    
    # 연령대 결정
    if age < 30:
        age_group = '20대'
    elif age < 40:
        age_group = '30대'
    elif age < 50:
        age_group = '40대'
    elif age < 60:
        age_group = '50대'
    else:
        age_group = '60대 이상'
    
    # 저축 여력 계산 (예시: 연소득의 30%)
    saving_potential = user.annual_income * 0.3
    
    return Response({
        'age_group': age_group,
        'average_asset_for_age': age_group_assets[age_group],
        'user_asset': user.total_assets,
        'asset_comparison': user.total_assets - age_group_assets[age_group],
        'annual_income': user.annual_income,
        'recommended_monthly_saving': saving_potential / 12,
        'asset_health_score': min(100, (user.total_assets / age_group_assets[age_group]) * 100)
    })