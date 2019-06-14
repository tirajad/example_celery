from example_celery import celery_app
from django.conf import settings

def test():
    celery.delay()



@celery_app.task(bind=True, max_retries=5, default_retry_delay=15)  # Retry in 15 s
def celery(self):
    retries_times = self.request.retries
    print('celery start {}'.format(retries_times))

    try:
        x = retries_times
        z = [0, 1, 2, 3]
        if retries_times in z:
            x = 'error'

        data = 1 + x
        print('success')
    except Exception as exc:
        # print(exc)
        raise self.retry()



@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)  # Retry in 30 s
def celery_1(self):
    print('TEST adsad5a1s45d45a4d5a14s5d45as1d5sa1d3a12d1a3da2')
    