from django.db import models

from django.contrib.auth.models import User


# for classifying the budget to schoool by the moe
from django.utils import timezone

class SchoolBudget(models.Model):
    school_username = models.CharField(max_length=100)
    school_items = models.IntegerField(default=0)   # computer, marker, desk, table, pen, paper, etc  
    food=models.IntegerField(default=0)
    health = models.IntegerField(default=0)  #first aid kit, sanitary pads
    transportation = models.IntegerField(default=0)  # buses
    clothes = models.IntegerField(default=0)  # uniform, shoes, tie
    bills = models.IntegerField(default=0)   # electricity, water, gas, internet
    sports = models.IntegerField(default=0)  # sports related 
    extra_curricular = models.IntegerField(default=0)  #events, programs
    distributed = models.BooleanField(default=False) #whether distributed or not
    curr_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.curr_date = timezone.now().date()
        super(SchoolBudget, self).save(*args, **kwargs)

# Monthly Saving Plan (1 row for one school)
class MonthlySavingPlan(models.Model):
    school_username = models.CharField(max_length=100)
    school_items = models.IntegerField(default=0)   # computer, marker, desk, table, pen, paper, etc  
    food=models.IntegerField(default=0)
    health = models.IntegerField(default=0)  #first aid kit, sanitary pads
    transportation = models.IntegerField(default=0)  # buses
    clothes = models.IntegerField(default=0)  # uniform, shoes, tie
    bills = models.IntegerField(default=0)   # electricity, water, gas, internet
    sports = models.IntegerField(default=0)  # sports related 
    extra_curricular = models.IntegerField(default=0)  #events, programs
    status=models.BooleanField(default=True) # check if running out of plan or not


#Daily saving plan (daily rows for each of the school)
class DailySavingPlan(models.Model):
    school_username = models.CharField(max_length=100)
    school_items = models.IntegerField(default=0)   # computer, marker, desk, table, pen, paper, etc  
    food=models.IntegerField(default=0)
    health = models.IntegerField(default=0)  #first aid kit, sanitary pads
    transportation = models.IntegerField(default=0)  # buses
    clothes = models.IntegerField(default=0)  # uniform, shoes, tie
    bills = models.IntegerField(default=0)   # electricity, water, gas, internet
    sports = models.IntegerField(default=0)  # sports related 
    extra_curricular = models.IntegerField(default=0)  #events, programs




# for daily tracking the budget by school
class DailyTrack(models.Model):
    school_username = models.CharField(max_length=100)
    food=models.IntegerField()
    school_items=models.IntegerField()   # computer, marker, desk, table, pen, paper, etc  
    health=models.IntegerField()  #first aid kit, sanitary pads
    transportation=models.IntegerField()  # buses
    clothes=models.IntegerField()  # uniform, shoes, tie
    bills=models.IntegerField()   # electricity, water, gas, internet
    sports=models.IntegerField()  # sports related 
    extra_curricular=models.IntegerField()  #events, programs
    notes=models.CharField(max_length=300,default="")  #write short summary on the expenses today
    current_date=models.CharField(max_length=50)  #today date (day/month/year format)


class SchoolForm(models.Model):
    # school details
    schoolname=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    state=models.IntegerField()
    pan=models.CharField(max_length=30)
    image_file = models.ImageField(upload_to='images/')




    # Infrastructure details
    classrooms=models.IntegerField()
    laboratories=models.IntegerField()
    library=models.IntegerField()
    computer_labs=models.IntegerField()
    staff_rooms=models.IntegerField()


    # Academic Details
    students=models.IntegerField()
    teachers=models.IntegerField()
    administrative_staffs=models.IntegerField()


    # principal Details
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    contact_email=models.CharField(max_length=100)
    educational_background=models.CharField(max_length=100,default="")
    years_of_experience=models.IntegerField()
    vision_for_school=models.CharField(max_length=200,default="")

    status=models.IntegerField(default=0)

    def __str__(self):
        return self.image_file.name
    
