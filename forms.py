# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _


class DateRangeForm(forms.Form):       
    """
    RUS: Форма для фильтрации по дате
    """ 
    range_gte = forms.DateField(
                    label=_("From date"),
                    widget=forms.DateInput(
                        attrs={
                            "type": "date",
                            "format": "%d-%m-%Y"
                            }
                        ),
                    localize=True,
                    required=False,
                )
    range_lte = forms.DateField(
                    label=_("To date"),
                    widget=forms.DateInput(
                        attrs={
                            "type": "date",
                            "format": "%d-%m-%Y"
                            }
                        ),
                    localize=True,
                    required=False,
                )
    def __init__(self, *args, **kwargs):
        # """
        # RUS: Конструктор класса
        # """
        # self.range_gte.initial = default_gte
        # self.range_lte.initial = default_lte
        super(DateRangeForm, self).__init__(*args, **kwargs)
    
    def is_valid(self) -> bool:        
        return super().is_valid()
    
    # def clean(self):
    #     return super().clean()
    
    # def clean_range_gte(self):
    #     data = self.cleaned_data['range_gte']
    #     #Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
    #     # if data < datetime.date.today():
    #     #     raise ValidationError(_('Invalid date - renewal in past'))
    #     #Проверка того, то дата не выходит за "верхнюю" границу (+4 недели).
    #     # if data > datetime.date.today() + datetime.timedelta(weeks=4):
    #     #     raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
    #     # Помните, что всегда надо возвращать "очищенные" данные.
    #     return data
    
    # def clean_range_lte(self):
    #     data = self.cleaned_data['range_lte']
    #     return data
        