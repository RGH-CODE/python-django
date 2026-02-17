

from django.db import migrations

from django.db import migrations, models
class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_productimage_image'),
    ]

    operations = [
       migrations.RunSQL(
            sql="""
                ALTER TABLE store_customer
                ADD COLUMN IF NOT EXISTS first_name VARCHAR(255);
                ALTER TABLE store_customer
                ADD COLUMN IF NOT EXISTS last_name VARCHAR(255);
            """,
            reverse_sql="""
                ALTER TABLE store_customer
                DROP COLUMN IF EXISTS first_name;
                ALTER TABLE store_customer
                DROP COLUMN IF EXISTS last_name;
            """
        ),
    ]
