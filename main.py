# -*- coding: utf-8 -*-

import os
import json
import requests
import arrow

from flask import Flask
from flask import request

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        post_data = request.get_data()
        send_alert(bytes2json(post_data))
        return 'success'
    else:
        return 'weclome to use prometheus alertmanager dingtalk webhook server!'


def bytes2json(data_bytes):
    data = data_bytes.decode('utf8').replace("'", '"')
    return json.loads(data)


def send_alert(data):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=dd7d1e614b4c852c17deac7d282e1825aa2ea8d3f16d712d9fb6cc3568a193c5' 
    #print "alert:", data['alerts']
    for output in data['alerts'][:]:
        #print "output:", output
        send_data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "prometheus_alert",
                "text": "## 告警项目: %s \n\n" % output['labels']['job'] + 
                        "**告警级别**: %s \n\n" % output['labels']['severity'] +
                        "**告警类型**: %s \n\n" % output['labels']['alertname'] +
                        "**告警实例**: %s \n\n" % output['labels']['instance'] +
                        "**告警详情**: %s \n\n" % output['annotations']['summary'] +
                        "**告警描述**: %s \n\n" % output['annotations']['description'] +
                        "**告警状态**: %s \n\n" % output['status'] +
                        "**触发时间**: %s \n\n" % arrow.get(output['startsAt']).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss ZZ') +
                        "**触发结束时间**: %s \n" % arrow.get(output['endsAt']).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss ZZ')
            }
        }
        req = requests.post(url, json=send_data)
        result = req.json()
        if result['errcode'] != 0:
            print('notify dingtalk error: %s' % result['errcode'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8060)
