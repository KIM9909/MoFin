from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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
def top_rate(request):
    top_option = DepositOptions.objects.order_by('-intr_rate2').first()

    if not top_option:
        return Response({'error': '데이터가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    product = top_option.product
    options = DepositOptions.objects.filter(product=product)
    product_serializer = DepositProductsSerializer(product)
    options_serializer = DepositOptionsSerializer(options, many=True)

    response_data = {
        'deposit_product': product_serializer.data,
        'options': options_serializer.data,
    }
    
    return Response(response_data)
