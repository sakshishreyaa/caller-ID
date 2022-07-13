from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where phone is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, phone, password, name,**extra_fields):
        """
        Create and save a User with the given phone and password.
        """
        if extra_fields.get('email'):
            extra_fields['email'] = self.normalize_email(extra_fields['email'])
        user = self.model(phone=phone,name=name, **extra_fields)
        user.set_password(password)
        if  extra_fields.get('spam'):
            user.spam = extra_fields['spam']
        user.save()
        return user

    def create_superuser(self, email, password,name, **extra_fields):
        """
        Create and save a SuperUser with the given phone and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password,name, **extra_fields)