from django.db import models


class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.first_name} {self.second_name} {self.father_name}"
