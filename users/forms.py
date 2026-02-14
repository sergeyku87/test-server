from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget_type = field.widget.__class__.__name__.lower()

            if 'checkbox' in widget_type or 'radio' in widget_type:
                css_class = 'form-check-input'
            elif 'select' in widget_type:
                css_class = 'form-select'
            elif 'textarea' in widget_type:
                css_class = 'form-control'
            else:
                css_class = 'form-control'

            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css_class} {existing_classes}".strip()

            if not field.widget.attrs.get('placeholder'):
                field.widget.attrs['placeholder'] = field.label

            if not "checkbox" in widget_type:
                field.label = ""
            field.help_text = None


class CustomAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Никнейм"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
    )


class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "first_name",
            "last_name",
            "father_name",
        ]


