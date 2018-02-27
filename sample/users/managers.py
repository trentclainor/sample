from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_candidate(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_candidate', True)
        extra_fields.setdefault('is_admin', False)
        return self.create_user(email, password, **extra_fields)

    def create_recruiter(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_recruiter', True)
        extra_fields.setdefault('is_admin', False)
        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given name, email and password.
        """
        extra_fields.setdefault('is_candidate', False)
        extra_fields.setdefault('is_recruiter', False)
        extra_fields.setdefault('is_admin', False)

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_candidate', False)
        extra_fields.setdefault('is_recruiter', False)
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


