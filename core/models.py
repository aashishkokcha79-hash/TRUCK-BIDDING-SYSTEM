from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('Customer', 'Customer'),
        ('Transporter', 'Transporter'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    contact_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class TransporterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='transporter_profile')
    transporter_name = models.CharField(max_length=255)
    vehicle_number = models.CharField(max_length=50)
    current_latitude = models.FloatField(default=0.0)
    current_longitude = models.FloatField(default=0.0)

    def __str__(self):
        return self.transporter_name

class Requirement(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requirements')
    source_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    winning_bid = models.ForeignKey('Bid', null=True, blank=True, on_delete=models.SET_NULL, related_name='won_requirements')

    def __str__(self):
        return f"{self.source_city} to {self.destination_city} ({self.status})"

class Bid(models.Model):
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='bids')
    transporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='placed_bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.transporter.username} for {self.amount}"
