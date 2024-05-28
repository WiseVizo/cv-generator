from django.db import models

# Create your models here.
class UserData(models.Model):
    #Personal Information
    full_name = models.CharField(max_length=180)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    linkedin_link = models.URLField(blank=True)

    #education
    university_name = models.CharField(max_length=200)
    major_field = models.CharField(max_length=200)
    graduation_year = models.CharField(max_length=10) # maybe this should be date field 
    course_name = models.CharField(max_length=100, default="BCA", blank=True)
    gpa_out_of_5 = models.DecimalField(max_digits=4, decimal_places=2, default=3.5)
    courses = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    educational_achivements = models.TextField(blank=True)

    #work experience if any
    have_work_experience = models.BooleanField(default=False)
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=150)
    date_joinned = models.DateField() # wait whts is this data time field instead
    date_quit = models.DateField()
    achivements = models.CharField(max_length=300)

    #Skills and Expertise
    programming_languages = models.CharField(max_length=350)
    frameworks = models.CharField(max_length=300)
    non_tech_skills = models.CharField(max_length=350)
    professional_qualifications = models.CharField(max_length=350)

    #carrer goals
    target_role = models.CharField(max_length=100)
    carrer_goals = models.CharField(max_length=400)

    def __str__(self):
        return self.full_name

