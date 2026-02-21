from django.contrib import admin
from django.utils import timezone
from datetime import datetime, date, time
from .models import Candidate, PreApprovedVoter
from .models import ElectionSettings


# =========================================
# 🕒 Voting Start Time
# =========================================

VOTING_DATE = date(2026, 2, 14)
START_TIME = time(9, 0)

def voting_started():
    start = timezone.make_aware(datetime.combine(VOTING_DATE, START_TIME))
    return timezone.localtime(timezone.now()) >= start


# =========================================
# 🔒 Candidate Control
# =========================================

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):

    list_display = ('name', 'party', 'location', 'votes')

 #✅ Only allow ADD before 9 AM
    def has_add_permission(self, request):
        return not voting_started()

    #❌ Never allow edit
    def has_change_permission(self, request, obj=None):
       return False

    # ❌ Never allow delete
    def has_delete_permission(self, request, obj=None):
        return False


# =========================================
# 🔒 PreApproved Voter Control
# =========================================

@admin.register(PreApprovedVoter)
class PreApprovedVoterAdmin(admin.ModelAdmin):

    list_display = ('aadhaar_number', 'voter_id', 'location')

    # ✅ Only allow ADD before 9 AM
    #def has_add_permission(self, request):
        #return not voting_started()

    # ❌ Never allow edit
    def has_change_permission(self, request, obj=None):
        return False

    # ❌ Never allow delete
    #def has_delete_permission(self, request, obj=None):
      #  return False








admin.site.register(ElectionSettings)
