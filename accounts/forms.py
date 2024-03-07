from django import forms
from .models import * 

class DateInput(forms.DateInput):
    input_type = 'date'

# login form
class LoginForm(forms.Form):    
        
    username = forms.CharField(
                 widget=forms.TextInput(attrs={ 
                                                    'class':'form-control'}))
    password = forms.CharField(
                 widget=forms.PasswordInput(attrs={
                                                   'class':'form-control'}))
                                                   
                                                   
# edit profileform
class EditProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=DateInput)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'sex', 'date_of_birth', 'photo', 'phone', 'address', 'city', 'state', 'email')
       


class AddOfficer(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'sex',  'photo',  'email', 'phone')
    
    def __init__(self, *args, **kwargs):
        super(AddOfficer, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['username'].widget.attrs.update({'class' : 'form-control'})
        self.fields['sex'].widget.attrs.update({'class' : 'form-control'})
        self.fields['photo'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['phone'].widget.attrs.update({'class' : 'form-control'})
     
       
"""
class AddOfficerForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super (AddOfficerForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['teacher'].queryset = User.objects.filter(role="Teacher")
        self.fields['class_group'].label = "Class"

    class Meta:
        model = AssignedOfficer
        fields = '__all__'

"""


class AddAssignedOfficerForm(forms.ModelForm):

    class Meta:
        model = AssignedOfficer
        fields = ('church','district','officer')


    def __init__(self,*args,**kwargs):
        super (AddAssignedOfficerForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['church'].widget.attrs.update({'class' : 'form-control'})
        self.fields['district'].widget.attrs.update({'class' : 'form-control'})
        self.fields['officer'].widget.attrs.update({'class' : 'form-control'})



class AddDistrictForm(forms.ModelForm):
    
    class Meta:
        model = District
        fields = ('district_name','conference','address','email','pastor','pastors_phone', 'facebook')
        
    def __init__(self, *args, **kwargs):
        super(AddDistrictForm, self).__init__(*args, **kwargs)
        self.fields['district_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['conference'].widget.attrs.update({'class' : 'form-control'})
        self.fields['address'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['pastor'].widget.attrs.update({'class' : 'form-control'})
        self.fields['pastors_phone'].widget.attrs.update({'class' : 'form-control'})
        self.fields['facebook'].widget.attrs.update({'class' : 'form-control'})
     
 
 
 
class AddChurchForm(forms.ModelForm):
    
    class Meta:
        model = Church
        fields = ('church_name','district','address','email', 'phone', 'facebook')
        
    def __init__(self, *args, **kwargs):
        super(AddChurchForm, self).__init__(*args, **kwargs)
        self.fields['church_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['district'].widget.attrs.update({'class' : 'form-control'})
        self.fields['address'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['phone'].widget.attrs.update({'class' : 'form-control'})
        self.fields['facebook'].widget.attrs.update({'class' : 'form-control'})
     
 
        
class AddQuarterForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

    class Meta:
        model = Quarter
        fields = ('quarter_name','year', 'start_date', 'tag','end_date', 'conference')  
        
    def __init__(self, *args, **kwargs):
        super(AddQuarterForm, self).__init__(*args, **kwargs)
        self.fields['quarter_name'].widget.attrs.update({'class' : 'form-control', 'placeholder':'title'})
        self.fields['year'].widget.attrs.update({'class' :'form-control'})
        self.fields['start_date'].widget.attrs.update({'class' : 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class' : 'form-control'})
        self.fields['tag'].widget.attrs.update({'class' : 'form-control'})
        self.fields['end_date'].widget.attrs.update({'class' : 'form-control'})
        self.fields['conference'].widget.attrs.update({'class' : 'form-control'})
 
 
class AddMonthForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    
    class Meta:
        model = Month
        fields = ('month_name','start_date','end_date','quarter',)
    def __init__(self, *args, **kwargs):
        super(AddMonthForm, self).__init__(*args, **kwargs)
        self.fields['month_name'].widget.attrs.update({'class' : 'form-control',})
        self.fields['start_date'].widget.attrs.update({'class' : 'form-control'})
        self.fields['end_date'].widget.attrs.update({'class' : 'form-control'})
        self.fields['quarter'].widget.attrs.update({'class' : 'form-control'})
         
 
 
 
class AddSabbathForm(forms.ModelForm):
    sabbath_week_start = forms.DateField(widget=DateInput)
    sabbath_week_ends = forms.DateField(widget=DateInput)
    class Meta:
        model = Sabbath
        fields = ('sabbath_alias','sabbath_week_start','sabbath_week_ends', 'month','is_active')
        
    def __init__(self, *args, **kwargs):
        super(AddSabbathForm, self).__init__(*args, **kwargs)
        self.fields['sabbath_alias'].widget.attrs.update({'class' : 'form-control',})
        self.fields['sabbath_week_start'].widget.attrs.update({'class' : 'form-control'})
        self.fields['sabbath_week_ends'].widget.attrs.update({'class' : 'form-control'})
        self.fields['month'].widget.attrs.update({'class' : 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class' : 'form-control'})
        
         

 
class AddMemberForm(forms.ModelForm):
   
    class Meta:
        model = Member
        fields = ('member_name','member_email', 'member_phone','member_Gender','tithe_card_number','church')
        
    def __init__(self, *args, **kwargs):
        super(AddMemberForm, self).__init__(*args, **kwargs)
        self.fields['member_name'].widget.attrs.update({'class' : 'form-control',})
        self.fields['member_email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['member_phone'].widget.attrs.update({'class' : 'form-control'})
        self.fields['member_Gender'].widget.attrs.update({'class' : 'form-control'})
        self.fields['tithe_card_number'].widget.attrs.update({'class' : 'form-control'})
        self.fields['church'].widget.attrs.update({'class' : 'form-control'})
         
                      