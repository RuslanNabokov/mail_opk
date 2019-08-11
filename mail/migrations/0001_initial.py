# Generated by Django 2.2.1 on 2019-07-22 10:40

from django.db import migrations, models
import django.db.models.deletion
import mail.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_to_folder', to='main.AuthUser')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('body', models.CharField(blank=True, max_length=1000, null=True)),
                ('secrecy', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')])),
                ('article_date', models.DateTimeField(blank=True, default=mail.models.default_datetime, null=True)),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folder_to_message', to='mail.Folder')),
            ],
        ),
        migrations.CreateModel(
            name='Group_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lifetime', models.DateTimeField(blank=True, null=True)),
                ('have_read', models.ManyToManyField(blank=True, related_name='dsds', to='main.Profile', verbose_name='Кто прочел')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sdsd', to='mail.Message', verbose_name='Message')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='otprav', to='main.Profile', verbose_name='Пользователь')),
                ('users', models.ManyToManyField(related_name='users', to='main.Profile', verbose_name='Получатели почты')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('ps', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=25, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=mail.models.get_file_path)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Сообщение', to='mail.Message')),
            ],
        ),
    ]
