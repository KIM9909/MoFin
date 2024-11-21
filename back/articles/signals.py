# articles/signals.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Article

User = get_user_model()

@receiver(pre_delete, sender=User)
def delete_user_articles(sender, instance, **kwargs):
    # 사용자 삭제 전에 해당 사용자의 게시글 처리
    Article.objects.filter(user=instance).update(user=None)