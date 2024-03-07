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
        ('SABBATH_SCHOOL', 'SABBATH_SCHOOL'),
        ('LOOSE_OFFERING', 'LOOSE_OFFERING'),
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
    church = models.ForeignKey(Church, on_delete=models.CASCADE, default=0)
    comment = models.CharField(max_length=255, blank=True, null=True)
    income_type = models.CharField(max_length=20, choices=INCOME)
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
   
    # @classmethod
    # def calculate_combined_offering(cls, church_income_entries, church):
    #         # Extract ChurchIncome entries IDs
    #         church_income_ids = [entry.income_id for entry in church_income_entries]

    #         # Fetch relevant ChurchIncome entries as a queryset for each entry's week
    #         church_income_queryset = ChurchIncome.objects.filter(
    #             income_id__in=church_income_ids
    #         ).filter(
    #             sabbath__in=[entry.sabbath for entry in church_income_entries],
    #             income_type__in=['APPRECIATION', 'LOOSE_OFFERING', 'CHILD_DEDICATION', 'THANKS_OFFERING', 'SABBATH_SCHOOL']
    #         )
    #         print('ssssssssssssssssssssssssssssssssssssssssssss',church_income_queryset)
    #         for i in church_income_queryset:
    #             print (i.sabbath_id)

    #         # Extract related TitheOffering entries IDs
    #         tithe_offering_ids = TitheOffering.objects.filter(
    #             donation_id__in=church_income_queryset
    #         ).values_list('donation_id', flat=True)

    #         # Fetch relevant TitheOffering entries as a queryset
    #         tithe_offering_queryset = TitheOffering.objects.filter(donation_id__in=tithe_offering_ids)

    #         # Calculate combined offering
    #         combined_offering = (
    #             church_income_queryset.aggregate(amount=Sum('amount'))['amount'] or 0 +
    #             tithe_offering_queryset.aggregate(offering=Sum('offering'))['offering'] or 0
    #         )

    #         # Calculate amounts due based on percentages
    #         amount_due_district = float(combined_offering) * 0.10
    #         amount_due_church = float(combined_offering) * 0.50
    #         amount_due_conference = float(combined_offering) * 0.40

    #         # Fetch the active Sabbath
    #         active_sabbath = Sabbath.objects.filter(is_active=True).first()

    #         # Create or update the CombinedOffering entry
    #         combined_offering_entry, created = cls.objects.update_or_create(
    #             associated_church=church,
    #             sabbath_week=active_sabbath,
    #             defaults={
    #                 'combined_offering': combined_offering,
    #                 'amount_due_district': amount_due_district,
    #                 'amount_due_church': amount_due_church,
    #                 'amount_due_conference': amount_due_conference,
    #             }
    #         )

    #         # Calculate and update total_available_income
    #         # combined_offering_entry.update_total_available_income()

    #         return combined_offering_entry, created

  
class ChurchExpense(models.Model):

    expense_id = models.AutoField(primary_key=True)
    sabbath = models.ForeignKey(Sabbath, on_delete=models.CASCADE, default=0)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, default=0)
    title = models.CharField(max_length=255, blank=False, null=False)
    comment = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str("Expense =" + "" + self.title + " " + self.comment)


class ChurchCashAccount(models.Model):
    cash_id = models.AutoField(primary_key=True)
    cash_generated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cash_spent = models.DecimalField(max_digits=10, decimal_places=2)
    cash_to_bank = models.DecimalField(max_digits=10, decimal_places=2)
    cash_at_hand = models.DecimalField(max_digits=10, decimal_places=2)
    sabbath_week = models.ForeignKey(Sabbath, on_delete=models.CASCADE)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, default=0)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sabbath_week.sabbath_alias


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
