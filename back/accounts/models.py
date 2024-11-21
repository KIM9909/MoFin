from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from django.db import models
from savings.models import SavingsProducts, DepositProducts

class User(AbstractUser):
    nickname = models.CharField(max_length=255, blank=False)
    birth = models.DateField(blank=True, null=True)
    preference = models.TextField(blank=True, null=True)
    subscribe_deposits = models.ManyToManyField(DepositProducts, blank=True)
    subscribe_savings = models.ManyToManyField(SavingsProducts, blank=True)

    def __str__(self):
        return self.username


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        data = form.cleaned_data
        user.nickname = data.get('nickname')
        user.birth = data.get('birth')
        user.preference = data.get('preference')
        
        if commit:
            user.save()
        return user