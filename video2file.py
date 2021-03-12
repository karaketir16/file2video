# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2
import base64
import sys
from pyzbar import pyzbar


def read_the_barc(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        barcode_info = barcode.data.decode('utf-8')
        return True, barcode_info
    return False, 0

def read_vid():
    cap = cv2.VideoCapture(sys.argv[1])
    counter = 0
    file = open(sys.argv[2], "wb")

    while(cap.isOpened()):
        counter += 1
        print(counter)
        ret, frame = cap.read()
        if ret:
            res, retval = read_the_barc(frame)
            assert res
            file.write(base64.b64decode(retval))
        else:
            break

    file.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print('PyCharm')
    # my_func_3()
    read_vid()
    # main()
    # print("After")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


#https://towardsdatascience.com/building-a-barcode-qr-code-reader-using-python-360e22dfb6e5

