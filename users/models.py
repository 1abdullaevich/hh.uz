from django.db import models
from django.contrib.auth.models import AbstractUser


class LocationModel(models.Model):
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.city}, {self.country}"

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        db_table = 'locations'


class MyUserModel(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.ForeignKey(LocationModel, on_delete=models.SET_NULL, blank=True, null=True)

    otp = models.CharField(max_length=6, null=True)
    otp_max_try = models.IntegerField(default=3, null=True)
    otp_expiry = models.DateTimeField(null=True)
    otp_max_out = models.DateTimeField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'


class CompanyModel(models.Model):
    user = models.OneToOneField(MyUserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        db_table = 'companies'


class VacancyModel(models.Model):
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    location = models.ForeignKey(LocationModel, on_delete=models.SET_NULL, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
        db_table = 'vacancies'


class ApplicationModel(models.Model):
    employee = models.ForeignKey(MyUserModel, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(VacancyModel, on_delete=models.CASCADE)
    message = models.TextField()
    resume = models.FileField(upload_to='employee_resumes/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} applied for {self.vacancy.title}"

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        db_table = 'applications'


class SkillModel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
        db_table = 'skills'


class EducationModel(models.Model):
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    graduation_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.degree} from {self.institution} ({self.graduation_year})"

    class Meta:
        verbose_name = 'Education'
        verbose_name_plural = 'Educations'
        db_table = 'educations'


class ExperienceModel(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} at {self.company}"

    class Meta:
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'
        db_table = 'experiences'


class SkillSetModel(models.Model):
    employee = models.ForeignKey(MyUserModel, on_delete=models.CASCADE)
    skill = models.ForeignKey(SkillModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee.email} - {self.skill.name}"

    class Meta:
        verbose_name = 'Skill Set'
        verbose_name_plural = 'Skill Sets'
        db_table = 'skill_sets'


class EmployeeEducationModel(models.Model):
    employee = models.ForeignKey(MyUserModel, on_delete=models.CASCADE)
    education = models.ForeignKey(EducationModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee.email} - {self.education}"

    class Meta:
        verbose_name = 'Employee Education'
        verbose_name_plural = 'Employee Educations'
        db_table = 'employee_educations'


class EmployeeExperienceModel(models.Model):
    employee = models.ForeignKey(MyUserModel, on_delete=models.CASCADE)
    experience = models.ForeignKey(ExperienceModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee.email} - {self.experience}"

    class Meta:
        verbose_name = 'Employee Experience'
        verbose_name_plural = 'Employee Experiences'
        db_table = 'employee_experiences'
