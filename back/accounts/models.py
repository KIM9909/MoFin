from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from django.db import models
from savings.models import SavingsProducts

class User(AbstractUser):
    nickname = models.CharField(max_length=255, blank=False)
    birth = models.DateField(blank=True, null=True)
    preference = models.TextField(blank=True, null=True)
    joined_products = models.ManyToManyField(SavingsProducts, blank=True, null=True, related_name='users_joined')

    def __str__(self):
        return self.username


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field, user_username
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        nickname = data.get("nickname")
        birth = data.get("birth")
        preference = data.get("preference")
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if nickname:
            user_field(user, "nickname", nickname)
        if birth:
            user_field(user, "birth", birth)
        if preference:
            user_field(user, "preference", preference)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()

        self.populate_username(request, user)

        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()

        return user