from datetime import date
from typing import Dict, Any

def calculate_age(birth_date: date) -> int:
    """생년월일로부터 나이 계산"""
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def get_life_cycle_recommendation(age: int) -> Dict[str, Any]:
    """연령대별 생애주기 추천 로직"""
    if age < 30:
        return {
            'cycle': '청년기',
            'description': '자산 형성 초기 단계로, 유동성과 안정성을 동시에 고려해야 합니다.',
            'deposit_priority': ['높은 금리', '낮은 예치금액'],
            'savings_priority': ['자유입출금', '단기저축']
        }
    elif age < 40:
        return {
            'cycle': '사회초년기',
            'description': '소득이 발생하기 시작하는 시기로, 저축습관 형성이 중요합니다.',
            'deposit_priority': ['중금리', '중기예치'],
            'savings_priority': ['정기적금', '고금리']
        }
    elif age < 50:
        return {
            'cycle': '자산형성기',
            'description': '자산을 적극적으로 늘려나가야 하는 시기입니다.',
            'deposit_priority': ['고금리', '장기예치'],
            'savings_priority': ['고금리', '장기저축']
        }
    elif age < 65:
        return {
            'cycle': '자산안정기',
            'description': '안정적인 자산 운용이 필요한 시기입니다.',
            'deposit_priority': ['안정성', '중장기예치'],
            'savings_priority': ['원금보장', '이자수익']
        }
    else:
        return {
            'cycle': '노년기',
            'description': '안전한 자산 관리가 최우선인 시기입니다.',
            'deposit_priority': ['안정성', '단기예치'],
            'savings_priority': ['원금보장', '수시입출금']
        }

def get_income_level_recommendation(annual_income: int) -> Dict[str, Any]:
    """소득 수준별 추천 로직"""
    if annual_income >= 80000:  # 8천만원 이상
        return {
            'level': '고소득층',
            'description': '적극적인 자산 운용이 가능한 소득 수준입니다.',
            'recommended_amount': annual_income * 0.4,  # 연소득의 40%
            'deposit_priority': ['고액예치', 'VIP혜택'],
            'savings_priority': ['고금리', '장기저축']
        }
    elif annual_income >= 30000:  # 3천만원 이상
        return {
            'level': '중위소득층',
            'description': '안정적인 저축과 투자가 가능한 소득 수준입니다.',
            'recommended_amount': annual_income * 0.3,  # 연소득의 30%
            'deposit_priority': ['중금리', '혜택형'],
            'savings_priority': ['정기적금', '목돈마련']
        }
    else:
        return {
            'level': '서민층',
            'description': '안정적인 저축 습관 형성이 중요한 시기입니다.',
            'recommended_amount': annual_income * 0.2,  # 연소득의 20%
            'deposit_priority': ['낮은예치금액', '서민우대'],
            'savings_priority': ['비과세혜택', '소액적립']
        }

def get_asset_based_recommendation(total_assets: int) -> Dict[str, Any]:
    """자산 규모별 추천 로직"""
    if total_assets >= 100000:  # 10억 이상
        return {
            'level': '고자산층',
            'description': 'VIP 전용 상품과 프리미엄 서비스를 활용하세요.',
            'investment_ratio': {
                'deposits': 0.4,
                'savings': 0.6
            },
            'deposit_priority': ['프리미엄', 'VIP상품'],
            'savings_priority': ['고액예치', '특별우대']
        }
    elif total_assets >= 30000:  # 3억 이상
        return {
            'level': '중자산층',
            'description': '안정성과 수익성의 균형을 맞추어 자산을 운용하세요.',
            'investment_ratio': {
                'deposits': 0.5,
                'savings': 0.5
            },
            'deposit_priority': ['우대금리', '중장기'],
            'savings_priority': ['고금리', '장기저축']
        }
    else:
        return {
            'level': '일반층',
            'description': '안정적인 자산 증식을 위해 정기적인 저축을 유지하세요.',
            'investment_ratio': {
                'deposits': 0.6,
                'savings': 0.4
            },
            'deposit_priority': ['안정성', '유동성'],
            'savings_priority': ['소액저축', '단기저축']
        }