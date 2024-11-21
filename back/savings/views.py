from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import SavingsProducts, SavingsOptions
from .serializers import SavingsProductsSerializer, SavingsOptionsSerializer
from .models import DepositProducts, DepositOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
import requests


@api_view(['GET'])
def save_deposit_products(request):
    api_key = settings.API_KEY
    url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    params = {
        'auth': api_key,
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }
    response = requests.get(url, params=params).json()

    for data in response.get('result').get('baseList'):
        fin_prdt_cd = data.get('fin_prdt_cd')
        kor_co_nm = data.get('kor_co_nm')
        fin_prdt_nm = data.get('fin_prdt_nm')
        etc_note = data.get('etc_note')
        join_deny = data.get('join_deny')
        join_member = data.get('join_member')
        join_way = data.get('join_way')
        spcl_cnd = data.get('spcl_cnd')

        save_data = {
            'fin_prdt_cd': fin_prdt_cd,
            'kor_co_nm': kor_co_nm,
            'fin_prdt_nm': fin_prdt_nm,
            'etc_note': etc_note,
            'join_deny': join_deny,
            'join_member': join_member,
            'join_way': join_way,
            'spcl_cnd': spcl_cnd,
        }
            
        if DepositProducts.objects.filter(
            fin_prdt_cd=fin_prdt_cd, kor_co_nm=kor_co_nm, fin_prdt_nm=fin_prdt_nm, 
            etc_note=etc_note, join_deny=join_deny, join_member=join_member, 
            join_way=join_way, spcl_cnd=spcl_cnd
        ).exists():
            continue

        serializer = DepositProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    options = response.get('result').get('optionList')

    for option in options:
        intr_rate_type_nm = option.get('intr_rate_type_nm')
        intr_rate = option.get('intr_rate')
        intr_rate2 = option.get('intr_rate2')
        save_trm = option.get('save_trm')
        fin_prdt_cd = option.get('fin_prdt_cd')

        if DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd):
            product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            save_data = {
                'intr_rate_type_nm': intr_rate_type_nm,
                'intr_rate': intr_rate,
                'intr_rate2': intr_rate2,
                'save_trm': save_trm,
                'fin_prdt_cd': fin_prdt_cd,
            }

            if DepositOptions.objects.filter(
                intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, 
                intr_rate2=intr_rate2, save_trm=save_trm
            ).exists():
                continue

            serializer = DepositOptionsSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(product=product)


    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        deposit_products_list = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(deposit_products_list, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'message': '이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    product = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(product, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def deposit_product_details(request, fin_prdt_cd):
    """
    특정 상품에 대한 상세정보와 옵션 리스트를 반환합니다.
    """
    try:
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    except DepositProducts.DoesNotExist:
        return Response({'error': '상품이 존재하지 않습니다.'}, status=404)
    
    product_serializer = DepositProductsSerializer(product)
    options = DepositOptions.objects.filter(product=product)
    options_serializer = DepositOptionsSerializer(options, many=True)

    response_data = {
        'product': product_serializer.data,
        'options': options_serializer.data,
    }

    return Response(response_data)


@api_view(['GET'])
def save_savings_products(request):
    api_key = settings.API_KEY
    url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
    params = {
        'auth': api_key,
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }
    response = requests.get(url, params=params).json()

    for data in response.get('result').get('baseList'):
        fin_prdt_cd = data.get('fin_prdt_cd')
        kor_co_nm = data.get('kor_co_nm')
        fin_prdt_nm = data.get('fin_prdt_nm')
        etc_note = data.get('etc_note')
        join_deny = data.get('join_deny')
        join_member = data.get('join_member')
        join_way = data.get('join_way')
        spcl_cnd = data.get('spcl_cnd')

        save_data = {
            'fin_prdt_cd': fin_prdt_cd,
            'kor_co_nm': kor_co_nm,
            'fin_prdt_nm': fin_prdt_nm,
            'etc_note': etc_note,
            'join_deny': join_deny,
            'join_member': join_member,
            'join_way': join_way,
            'spcl_cnd': spcl_cnd,
        }

        if SavingsProducts.objects.filter(
            fin_prdt_cd=fin_prdt_cd, kor_co_nm=kor_co_nm, fin_prdt_nm=fin_prdt_nm, 
            etc_note=etc_note, join_deny=join_deny, join_member=join_member, 
            join_way=join_way, spcl_cnd=spcl_cnd
        ).exists():
            continue

        serializer = SavingsProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    options = response.get('result').get('optionList')

    for option in options:
        intr_rate_type_nm = option.get('intr_rate_type_nm')
        intr_rate = option.get('intr_rate')
        intr_rate2 = option.get('intr_rate2')
        save_trm = option.get('save_trm')
        fin_prdt_cd = option.get('fin_prdt_cd')

        if SavingsProducts.objects.get(fin_prdt_cd=fin_prdt_cd):
            product = SavingsProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            save_data = {
                'intr_rate_type_nm': intr_rate_type_nm,
                'intr_rate': intr_rate,
                'intr_rate2': intr_rate2,
                'save_trm': save_trm,
                'fin_prdt_cd': fin_prdt_cd,
            }

            if SavingsOptions.objects.filter(
                intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, 
                intr_rate2=intr_rate2, save_trm=save_trm
            ).exists():
                continue

            serializer = SavingsOptionsSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(product=product)


    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def savings_products(request):
    if request.method == 'GET':
        deposit_products_list = SavingsProducts.objects.all()
        serializer = SavingsProductsSerializer(deposit_products_list, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = SavingsProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'message': '이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def savings_product_options(request, fin_prdt_cd):
    product = SavingsOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = SavingsOptionsSerializer(product, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def savings_product_details(request, fin_prdt_cd):
    """
    특정 상품에 대한 상세정보와 옵션 리스트를 반환합니다.
    """
    try:
        product = SavingsProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    except SavingsProducts.DoesNotExist:
        return Response({'error': '상품이 존재하지 않습니다.'}, status=404)
    
    product_serializer = SavingsProductsSerializer(product)
    options = SavingsOptions.objects.filter(product=product)
    options_serializer = SavingsOptionsSerializer(options, many=True)

    response_data = {
        'product': product_serializer.data,
        'options': options_serializer.data,
    }

    return Response(response_data)


@api_view(['POST'])
def toggle_subscription(request, product_type, fin_prdt_cd):
    if not request.user.is_authenticated:
        return Response({'error': '로그인이 필요합니다.'}, status=401)
    
    try:
        if product_type == 'deposit':
            product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            if request.user.subscribe_deposits.filter(fin_prdt_cd=fin_prdt_cd).exists():
                request.user.subscribe_deposits.remove(product)
                message = '구독이 취소되었습니다.'
            else:
                request.user.subscribe_deposits.add(product)
                message = '구독이 완료되었습니다.'
        elif product_type == 'savings':
            product = SavingsProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            if request.user.subscribe_savings.filter(fin_prdt_cd=fin_prdt_cd).exists():
                request.user.subscribe_savings.remove(product)
                message = '구독이 취소되었습니다.'
            else:
                request.user.subscribe_savings.add(product)
                message = '구독이 완료되었습니다.'
        else:
            return Response({'error': '잘못된 상품 타입입니다.'}, status=400)
        
        return Response({'message': message}, status=200)
    except (DepositProducts.DoesNotExist, SavingsProducts.DoesNotExist):
        return Response({'error': '상품을 찾을 수 없습니다.'}, status=404)

@api_view(['GET'])
def get_subscriptions(request):
    if not request.user.is_authenticated:
        return Response({'error': '로그인이 필요합니다.'}, status=401)
    
    deposits = DepositProductsSerializer(request.user.subscribe_deposits.all(), many=True).data
    savings = SavingsProductsSerializer(request.user.subscribe_savings.all(), many=True).data
    
    return Response({
        'deposits': deposits,
        'savings': savings
    })