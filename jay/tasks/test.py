from example_celery import celery_app
from django.conf import settings


def test():
    """เรียกใช้ task 'celery' แบบ asynchronous ผ่าน .delay()
    เป็นฟังก์ชันตัวกลางสำหรับส่ง task เข้า queue ของ Celery"""
    celery.delay()


@celery_app.task(bind=True, max_retries=5, default_retry_delay=15)  # Retry ทุก 15 วินาที
def celery(self):
    """Celery task ตัวอย่างที่สาธิตกลไกการ retry

    การทำงาน:
    - ดึงจำนวนครั้งที่ retry แล้วจาก self.request.retries
    - ถ้าจำนวนครั้ง retry อยู่ในช่วง 0-3 จะเปลี่ยนค่า x เป็น string 'error'
      ทำให้การบวก 1 + x เกิด TypeError (จำลองสถานการณ์ error)
    - เมื่อ retry ครั้งที่ 4 (ไม่อยู่ในลิสต์ z) ค่า x จะเป็นตัวเลข → บวกได้สำเร็จ
    - ถ้าเกิด exception จะ retry อัตโนมัติ (สูงสุด 5 ครั้ง)
    """
    retries_times = self.request.retries
    print('celery start {}'.format(retries_times))

    try:
        x = retries_times
        z = [0, 1, 2, 3]
        # ถ้า retry ครั้งที่ 0-3 จะจงใจสร้าง error โดยเปลี่ยน x เป็น string
        if retries_times in z:
            x = 'error'

        # ถ้า x เป็น string จะเกิด TypeError ที่บรรทัดนี้ → เข้า except → retry
        data = 1 + x
        print('success')
    except Exception as exc:
        # เกิด error → สั่ง retry task ใหม่อีกครั้ง
        raise self.retry()


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)  # Retry ทุก 30 วินาที
def celery_1(self):
    """Celery task ตัวอย่างอีกตัว สำหรับทดสอบการรัน task พื้นฐาน
    แค่ print ข้อความออกมาเพื่อยืนยันว่า task ถูกเรียกใช้งานสำเร็จ
    ตั้งค่า retry สูงสุด 3 ครั้ง ห่างกันครั้งละ 30 วินาที
    """
    print('TEST cxcxcxcxcxcxcxcxcxcxccxcxcxcxcxcxcxcxcxcxcxcxcxcxcx=c=x=c=x=cx=c=x=c=x=c=xc=x=c=x')
    