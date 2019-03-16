# -*- coding: utf-8 -*
import serial
import time
import serial.tools.list_ports
#ser = serial.Serial("com3", 9600)

def get_ser():
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <= 0:
        print("没有发现端口!")
    else:
        plist_0 = list(plist[0])
        serialName = plist_0[0]
        ser = serial.Serial(serialName, 9600, timeout=60)
        return ser



def main():
    c = 0;f=False
    plist = list(serial.tools.list_ports.comports())
    try:
        if len(plist) <= 0:
            print("没有发现端口!")
        else:
            plist_0 = list(plist[0])
            serialName = plist_0[0]
            ser = serial.Serial(serialName, 9600, timeout=60)
            print("可用端口名>>>", ser.name)

            st=time.time()
            while True:
                ser.flushInput()
                count = ser.inWaiting()

                if count :
                    print(count)
                    #ser.write(b'qqq\r\n')
                    recv = ser.read_all()
                    print(recv)
                    f=True
                    #ser.write(recv)
                if(time.time()-st>3 and not f):
                    raise KeyboardInterrupt


    except KeyboardInterrupt:
        print('无信息')
        if ser != None:
            ser.close()


if __name__ == '__main__':
    main()