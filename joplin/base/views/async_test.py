from rest_framework.decorators import api_view
from rest_framework.response import Response
import threading
import time

def async_process():
    print(1)
    time.sleep(2)
    print(2)
    time.sleep(2)
    print(3)
    time.sleep(2)
    print(4)
    time.sleep(2)
    print(555555)
    time.sleep(2)
    print(6)
    time.sleep(2)
    print(7)
    time.sleep(2)
    print(8)
    time.sleep(2)
    print(9)
    time.sleep(2)
    print("TEN")

@api_view(['POST'])
def async_test(request):
    print("started async_test")
    threading.Thread(target=async_process).start()
    return Response(200)
