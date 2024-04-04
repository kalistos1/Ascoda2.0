from django.db import models
from django.db.models import Sum
from accounts.models import Member, Sabbath, Church, District
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

class TitheOffering(models.Model):
    METHOD = (
        ('Cash', 'Cash'),
        ('Bank', 'Bank'),
    )
    donation_id = models.AutoField(primary_key=True)
    sabbath_week = models.ForeignKey(Sabbath, on_delete=models.CASCADE, default=1)
    tithe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    offering = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    project = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField(max_length=10, choices=METHOD)
    church_member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="tithe_offerings")
    date_added = models.DateField(auto_now=True)
    last_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.church_member.member_name

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.calculate_combined_offering()

    # def calculate_combined_offering(self):
    #     # Fetch the associated church and active week
    #     associated_church = self.church_member.church
    #     active_week = self.sabbath_week

    #     # Calculate combined offering
    #     combined_offering_entry, created = CombinedOffering.calculate_combined_offering(
    #         church_income_entries=[self],
    #         church=associated_church
    #     )

    #     # Update other models or perform additional actions as needed
    #     # For example, you can update the TotalToConference model here

    #     return combined_offering_entry


class WeeklyTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    sabbath_week = models.ForeignKey(Sabbath, on_delete=models.CASCADE)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, default="1")
    tithe_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    offering_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    project_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_added = models.DateField(auto_now=True)

    def __str__(self):
        return f"Weekly Transaction {self.transaction_id} - {self.sabbath_week.sabbath_alias} - {self.church.church_name}"


class ChurchIncome(models.Model):
    METHOD = (
        ('Others', 'Others'),
        ('Cash', 'Cash'),
        ('Bank', 'Bank'),
    )

    INCOME = (
        ('APPRECIATION', 'APPRECIATION'),
        ('DONATION', 'DONATION'),
        ('CHILD_DEDICATION', 'CHILD_DEDICATION'),
        ('THANKS_OFFERING', 'THANKS_OFFERING'),
        ('VOW', 'VOW'),
        ('SABBATH_SCHOOL_EXPENSE_OFFERING', 'SABBATH_SCHOOL_EXPENSE_OFFERING'),
        ('SABBATH_SCHOOL_OFFERING', 'SABBATH_SCHOOL_OFFERING'),
        ('LOOSE_OFFERING', 'LOOSE_OFFERING'),
        ('ENVELOPE_OFFERING', 'LOOSE_ENVELOPE'),
        ('13TH_SABBATH', '13TH_SABBATH'),
        ('HARVEST', 'HARVEST'),
        ('CAMP_MEETING', 'CAMP_MEETING'),
        ('AMO', 'AMO'),
        ('AWM', 'AWM'),
        ('YOUTH', 'YOUTH'),
        ('OTHERS', 'OTHERS'),
        ("T_O_P", 'T_O_P'),
    )

    income_id = models.AutoField(primary_key=True)
    sabbath = models.ForeignKey(Sabbath, on_delete=models.CASCADE)
    church = models.ForeignKey(Church, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, blank=True, null=True)
    income_type = models.CharField(max_length=40, choices=INCOME)
    payment_method = models.CharField(max_length=10, choices=METHOD)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Church income - {self.sabbath.sabbath_alias}"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.calculate_combined_offering()

    # def calculate_combined_offering(self):
    #     # Fetch the associated church and active week
    #     associated_church = self.church
    #     active_week = self.sabbath

    #     # Calculate combined offering
    #     combined_offering_entry, created = CombinedOffering.calculate_combined_offering(
    #         church_income_entries=[self],
    #         church=associated_church
    #     )

    #     # Update other models or perform additional actions as needed

    #     return combined_offering_entry


class CombinedOffering(models.Model):
    associated_church = models.ForeignKey(Church, on_delete=models.CASCADE)
    combined_offering = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_due_district = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_due_church = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_due_conference = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_available_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sabbath_week = models.ForeignKey(Sabbath, on_delete=models.CASCADE)
    date_calculated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Combined Offering for {self.associated_church.church_name} - {self.sabbath_week.sabbath_alias}"
   

  
class ChurchExpense(models.Model):

    expense_id = models.AutoField(primary_key=True)
    sabbath = models.ForeignKey(Sabbath, on_delete=models.CASCADE)
    church = models.ForeignKey(Church, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    comment = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str("Expense =" + "" + self.title + " " + self.comment)


class ChurchCashAccount(models.Model):
    cash_id = models.AutoField(primary_key=True)
    cash_generated = models.DecimalField(max_digits=10, decimal_places=2)
    cash_spent = models.DecimalField(max_digits=10, decimal_places=2)
    cash_to_bank = models.DecimalField(max_digits=10, decimal_places=2)
    cash_at_hand = models.DecimalField(max_digits=10, decimal_places=2)
    sabbath_week = models.ForeignKey(Sabbath, on_delete=models.CASCADE)
    church = models.ForeignKey(Church, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'cash spent'
    
    def save(self, *args, **kwargs):
        # Calculate cash_at_hand before saving
        self.cash_at_hand = (self.cash_generated) - (self.cash_spent + self. cash_to_bank)
        super(ChurchCashAccount, self).save(*args, **kwargs)


class BalanceBroughtForward(models.Model):
    balance_id = models.AutoField(primary_key=True)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sabbath_week = models.ForeignKey(Sabbath, on_delete=models.CASCADE)
    church = models.ForeignKey(Church, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        # Add an ordering to ensure consistency in queries
        ordering = ['sabbath_week', 'church']

    def __str__(self):
        return f"Balance Brought Forward - {self.sabbath_week.sabbath_alias} - {self.church.church_name}"
    
    @classmethod
    def create_balance_entry(cls, church, sabbath_week):
        active_quarter_info = sabbath_week.month.quarter  # Adjust this based on your model structure


        church_expenses = ChurchExpense.objects.filter(church=church, sabbath=sabbath_week, sabbath__month__quarter=active_quarter_info)
        church_incomes = ChurchIncome.objects.filter(church=church, sabbath=sabbath_week, sabbath__month__quarter=active_quarter_info)

        # Calculate total income excluding specific income_types
        excluded_income_types = ['APPRECIATION', 'LOOSE_OFFERING', 'CHILD_DEDICATION', 'THANKS_OFFERING', 'SABBATH_SCHOOL_EXPENSE_OFFERING','ENVELOPE_OFFERING']
        total_week_income = church_incomes.exclude(income_type__in=excluded_income_types).aggregate(Sum('amount'))['amount__sum'] or 0

        total_week_expense = church_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        # Sum of tithe and offering from titheoffering model
        church_tithes_and_offerings = TitheOffering.objects.filter(
            church_member__church=church,
            sabbath_week=sabbath_week,
            sabbath_week__month__quarter=active_quarter_info
        ).aggregate(
            total_tithe=Sum('tithe'),
            total_offering=Sum('offering'),
            total_project=Sum('project')
        )
        total_tithe = church_tithes_and_offerings['total_tithe'] or 0
        total_offering = church_tithes_and_offerings['total_offering'] or 0
        total_project = church_tithes_and_offerings['total_project'] or 0

        combined_offering_church = CombinedOffering.objects.filter(
            associated_church=church,
            sabbath_week=sabbath_week,
            sabbath_week__month__quarter=active_quarter_info
        ).first()

        weeks_combined_top_2 = total_tithe + total_project + (combined_offering_church.amount_due_church if combined_offering_church else 0)

        # Calculate the combined income for the week using data from tithe offering model
        weeks_combined_income_2 = weeks_combined_top_2 + total_week_income
        balance_brought_forward = weeks_combined_income_2 - total_week_expense

        # Create a new BalanceBroughtForward entry
        # cls.objects.create(
        #     balance_amount=balance_brought_forward,
        #     sabbath_week=sabbath_week,
        #     church=church
        # )
   # Create a new BalanceBroughtForward entry
        return cls(church=church, sabbath_week=sabbath_week, balance_amount=balance_brought_forward)


class TrustFund(models.Model):
    fund_id = models.AutoField(primary_key=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, default=0)
    tithe_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    offering_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sabbath_week = models.ForeignKey(Sabbath, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now=True)

    def __str__(self):
        return f"Trust Fund - {self.total_amount}"
    
    def update_amounts(self):
        # Get the active week and associated church
        active_week = self.sabbath_week
        associated_church = self.church

        # Calculate tithe amount from TitheOffering model
        tithe_amount = TitheOffering.objects.filter(
            church_member__church=associated_church,
            sabbath_week=active_week
        ).aggregate(sum_tithe=Sum('tithe'))['sum_tithe'] or 0

        # Calculate offering amount from CombinedOffering model
        combined_offering_entry = CombinedOffering.objects.filter(
            associated_church=associated_church,
            sabbath_week=active_week
        ).first()

        if combined_offering_entry:
            offering_amount = combined_offering_entry.amount_due_conference
        else:
            offering_amount = 0

        # Update the TrustFund model
        self.tithe_amount = tithe_amount
        self.offering_amount = offering_amount
        self.total_amount = tithe_amount + offering_amount
        self.save()


class TotalToConference(models.Model):
    conf_id = models.AutoField(primary_key=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE)
    amount_remitted = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sabbath_week = models.ForeignKey(Sabbath, on_delete=models.CASCADE)
    remitance_date = models.DateField()
    date_added = models.DateField(auto_now=True)

    def __str__(self):
        return f"Conference Remittance - {self.church.church_name, self.amount_remitted}"


class DistrictIncome(models.Model):
    METHOD = (
        ('Others', 'Others'),
        ('Cash', 'Cash'),
        ('Bank', 'Bank'),
    )

    INCOME = (
        ('DONATION', 'DONATION'),
        ('VOW', 'VOW'),
        ('OFFERING_FROM_CHURCHES', 'OFFERING_FROM_CHURCHES'),
        ('PROJECT', 'PROJECT'),
        ('OTHERS', 'OTHERS'),
    )

    income_id = models.AutoField(primary_key=True)
    sabbath_week = models.ForeignKey(Sabbath, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=False, null=False)
    income_type = models.CharField(max_length=30, choices=INCOME)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=METHOD)
    date_added = models.DateField(auto_now=True)

    def __str__(self):
        return f"District income - {self.district.district_name, self.description}"


class DistrictExpense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    sabbath_week = models.ForeignKey(Sabbath, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False, default="expense")
    comment = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()
    date_added = models.DateField(auto_now=True)

    def __str__(self):
        return f"District Expenses - {self.district.district_name, self.title}"
