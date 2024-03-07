from .models import Conference, User, Quarter, Church, District, AssignedOfficer,Sabbath,Year

def getGlobalContext(user):
    try:
        conference = Conference.objects.get(id=1)
    except Conference.DoesNotExist:
        conference = None

    try:
        active_quarter = Quarter.objects.get(is_active=True)
    except Quarter.DoesNotExist:
        active_quarter = None

    try:
        active_week = Sabbath.objects.get(is_active=True)
    except Sabbath.DoesNotExist:
        active_week = None

    try:
        active_year = Year.objects.get(is_active=True)
    except Sabbath.DoesNotExist:
        active_year = None

    # Get user's associated church and district based on their role
    associated_church = None
    associated_district = None

    if user.role in ['Church_treasurer', 'Church_secretary']:
        # User is associated with a church
        assigned_officer = AssignedOfficer.objects.filter(officer=user).first()
        if assigned_officer:
            associated_church = assigned_officer.church
            associated_district = assigned_officer.district  # Access associated district through AssignedOfficer

    elif user.role in ['District_treasurer', 'District_secretary']:
        # User is associated with a district
        assigned_officer = AssignedOfficer.objects.filter(officer=user).first()
        if assigned_officer:
            associated_district = assigned_officer.district  # Access associated district through AssignedOfficer
    
    sabbath_week_start = None
    sabbath_week_ends = None
    if active_week:
        sabbath_week_start = active_week.sabbath_week_start
        sabbath_week_ends = active_week.sabbath_week_ends


    return {
        'conference': conference,
        'active_quarter': active_quarter,
        'associated_church': associated_church,
        'associated_district': associated_district,
        'active_week': active_week,
        'sabbath_week_start': sabbath_week_start,
        'sabbath_week_ends': sabbath_week_ends,
    }