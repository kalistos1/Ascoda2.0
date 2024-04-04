from django import forms
from accounts.models import Church, Month, District,Sabbath
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

    payment_method = forms.ChoiceField(
        choices=[('', 'choose Payment Method'),('', 'All'), ('Cash', 'Cash'), ('Bank', 'Bank')],

        required=False,
        widget=forms.Select(attrs={'name':'payment_method','class': 'form-select', 'placeholder': 'Select payment method'})
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


class IncomeExpenseForm(forms.Form):
    month = forms.ModelChoiceField(
        queryset=Month.objects.all(),
        empty_label="Select a month",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select a month'})
    )
    payment_method = forms.ChoiceField(
        choices=[('', 'All'), ('Cash', 'Cash'), ('Bank', 'Bank')],
        required=False,
        widget=forms.Select(attrs={'name':'payment_method','class': 'form-select', 'placeholder': 'Select payment method'})
    )

    def __init__(self, *args, **kwargs):
        super(IncomeExpenseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})



class churchTitheReportForm(forms.Form):
   
    sabbath_week = forms.ModelChoiceField(
        queryset=Sabbath.objects.all(),
        empty_label="Select a Week",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select a week'})
    )

    payment_method = forms.ChoiceField(
        choices=[('', ' Payment Method'),('', 'All'), ('Cash', 'Cash'), ('Bank', 'Bank')],

        required=False,
        widget=forms.Select(attrs={'name':'payment_method','class': 'form-select', 'placeholder': 'Select payment method'})
    )


    def __init__(self, *args, **kwargs):
        super(churchTitheReportForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class AdminChurchTitheReportForm(forms.Form):
    church = forms.ModelChoiceField(
        queryset=Church.objects.all(),
        empty_label="Select a church",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select a church'})
    )
    sabbath_week = forms.ModelChoiceField(
        queryset=Sabbath.objects.all(),
        empty_label="Select a Week",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select a week'})
    )

    payment_method = forms.ChoiceField(
        choices=[('', ' Payment Method'),('', 'All'), ('Cash', 'Cash'), ('Bank', 'Bank')],

        required=False,
        widget=forms.Select(attrs={'name':'payment_method','class': 'form-select', 'placeholder': 'Select payment method'})
    )


    def __init__(self, *args, **kwargs):
        super(AdminChurchTitheReportForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

