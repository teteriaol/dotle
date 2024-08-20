@echo off
echo Running commands in the console...

set "start_dir=%CD%"

cd /d "%start_dir%\dotle"

rem echo Files in the 'dotle' folder:
rem dir /b

python manage.py makemigrations

python manage.py migrate

cd /d "%start_dir%"

pause
