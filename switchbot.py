import time
import hashlib
import hmac
import base64
import subprocess
import requests
import json
import os
import logging

def updateDeviceMap(devices):
    writestream = {}
    for device in devices:
        writestream[device['deviceName'].strip()] = device['deviceId']
    f = open(os.environ['SB_DEVICE_MAP'])
    current_config = f.read()
    f.close()
    if writestream != current_config:
        f = open(os.environ['SB_DEVICE_MAP'],'w')
        f.write(repr(writestream))
        f.close()


class SwitchBot(object):

    def __init__(self):
        logging.info('Setting up program defaults')
        self.BASEURL = 'https://api.switch-bot.com'
        self.DEVICES = '/v1.1/devices'
        self.DEVICE_STATUS = '/v1.1/devices/DEVICEID/status'
        self.DEVICE_COMMANDS = '/v1.1/devices/DEVICEID/commands'
        self.token = os.environ['TOKEN']
        self.secret = os.environ['SECRET']
        self.nonce = subprocess.run(['uuid'],stdout=subprocess.PIPE).stdout.decode().strip()
        self.PARAMS = {
                'command':'',
                'parameter':'default',
                'commandType':'command'
                }

    def authorize(self):
        logging.info('Calling authorization module')
        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(self.token, t, self.nonce)
        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(self.secret, 'utf-8')
        self.sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
        self.HEADERS = {
            'Authorization':format(self.token),
            'sign':format(str(self.sign, 'utf-8')),
            't':format(t),
            'nonce':format(self.nonce),
            'Content-Type': 'application/json; charset=utf8'
        }

    def getRequest(self, url, headers):
        #print(url)
        logging.info('Calling URL : %s' %url)
        r = requests.get(url = url, headers = headers)
        return r.json()

    def postRequest(self, url, params, headers):
        #print(url)
        logging.info('Calling URL : %s' %url)
        r = requests.post(url = url, data=json.dumps(params), headers = headers)
        return r.json()


    def getDevices(self):
        self.authorize()
        logging.info('Extracting device list')
        data = self.getRequest(url = self.BASEURL+self.DEVICES, headers = self.HEADERS)
        if data['message'] == 'success':
            self.deviceList = data['body']['deviceList']
            #print(self.deviceList)
            updateDeviceMap(self.deviceList)
        else:
            print(data['message'])
            self.deviceList = []
        return self.deviceList

    def getDeviceId(self, name):
        self.authorize()
        logging.info('Locating Device ID of the Device : %s' %name)
        data = self.getRequest(url = self.BASEURL+self.DEVICES, headers = self.HEADERS)
        if data['message'] == 'success':
            self.deviceList = data['body']['deviceList']
            #print(self.deviceList)
        else:
            print(data['message'])
            self.deviceList = []
        if self.deviceList:
            for device in self.deviceList:
                if device['deviceName'] == name:
                    return device['deiveId']
        else:
            return ''

    def getDeviceStatus(self, deviceId):
        self.authorize()
        logging.info('Capturing current state of the Device : %s' %deviceId)
        data = self.getRequest(url = self.BASEURL+self.DEVICE_STATUS.replace('DEVICEID',str(deviceId)), headers = self.HEADERS)
        #data = r.json()
        #print(data['body']['lockState'])
        return data['body']['lockState']
            
    def unlockDevice(self, deviceId):
        self.authorize()
        self.PARAMS['command'] = 'unlock'
        #print(self.PARAMS)
        logging.info('Attempting to unlock the Device : %s' %deviceId)
        data = self.postRequest(url = self.BASEURL + self.DEVICE_COMMANDS.replace('DEVICEID',str(deviceId)), params=self.PARAMS, headers = self.HEADERS)
        logging.info(data)
            
    def lockDevice(self, deviceId):
        self.authorize()
        self.PARAMS['command'] = 'lock'
        #print(self.PARAMS)
        logging.info('Attempting to lock the Device : %s' %deviceId)
        data = self.postRequest(url = self.BASEURL + self.DEVICE_COMMANDS.replace('DEVICEID',str(deviceId)), params=self.PARAMS, headers = self.HEADERS)
        logging.info(data)

def main():
    #Test working of Switchbot API by locking or unlocking Fluffy Door
    sb = SwitchBot()
    devices = sb.getDevices()
    for device in devices:
        if device['deviceName'] == 'Fluffy Door':
            status = sb.getDeviceStatus(device['deviceId'])
            if status == 'locked':
                sb.unlockDevice(device['deviceId'])
            else:
                sb.lockDevice(device['deviceId'])
    logging.info('End of demo program')

main()
