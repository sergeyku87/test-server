from django import forms

from events.models import TimeEvent


class TimeEventForm(forms.ModelForm):
    class Meta:
        model = TimeEvent
        fields = "__all__"


class EventForm(forms.Form):
    action = forms.ChoiceField(
        choices=[
            ('clock_in', 'Приход'),
            ('clock_out', 'Уход'),
        ],
        widget=forms.HiddenInput(),
        required=True,
    )


# class ClockForm(forms.Form):
#     action = forms.ChoiceField(
#         choices=[
#             ('clock_in', 'Clock In'),
#             ('clock_out', 'Clock Out'),
#         ],
#         widget=forms.HiddenInput(),  # Поле скрыто, значение передаётся через кнопки
#         required=True
#     )
