from django.db import models

# Create your models here.
class DepositProducts(models.Model):  # 예금상품
    fin_prdt_cd = models.TextField()  # 금융상품 코드
    kor_co_nm = models.TextField()  # 금융회사 명
    fin_prdt_nm = models.TextField()  # 금융 상품명
    etc_note = models.TextField()  # 기타 유의사항
    join_deny = models.IntegerField()  # 가입제한 Ex) 1: 제한없음, 2: 서민전용, 3: 일부제한
    join_member = models.TextField()  # 가입대상
    join_way = models.TextField()  # 가입방법
    spcl_cnd = models.TextField()  # 우대조건


class DepositOptions(models.Model):  # 예금상품 옵션
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)  # 예금상품
    fin_prdt_cd = models.TextField()  # 금융상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)  # 저축 금리 유형명
    intr_rate = models.FloatField(null=True)  # 저축 금리
    intr_rate2 = models.FloatField(null=True)  # 최고 우대금리
    save_trm = models.IntegerField()  # 저축 기간


class SavingsProducts(models.Model):  # 적금상품
    fin_prdt_cd = models.TextField()  # 금융상품 코드
    kor_co_nm = models.TextField()  # 금융회사 명
    fin_prdt_nm = models.TextField()  # 금융 상품명
    etc_note = models.TextField()  # 기타 유의사항
    join_deny = models.IntegerField()  # 가입제한 Ex) 1: 제한없음, 2: 서민전용, 3: 일부제한
    join_member = models.TextField()  # 가입대상
    join_way = models.TextField()  # 가입방법
    spcl_cnd = models.TextField()  # 우대조건


class SavingsOptions(models.Model):  # 적금상품 옵션
    product = models.ForeignKey(SavingsProducts, on_delete=models.CASCADE)  # 적금상품
    fin_prdt_cd = models.TextField()  # 적금상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)  # 저축 금리 유형명
    intr_rate = models.FloatField(null=True)  # 저축 금리
    intr_rate2 = models.FloatField(null=True)  # 최고 우대금리
    save_trm = models.IntegerField()  # 저축 기간
