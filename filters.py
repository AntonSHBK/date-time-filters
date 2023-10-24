# -*- coding: utf-8 -*-

import datetime
from typing import Any
from collections import OrderedDict

from django import forms
from django.contrib.admin import FieldListFilter
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

DATA_RANGE_FILTER_TEMPLATE = '/date_time_filters/date_filter.htm'


class DateRangeFilter(FieldListFilter):
    """
        Фильтр по дате (DateTimeField)
    """
    
    def __init__(self, field, request, params, model, model_admin, field_path,
                 default_from_date=None, default_to_date=None):      
        self.from_date = "{0}_from_date".format(field_path)
        self.to_date = "{0}_to_date".format(field_path) 
        
        self.default_from_date = default_from_date
        self.default_to_date = default_to_date
        
        super(DateRangeFilter, self).__init__(field, request, params, model, model_admin, field_path)    
        
        self.template = self._get_template()

        self.request = request
        self.model_admin = model_admin
        self.form = self.get_form(request)
    
    def _get_template(self): 
        return DATA_RANGE_FILTER_TEMPLATE
    
    def has_output(self) -> bool:    
        return True
    
    def expected_parameters(self):
        return [self.from_date, self.to_date]
    
    def choices(self, changelist: Any):
        """
        RUS: Кодировка значенией в UTF-8
        """
        yield {
            "fild_name": str(self.title),
        }

    def _get_form_fields(self):
        """
        RUS: Установить поля формы ввода
        """
        return OrderedDict(
            (
                (
                    self.from_date,
                    forms.DateField(
                        label=_("С"),
                        widget=forms.DateInput(
                            attrs={
                                "type": "date",
                                }
                            ),
                        localize=True,
                        required=False,
                        initial=self.default_from_date
                    ),
                ),
                (
                    self.to_date,
                    forms.DateField(
                        label=_("По"),
                        widget=forms.DateInput(
                            attrs={
                                "type": "date",
                                }
                            ),
                        localize=True,
                        required=False,
                        initial=self.default_to_date
                    ),
                ),
            )
        )
        
    def _get_form_class(self):
        """
        RUS: Установить метакласс формы
        """
        fields = self._get_form_fields()
        form_class = type(
            str("DateRangeForm"), 
            (forms.BaseForm,), 
            {"base_fields": fields}
            )
        return form_class

    def get_form(self, request):
        """
        RUS: Получить объект формы
        """        
        form_class = self._get_form_class()
        return form_class(request.GET or None)
    
    def get_timezone(self, _request):
        return timezone.get_default_timezone()
        
    def _make_query_filter(self, request, validated_data):
        """
        RUS: Возвращает параметры для фильтрации
        """
        query_params = {}
        date_value_gte = validated_data.get(self.from_date, None)
        date_value_lte = validated_data.get(self.to_date, None)
        if date_value_gte:
            query_params["{0}__gte".format(self.field_path)] = datetime.datetime.combine(date_value_gte, datetime.time.min)
        if date_value_lte:
            query_params["{0}__lte".format(self.field_path)] = datetime.datetime.combine(date_value_lte, datetime.time.max)
        return query_params
    
    def  queryset(self, request, queryset):
        """
        RUS: Возвращает отфильтрованный объект запроса 
        на основе извлеченного значения из строки запроса
        """
        if self.form.is_valid():
            validated_data = dict(self.form.cleaned_data.items())
            if validated_data:
                return queryset.filter(**self._make_query_filter(request, validated_data))
        return queryset