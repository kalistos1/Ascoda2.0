from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(TitheOffering)
admin.site.register(WeeklyTransaction)
admin.site.register(ChurchIncome)
admin.site.register(ChurchExpense)
admin.site.register(ChurchCashAccount)
admin.site.register(TrustFund)
admin.site.register(CombinedOffering)
admin.site.register(DistrictIncome)
admin.site.register(DistrictExpense)
admin.site.register(BalanceBroughtForward)

