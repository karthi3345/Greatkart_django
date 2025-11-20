# from django.db import models
# from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager

# # Create your models here.

# class MyAccountManager(BaseUserManager):
#     def create_user(self,first_name, last_name,user_name,email,password=None):
#         if not email:
#             raise ValueError('User must have an email address')
#         if not user_name:
#             raise ValueError('User must have username')
        
#         user=self.model (
#             email=self.normalize_email(email), #if someone writtennin caps it change to small letter 
#             user_name=user_name,
#             first_name=first_name,
#             last_name=last_name,
#         )

# class Account(AbstractBaseUser):
#     first_name=models.CharField(max_length=50)
#     last_name=models.CharField(max_length=50)
#     user_name= models.CharField(max_length=50, unique= True)
#     email= models.EmailField(max_length=100, unique=True)
#     phno=models.CharField(max_length=50)

#     #required fields here

#     date_joined =models.DateField(auto_now_add=True)
#     last_login=models.DateField(auto_now_add=True)
#     is_admin=models.BooleanField(default=False)
#     is_staff=models.BooleanField(default=False)
#     is_active=models.BooleanField(default=False)
#     is_superadmin=models.BooleanField(default=False)

#     USERNAME_FIED= 'email'  #login with email address
#     REQUIRED_FIELDS= ['username','firstname','lastname']


#     def __str__(self):
#        return self.email # when we return it should return email addresds
    
#     def has_perm(self,perm,obj=None): #permission
#         return self.is_admin #user  is admin to make changes
    
#     def has_module_perms(self, add_label):
#         return True
    
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

### CUSTOM USER MANAGER
class MyAccountManager(BaseUserManager):

    ### Function to create a normal user
    def create_user(self, first_name, last_name, user_name, email, password=None):

        ### Check required fields (like database mandatory columns)
        if not email:
            raise ValueError("Email is required")

        if not user_name:
            raise ValueError("Username is required")

        ### Create a new user object (but not saved yet)
        user = self.model(
            email=self.normalize_email(email),   # cleans email format
            user_name=user_name,
            first_name=first_name,
            last_name=last_name
        )

        ### Set password using Django hashing (not plain text)
        user.set_password(password)

        ### Save user in database
        user.save(using=self._db)
        return user


    ### Function to create SUPERUSER (admin)
    def create_superuser(self, first_name, last_name, user_name, email, password):

        ### First create normal user
        user = self.create_user(
            email=email,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        ### Give superuser permissions
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_active = True

        user.save(using=self._db)
        return user



### CUSTOM USER MODEL
class Account(AbstractBaseUser):

    ### Basic user details (columns in table)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phno = models.CharField(max_length=50, blank=True)

    ### Auto fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    ### Permission-related fields
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    ### Login field → user logs in using email
    USERNAME_FIELD = 'email'

    ### Required fields when creating superuser
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    ### Connect custom manager
    objects = MyAccountManager()

    ### What to show when printing user
    def __str__(self):
        return self.email

    ### Permissions handling
    def has_perm(self, perm, obj=None):
        return self.is_admin  # Only admins have full permissions

    def has_module_perms(self, app_label):
        return True  # User can view all apps



### OPTIONAL: Change table name in database
    class Meta:
        db_table = "accounts"    # table name in PostgreSQL
