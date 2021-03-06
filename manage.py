#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mail_cnii.settings')

    if  sys.argv[1] == 'create_users':
        import django
        django.setup()
        from django.contrib.auth.models import User
        from mail.models import Profile
  
        print('  Начинаю  создавать пользователей ')
        f = open('users.txt', 'r')
        i = 0
        for line in f:
            print(line.split(' '))
            try:
                name,famaly,login, passwd = line.split(' ')                                      # name famaly org  login passwd\
                new_use = User.objects.create(username= name, password = passwd)
                new_use.save()
                new_prof = Profile.objects.create(position= 'user', first_name_d = name, last_name_d = famaly, user = new_use )
                i+=1
                print('создал: {} {}  '.format(name,famaly))
            except Exception as e:
                print('Ошибка: {} '.format(e)) 
                
            print('создано пользователей: {}'.format(i))
        print('Создание пользователей прошло успешно')
        return

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
