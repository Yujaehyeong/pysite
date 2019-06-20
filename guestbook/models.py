from django.db import models

# Create your models here.
class Guestbook(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=32)
    contents = models.CharField(max_length=1000)
    regdate =models.DateTimeField(auto_now=True) # 시간까지 나오는 타입


    def __str__(self):
        return f'Guestbook({self.name}, {self.password},{self.contents}, {self.regdate})'