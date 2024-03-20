from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.

class User(AbstractUser):

    ROLES = (
        ('Admin', 'Admin'),
        ('Church_treasurer', 'Church_treasurer'),
        ('Church_secretary', 'Church_secretary'),
        ('District_secretary', 'District_secretary'),
        ('District_treasurer', 'District_treasurer'),
       
    )
    SEX = (
       ("Male","Male"),
       ("Female","Female")
    )

    raw_password = models.CharField(max_length=200, default="abcd123")
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLES)
    phone = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(null=True, blank=True, upload_to='users')
    sex = models.CharField(max_length=10, choices=SEX, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
  

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.get_fullname()
        #return self.username
        

    def get_fullname(self):
        if self.middle_name is None:
            return self.last_name + " " + self.first_name
        else:
            return self.last_name + " " + self.first_name + ", " + self.middle_name
            
            
# conference model 
class Conference(models.Model):
    name = models.CharField(max_length=300)
    address = models.TextField()
    motto = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="school")
    email = models.CharField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=300, blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    whatsapp = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        db_table = 'conference'
        managed = True
        verbose_name = 'conference'
        verbose_name_plural = 'conference'
        
    def __str__(self):
        return self.name


# district model
class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    district_name = models.CharField(max_length=255)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=300, blank=True, null=True)
    pastor= models.CharField(max_length =50, blank=True, null= True)
    pastors_phone = models.CharField(max_length=15, blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    
    class Meta:
        db_table = 'district'
        verbose_name_plural = 'district'

    def __str__(self):
        return self.district_name


# church model
class Church(models.Model):
    church_id = models.AutoField(primary_key=True)
    church_name = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name ='church_district')
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=300, blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    
    class Meta:
        db_table = 'church'
        verbose_name_plural = 'church'

    def __str__(self):
        return self.church_name

  
   
# church memeber model
class Member(models.Model):

    SEX = ( 
       ("Male","Male"),
       ("Female","Female")
    )
    member_id = models.AutoField(primary_key=True)
    member_name = models.CharField(max_length=255)
    member_email = models.CharField(max_length=300, blank=True, null=True, unique= True)
    member_phone = models.CharField(max_length=300, blank=True, null=True)
    member_Gender = models.CharField(max_length=10, choices=SEX, null=True, blank=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE)
    tithe_card_number= models.IntegerField( default=0, blank=False, null= False, unique= True )
    created_on = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'member'
        verbose_name_plural = 'member'

    def __str__(self):
        return self.member_name

class Year(models.Model):
    year_id = models.AutoField(primary_key=True)
    year = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=False)
    #conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.year)


class Quarter(models.Model):
    TAG = (
        ('1st_Quarter','1st_Quarter'),
        ('2nd_Quarter','2nd_Quarter'),
        ('3rd_Quarter','3rd_Quarter'),
        ('4th_Quarter','4th_Quarter')
    )
    quarter_id = models.AutoField(primary_key=True)
    quarter_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField()
    tag = models.CharField(max_length=20, default='1st_Quarter', choices=TAG, unique =True)
    end_date = models.DateField()
    year = models.ForeignKey(Year, on_delete =models.CASCADE, blank =True, null = True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'quater'
        verbose_name_plural = 'quater'
        managed = True
        ordering = ['-start_date']

    def __str__(self):
        return self.quarter_name



class Month(models.Model):
    month_id = models.AutoField(primary_key=True)
    month_name = models.CharField(max_length=255, blank=True , null =True)
    start_date = models.DateField()
    end_date = models.DateField()
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE,)
    
    class Meta:
        db_table = 'Month'
        verbose_name_plural = 'Month'

    def __str__(self):
        return self.month_name
        

class Sabbath(models.Model):
    sabbath_id = models.AutoField(primary_key=True)
    sabbath_alias = models.CharField(max_length=100, blank=True , null =True)
    sabbath_week_start = models.DateField()  
    sabbath_week_ends = models.DateField()   
    is_active = models.BooleanField(default=False)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sabbath'
        verbose_name_plural = 'sabbath'

    def __str__(self):
        return self.sabbath_alias

    
    
class AssignedOfficer(models.Model):
    church = models.ForeignKey(Church, on_delete=models.CASCADE, blank=True, null=True, related_name="church_account_officer" )
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True, related_name="district_account_officer" )
    officer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_church")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'assigned_officers'
        managed = True
        verbose_name = 'assigned officer'
        verbose_name_plural = 'assigned officer'

    