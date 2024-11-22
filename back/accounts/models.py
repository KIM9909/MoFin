from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from django.db import models
from savings.models import SavingsProducts, DepositProducts


def user_profile_path(instance, filename):
    # 파일명이 중복되지 않도록 처리하면서, 사용자별로 폴더 구분
    ext = filename.split('.')[-1]  # 확장자 추출
    filename = f'{instance.username}_profile.{ext}'
    return f'profile_images/{instance.username}/{filename}'


class User(AbstractUser):
    nickname = models.CharField(max_length=255, blank=False)
    birth = models.DateField(blank=True, null=True)
    preference = models.TextField(blank=True, null=True)
    subscribe_deposits = models.ManyToManyField(DepositProducts, blank=True)
    subscribe_savings = models.ManyToManyField(SavingsProducts, blank=True)
    annual_income = models.BigIntegerField(blank=True, null=True, help_text="연 소득(만원)")
    total_assets = models.BigIntegerField(blank=True, null=True, help_text="총 자산(만원)")
    profile_img = models.ImageField(
        upload_to=user_profile_path,
        default=None, 
        blank=True, 
        null=True,
        verbose_name='프로필 이미지'
    )

    def __str__(self):
        return self.username


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        data = form.cleaned_data
        user.nickname = data.get('nickname')
        user.birth = data.get('birth')
        user.preference = data.get('preference')
        user.annual_income = data.get('annual_income')
        user.total_assets = data.get('total_assets')
        user.profile_img = data.get('profile_img')
        
        if commit:
            user.save()
        return user
    
