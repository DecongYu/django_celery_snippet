### django_celery_snippet
(This piece is meant for self-usage)
* Basic Django-celery with flower monitoring project structure. Celery, Django, Redis Django-channels, Django-Celery-beat are dockerized
* Celery worker change reload
* Task sheduler, failed task retry
* System monitoring (Celery logging, or hijacked Django logging) 
For the testing purpose, some bash commands and python executables are listed as follwing:
```bash
docker-compose exec <docker-service-name> bash
```
```bash
./manage.py shell
```
OR
```bash
docker-compose exec <docker-service-name> python manage.py shell
```bash
<clery_task>.delay()
```
```bash
<celery_task>.apply_async(args=[*arg], countdown=5)
```
