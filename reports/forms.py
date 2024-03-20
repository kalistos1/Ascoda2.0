from django import forms
from accounts.models import Church, Month, District
from accounting.models import TrustFund

class IncomeExpenseReportForm(forms.Form):
    church = forms.ModelChoiceField(
        queryset=Church.objects.all(),
        empty_label="Select a church",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select a church'})
    )
    month = forms.ModelChoiceField(
        queryset=Month.objects.all(),
        empty_label="Select a month",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select a month'})
    )

    def __init__(self, *args, **kwargs):
        super(IncomeExpenseReportForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class DistrictTrustfundForm(forms.Form):
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        empty_label="Select a district",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select a church'})
    )
    month = forms.ModelChoiceField(
        queryset=Month.objects.all(),
        empty_label="Select a month",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select a month'})
    )

    def __init__(self, *args, **kwargs):
        super(DistrictTrustfundForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class MonthForm (forms.Form):
    month = forms.ModelChoiceField(
        queryset=Month.objects.all(),
        empty_label="Select a month",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select a month'})
    )

    def __init__(self, *args, **kwargs):
        super(MonthForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


