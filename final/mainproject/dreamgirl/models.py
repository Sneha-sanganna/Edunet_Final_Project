from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator



class Candidate(models.Model):
    PARTY_CHOICES = [
        ('BJP', 'BJP'),
        ('Congress', 'Congress'),
        ('JDS', 'JDSB'),
        ('BSP', 'BSP'), 

    ]

    LOCATION_CHOICES = [
        ('Doranahalli', 'Doranahalli'),
        ('Shahapur', 'Shahapur'),
        ('Jayanagar', 'Jayanagar'),
        ('Vasantapura', 'Vasantapura'),
        ('Hosur', 'Hosur'),
    ]

    name = models.CharField(max_length=100)
    party = models.CharField(max_length=20, choices=PARTY_CHOICES)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    votes = models.IntegerField(default=0)   # total votes only (anonymous)
    party_logo = models.ImageField(upload_to='party_logos/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.party}) - {self.location}"


# 🔒 VOTER MODEL — ONE PERSON = ONE VOTE
class Voter(models.Model):
    aadhaar_number = models.CharField(max_length=12, unique=True)
    voter_id = models.CharField(max_length=10
                                , unique=True)

    has_voted = models.BooleanField(default=False)   # ⭐ MAIN ONE-TIME VOTE FLAG
    voted_at = models.DateTimeField(null=True, blank=True)  # optional (audit)
    email = models.EmailField(unique=True,blank=True,null=True)
    location = models.CharField(max_length=50,null=True,blank=True)
    age = models.IntegerField(
        validators=[MinValueValidator(18)],
        null=True,
        blank=True
    )
    gender = models.CharField(max_length=10,null=True,blank=True)

    
    reset_code = models.CharField(max_length=6, blank=True, null=True)
    
    
    
    def __str__(self):
        return f"{self.aadhaar_number} - {self.voter_id}"






class PreApprovedVoter(models.Model):
    aadhaar_number = models.CharField(max_length=12)
    voter_id = models.CharField(max_length=10)

    location = models.CharField(max_length=50)

    class Meta:
        unique_together = ('aadhaar_number', 'voter_id', 'location')

    def __str__(self):
        return f"{self.voter_id} - {self.aadhaar_number} ({self.location})"





class ElectionSettings(models.Model):
    voting_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Election on {self.voting_date}"

