import datetime
from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import Menu


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ('season', 'year', 'items', 'expiration_date')
        widgets = {
            'expiration_date': SelectDateWidget(years=range(2000, 2050)),
            'items': forms.CheckboxSelectMultiple
        }

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date < datetime.date(2000, 1, 1):
            raise forms.ValidationError(
                "Expiration date cannot be before year 2000"
            )
        return expiration_date

    def clean(self):
        cleaned_data = super(MenuForm, self).clean()
        season = cleaned_data.get('season')
        year = cleaned_data.get('year')
        existing_menu = Menu.objects.filter(season=season, year=year)
        if existing_menu and existing_menu[0].pk != self.instance.pk:
            raise forms.ValidationError(
                'Menu for this season already exists!'
            )
