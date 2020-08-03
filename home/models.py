from django.db import models
import re
from datetime import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, postData):
        #create a hash
        pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name=postData['first_name'],
            last_name=postData['last_name'],
            email=postData['email'],
            password=pw_hash,
        )
    # To check login
    def authenticate(self, email, password):
        user_with_email = self.filter(email = email)
        if not user_with_email:
            return False
        user = user_with_email[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def validator(self, postData):
        errors = {}
        # to validate name
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be atleast 3 characters.'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be atleast 2 characters.'

        # to validate email
        if len(postData['email']) < 1:
            errors['email'] = "Email is required."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        result =  self.filter(email = postData['email'])
        if len(result) > 0:
            errors['email'] = "Email is already in use."
        # to validate pw
        if len(postData['password']) < 4:
            errors['password'] = 'Password required, should be atleast 6 characters.'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Confirmation didn't match the password"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.TextField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
