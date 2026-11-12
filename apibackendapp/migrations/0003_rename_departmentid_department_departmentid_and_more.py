from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("apibackendapp", "0002_project"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = []
