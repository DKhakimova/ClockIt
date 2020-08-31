from django.db import models
from clock_it_app.models import Company
import re

# Create your models here.
class UserManager(models.Manager):
  def validate(self, form_data):
    errors = {}
    if len(form_data['first']) < 2:
      errors['first'] = 'First name should be at least 2 characters.'
    if len(form_data['last']) < 2:
      errors['last'] = 'Last name should be at least 2 characters.'
  
    if not form_data['first'].isalpha() and form_data['first'] != '':
      errors['first'] = "First name must contain only letters."

    if not form_data['last'].isalpha() and form_data['last'] != '':
        errors['last'] = "Last name must contain only letters."
    
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(form_data['email']):        
        errors['email'] = ("Invalid email address.")

    exist_email = self.filter(email=form_data['email'])
    if exist_email:
      errors['email'] = 'Email already in use.'

    if len(form_data['password']) < 8:
      errors['password'] = "Password must be at least 8 characters."
    
    if form_data['cpassword'] != form_data['password']:
      errors['cpassword'] = "Passwords did not match."
    return errors

class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  admin = models.BooleanField(default = False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)

  objects = UserManager()

