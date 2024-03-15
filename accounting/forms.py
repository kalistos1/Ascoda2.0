from django import forms
from .models import * 

class DateInput(forms.DateInput):
    input_type = 'date'
    
class TitheOfferingForm(forms.ModelForm):
    class Meta:
        model = TitheOffering
        fields = ('tithe', 'offering', 'project','payment_method')
        
    def __init__(self, *args, **kwargs):
        super(TitheOfferingForm, self).__init__(*args, **kwargs)
       
        self.fields['tithe'].widget.attrs.update({'class': 'form-control', 'placeholder':'Tithe'})
        self.fields['offering'].widget.attrs.update({'class': 'form-control','placeholder':'Offering'})
        self.fields['project'].widget.attrs.update({'class': 'form-control','placeholder':'Project'})
        self.fields['payment_method'].widget.attrs.update({'class': 'form-control','placeholder':''})
        

class WeeklyTransactionForm(forms.ModelForm):
    class Meta:
        model = WeeklyTransaction
        fields = ('sabbath_week', 'church', 'tithe_sum', 'offering_sum', )
        
    def __init__(self, *args, **kwargs):
        super(WeeklyTransactionForm, self).__init__(*args, **kwargs)
        self.fields['sabbath_week'].widget.attrs.update({'class': 'form-control'})
        self.fields['church'].widget.attrs.update({'class': 'form-control'})
        self.fields['tithe_sum'].widget.attrs.update({'class': 'form-control'})
        self.fields['offering_sum'].widget.attrs.update({'class': 'form-control'})
        

class ChurchIncomeForm(forms.ModelForm):
    class Meta:
        model = ChurchIncome
        fields = ('income_type','amount', 'payment_method', 'comment')
        
    def __init__(self, *args, **kwargs):
        super(ChurchIncomeForm, self).__init__(*args, **kwargs)

        self.fields['income_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})  
        self.fields['payment_method'].widget.attrs.update({'class': 'form-control'})


class ChurchExpenseForm(forms.ModelForm):
    expense_date = forms.DateField(widget=DateInput)
    class Meta:
        model = ChurchExpense
        fields = ( 'title', 'comment', 'amount','expense_date')
        
    def __init__(self, *args, **kwargs):
        super(ChurchExpenseForm, self).__init__(*args, **kwargs)        

        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['expense_date'].widget.attrs.update({'class': 'form-control'})
       

class ChurchCashAccountForm(forms.ModelForm):
    class Meta:
        model = ChurchCashAccount
        fields = ('cash_generated', 'cash_spent', 'cash_to_bank' )
        
    def __init__(self, *args, **kwargs):
        super(ChurchCashAccountForm, self).__init__(*args, **kwargs)
        self.fields['cash_generated'].widget.attrs.update({'class': 'form-control'})
        self.fields['cash_spent'].widget.attrs.update({'class': 'form-control'})
        self.fields['cash_to_bank'].widget.attrs.update({'class': 'form-control'})
      
       

class TrustFundForm(forms.ModelForm):
    class Meta:
        model = TrustFund
        fields = ( 'tithe_amount', 'offering_amount', 'total_amount', 'sabbath_week')
        
    def __init__(self, *args, **kwargs):
        super(TrustFundForm, self).__init__(*args, **kwargs)
       
        self.fields['tithe_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['offering_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['total_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['sabbath_week'].widget.attrs.update({'class': 'form-control'})
        
        
        
class DistrictIncomeForm(forms.ModelForm):
    class Meta:
        model = DistrictIncome
        fields = ('income_type','amount', 'payment_method', 'description')
        
    def __init__(self, *args, **kwargs):
        super(DistrictIncomeForm, self).__init__(*args, **kwargs)

        self.fields['income_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})  
        self.fields['payment_method'].widget.attrs.update({'class': 'form-control'})


class DistrictExpenseForm(forms.ModelForm):
    expense_date = forms.DateField(widget=DateInput)
    class Meta:
        model = DistrictExpense
        fields = ( 'title', 'comment', 'amount','expense_date')
        
    def __init__(self, *args, **kwargs):
        super(DistrictExpenseForm, self).__init__(*args, **kwargs)        

        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['expense_date'].widget.attrs.update({'class': 'form-control'})
       

class UploadTitheOfferingForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File')


class UploadMembersForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File')