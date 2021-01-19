### 依赖环境
- python2
- alertmanager==0.21.0

### 安装依赖包

```
$ pip install -r requirements.txt

```

### 运行

1. linux
```
python main.py
```
监听8060端口

### alertmanager配置
```
$ vim alertmanager.yml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 24h
  #repeat_interval: 3m
  receiver: 'web.hook'
  routes:
  - receiver: 'web.dingding'
    match:
      severity: critical
receivers:
- name: 'web.hook'
  webhook_configs:
  - url: 'http://127.0.0.1:5001/'
- name: 'web.dingding'
  webhook_configs:
  - url: 'http://localhost:8060/'
    send_resolved: true
```
