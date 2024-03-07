from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import ChurchIncome, TitheOffering, CombinedOffering, TrustFund
@receiver(post_save, sender=CombinedOffering)
def update_trust_fund(sender, instance, **kwargs):
    """
    Signal receiver to update TrustFund model when CombinedOffering is created or updated.
    """
    active_week = instance.sabbath_week
    associated_church = instance.associated_church

    # Check if TrustFund record exists for the combination of church and active week
    trust_fund, created = TrustFund.objects.get_or_create(
        church=associated_church,
        sabbath_week=active_week
    )

    # Update the TrustFund amounts
    trust_fund.update_amounts()