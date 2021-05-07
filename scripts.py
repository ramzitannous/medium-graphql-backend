import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medium.settings")
django.setup()

from users.models import User

User.objects.create_user(
    "ramzi@ramzi.com", "ramzi", username="ramzi", bio="this is ramzi"
)
User.objects.create_superuser("ramzi@admin.com", "ramzi", username="ramzi admin")
