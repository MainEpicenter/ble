# -*- coding: utf-8 -*-
#!/usr/bin/python3
# test BLE Scanning software
# 오픈소스 활용, 만든이: 주진원

import blescan #blescan.py 절대로 건들지 말아주세요
import sys
import time
import bluetooth._bluetooth as bluez

# -----------위의 모듈은 기존 오픈소스가 사용하는 module, 아래는 내가 쓰는 모듈 -------

import os
import sys
import struct
#import bluetooth._bluetooth as bluez -> 중복으로 주석
import bluetooth
import socket
import time
#import pexpect -> 이 module은 현재 쓸 계획 X
import subprocess
import glob

#--------------------------------- 오픈소스 시작----------------------------

dev_id = 0
try:
        sock = bluez.hci_open_dev(dev_id)
        #print ("ble thread started")

except:
        print ("error accessing bluetooth device...")
        sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

#--------------------- 이 위의 코드는 오픈 소스로 건들지 말기, 밑에 부분만 수정하자----------------------------

reset_point=0

def addr_confirm(addr):
    addr_set=['b8:27:eb:48:de:38', 'b8:27:eb:aa:2a:fd', 'b8:27:eb:a5:11:b8', 'b8:27:eb:96:5f:48', 'b8:27:eb:17:d9:c0', 'b8:27:eb:52:1b:57', 'b8:27:eb:32:ac:9d', 'b8:27:eb:61:96:25','b8:27:eb:b9:87:55','b8:27:eb:db:fe:06','b8:27:eb:ed:d2:9a','b8:27:eb:99:54:56','b8:27:eb:b0:05:dd','b8:27:eb:57:e3:74','b8:27:eb:af:b9:a5','b8:27:eb:38:cb:ca','b8:27:eb:90:aa:0c','b8:27:eb:3d:c0:38','b8:27:eb:e8:d2:e2','b8:27:eb:77:13:3d','b8:27:eb:3e:65:c9']
    #raspi_set=["0","1","2","3","4","5","6","7","8","9","10","11","12","13"]
    set_num=len(addr_set)
    run=False

    for i in range(0,set_num):
        if(addr_set[i]==str(addr)):
            result=str(i)
            run=True
    if run is False:
        result=False

    return result

def comfirm_hostname():
    myhost = os.uname()[1]
    host_order=int(myhost[1:])#노드의 숫자 1,2,3,4, 이런 숫자
    #host_list=['A0','A1','A2','A3','N1','N2','N3','N4'] #20개의 라즈베리파이에 Mac Address를 추가해라
    #그리고 arr[0][0]이 맨 처음 값이므로 노드 번호를 0번째부터 시작해야 맞는 것이다.
    #배열도 arr[0]가 먼저 시작이다.

    if myhost[0] == 'A':
        return host_order
    else:
        return host_order+3


def restart(): #이 함수는 오픈소스를 활용하여 만들었습니다. 수정하지 말것은 표시해놓겠습니다.
    global reset_point
    reset_point+=1
    if reset_point>6:
        executable = sys.executable#금지
        args = sys.argv[:]#금지
        args.insert(0, sys.executable)#금지
        time.sleep(2)#숫자는 바꿔도 된다
        os.execvp(executable, args)#금지


def send_data_server(ble_data,host_name):
    mac_address=ble_data[:17]
    rssi=int(ble_data[18:])

    if rssi>-70:
        raspi=addr_confirm(mac_address)#어떤 라즈베리파이인지 알려준다.
        #mat_data=str(raspi)+" "+str(rssi) #매트랩에 작성하기 위한 파일, data모으고 matlab에서 load해서 데이터 만들기 편함
        send_data=str(host_name)+'%'+str(raspi)
        if raspi is not False:
            #text.write(mat_data+'\r\n')
            time.sleep(0.2)
            #print(send_data) #디스플레이 환경에서 확인하기 유용

            #이렇게 해야 바로 전송하고 접속을 끊어서 다음 데이터가 잘 들어갈 수 있다.
            sock_data=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #sock_data.connect_ex(('166.104.75.39',8585)) -> 실험실 실험에서는 이것으로 과기관 실험에서는 192.168.0.2로
            if sock_data.connect_ex(('192.168.0.2',8585)) != 0:
                global reset_point
                reset_point=11#바로 종료하기 위한 코드 삽입
                restart()
            sock_data.send(send_data.encode())
            sock_data.close()

if __name__ == "__main__":
    #name=input()
    #name=name+".txt"
    host_name=comfirm_hostname()#라즈베리파이의 hostname을 가지고 있다.
    #text=open(name,"w+")
    while True:
        returnedList = blescan.parse_events(sock, 10)
        #print ("----------")
        for ble_data in returnedList:
            send_data_server(ble_data,host_name)
