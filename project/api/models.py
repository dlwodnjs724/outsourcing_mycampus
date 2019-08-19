import arrow
from django.db import models

# Create your models here.

class Token(models.Model):
    token = models.CharField(max_length=10)
    target_email = models.EmailField(unique=True)

    is_used = models.BooleanField(default=False) # 회원가입이 완료된 계정의 토큰
    is_accepted = models.BooleanField(default=False) # 토큰 인증을 받은 상태인지 확인

    created_at = models.IntegerField()

    @property
    def is_expired(self):
        now = arrow.now().timestamp
        if (now - self.created_at) > 5 * 60:
            return True
        else:
            return False