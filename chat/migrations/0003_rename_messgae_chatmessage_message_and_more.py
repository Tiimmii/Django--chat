# Generated by Django 4.1 on 2023-04-04 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_thread_chatmessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatmessage',
            old_name='messgae',
            new_name='message',
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chatmessage_thread', to='chat.thread'),
        ),
    ]
