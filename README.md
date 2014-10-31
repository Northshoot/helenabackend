helenabackend
=============
Django version 1.7!

pip install django_chartit
pip install django_autofixture
pip install simplejson
pip install requests 

chatit must be patched:
move files from patch_chartit to install dir


to install test data:

python manage.py loadtestdata databucket.Firestorm:30
python manage.py loadtestdata databucket.ObservedDevice:100
python manage.py loadtestdata databucket.FirestormReading:100

to send data localy use sendData.py example functions