# 내부 DNS 서버 구성

## 목적

Kali에서 hosts 파일을 수정하지 않고 www.shopping.host 도메인으로 쇼핑몰 웹서버에 접근하기 위해 Ubuntu에 dnsmasq 기반 내부 DNS 서버를 구성하였다.

## 설정 파일

`/etc/dnsmasq.d/lab-dns.conf`

```conf
listen-address=Ubuntu_IP
bind-interfaces

server=1.1.1.1
server=8.8.8.8

address=/shopping.host/Ubuntu_IP
address=/www.shopping.host/Ubuntu_IP
address=/admin.shopping.host/Ubuntu_IP

```

### 검증 명령어

```Bash
dig @Ubuntu_IP www.shopping.host
nslookup www.shopping.host Ubuntu_IP
```


Kali에서 Ubuntu DNS 서버를 사용하도록 설정:

```Bash
sudo nano /etc/resolv.conf
```
```bash
nameserver Ubuntu_IP # 우분투 DNS서버로 질의
```

## 결과

www.shopping.host가
 Ubuntu 웹서버 IP로 정상 해석됨을 확인하였다.