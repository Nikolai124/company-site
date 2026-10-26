import re

from django import forms

from .models import Lead, Service


class LeadForm(forms.ModelForm):
    # Поле-ловушка для спам-ботов: человек его не видит
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}))

    class Meta:
        model = Lead
        fields = ["name", "phone", "service", "comment"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Как к вам обращаться", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"placeholder": "+7 (___) ___-__-__", "type": "tel", "autocomplete": "tel"}),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Площадь, адрес, удобное время"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = Service.objects.filter(is_active=True)
        self.fields["service"].empty_label = "Пока не знаю, нужна консультация"
        self.fields["comment"].required = False

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Имя слишком короткое")
        return name

    def clean_phone(self):
        digits = re.sub(r"\D", "", self.cleaned_data["phone"])
        if len(digits) == 11 and digits[0] in "78":
            digits = "7" + digits[1:]
        elif len(digits) == 10:
            digits = "7" + digits
        else:
            raise forms.ValidationError("Введите номер в формате +7 900 123-45-67")
        return f"+{digits}"

    def is_spam(self) -> bool:
        return bool(self.cleaned_data.get("website"))
