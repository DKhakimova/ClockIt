from django.db import models

# Create your models here.

class Timesheet(models.Model):
    clock_in_time = models.DateTimeField(auto_now_add=True)
    clock_out_time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey('login_registration_app.User', related_name='employee_timesheet', on_delete=models.CASCADE, default='', null=True, blank=True)


class CompanyManager(models.Manager):
  
    def company_create(self, form_data):
        return self.create(
            name=form_data['name']
        )


    def validate(self, form_data):
        errors = {}
        if len(form_data['name']) < 3:
            errors['name'] = 'Company name must be at least 3 characters'
        company_with_name = self.filter(name=form_data['name'])
        if company_with_name:
            errors['name'] = 'Company already exists.'

        return errors

class Company(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CompanyManager()

    

