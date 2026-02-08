from django import forms

from tg_users.models import TelegramUser


class TelegramUserForm(forms.ModelForm):
    class Meta:
        model = TelegramUser
        fields = "chat_id", "first_name", "second_name", "father_name"

