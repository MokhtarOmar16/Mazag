from django.contrib.auth.models import BaseUserManager
from django.db.models import Q

class UserManager(BaseUserManager):
    """Define a model manager for User model with username and email required."""

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """Create and save a User with the given username, email, and password."""
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        """Create and save a regular User with the given username and email."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """Create and save a SuperUser with the given username and email."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, identifier):
        """Fetch user by username or email."""
        return self.get(Q(username=identifier) | Q(email=identifier))
