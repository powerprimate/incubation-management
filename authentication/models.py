from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class user(AbstractUser):

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    username = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin         = models.BooleanField(default=False)
    is_staff         = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superuser     = models.BooleanField(default=False)
    
    USERNAME_FIELD  =   'email'
    REQUIRED_FIELDS =   ['name','phone_number']
    
    def __str__(self):
        return self.email


class Application(models.Model):
    
    INCUBATION=(
        ('virtual','virtual'),
        ('physical','physical'),
    )
    
    STATUS=(
        ('new','new'),
        ('pending','pending'),
        ('confirmed','confirmed'),
        ('cancelled','cancelled'),
    )
    
    user = models.ForeignKey(user, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50,null=True)
    email = models.EmailField(max_length=100,null=True)
    phone_number = models.IntegerField(null=True)
    company_name = models.CharField(max_length=50,null=True)
    company_image = models.ImageField(upload_to='company_image',null=True)
    team_and_background_desc = models.TextField(max_length=5000,null=True)
    company_and_product_desc = models.TextField(max_length=5000,null=True)
    problem_desc = models.TextField(max_length=5000,null=True)
    solution = models.TextField(max_length=5000,null=True)
    preposition = models.TextField(max_length=5000,null=True)
    competitors_and_competative_advantage = models.TextField(max_length=5000,null=True)
    revenue_model = models.TextField(max_length=5000,null=True)
    market_size = models.TextField(max_length=5000,null=True)
    marketing_plan = models.TextField(max_length=5000,null=True)
    incubation_type = models.CharField(max_length=50,choices=INCUBATION,default='virtual')
    business_proposal = models.TextField(max_length=5000,null=True)
    status = models.CharField(max_length=50,choices=STATUS,default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    
class slot(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    slot = models.IntegerField()
    booked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.application.name