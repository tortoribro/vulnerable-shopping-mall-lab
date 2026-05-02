# Dns 관련 정리

# DNS
 - 도메인 이름을 ip주소로 바꿔주는 시스템

 ## 작동원리

 ```bash
사용자 PC
    ↓
로컬 DNS 캐시 확인
    ↓
hosts 파일 확인  # /etc/hosts
    ↓
설정된 DNS 서버에 질의 # /etc/resolv.conf
    ↓
Root DNS 서버
    ↓   #example.com은 어디?
TLD DNS 서버
    ↓
Authoritative DNS 서버
    ↓ #www.example.com의 IP는?
IP 주소 응답
    ↓ # x.x.x.x
브라우저가 해당 IP로 접속

 ```



 ## 예시
  - apache와 flask를 사용시
  - apache는 proxy 서버로 설정
  - 각 도메인 마다 어떤 웹페이지나 Flask 앱을 보여줄지 는 Apache가 결정한다.
 ```bash
도메인 이름
    ↓
DNS가 IP로 변환
    ↓
브라우저가 해당 IP로 접속
    ↓
Apache가 Host 이름을 보고 분기
    ↓
정적 페이지 또는 Flask 앱으로 연결 
 ```




 ## 간단한 DNS 서버 구축

 ### 설치

 ```bash
 sudo apt update
 sudo apt install dnsmasq dnsutils -y-y
 ```

 ### 설정파일

 `설정파일이름:lab-dns.conf`

 ```bash
 sudo nano /etc/dnsmasq.d/lab-dns.conf
```

### DNS 예시 설정

- 설정파일

```bash
# Lab DNS Server

listen-address=${DNS서버IP} #DNS 서버 IP
bind-interfaces

domain-needed

server=1.1.1.1
server=8.8.8.8

address=/shopping.host/${지정할IP} #ex) 웹서버,애플리케이션서버
address=/www.shopping.host/${지정할IP}
address=/admin.shopping.host/${지정할IP}
address=/shopping.test/${지정할IP}
address=/www.shopping.test/${지정할IP}
```
### 재시작
```bash
sudo systemctl restart dnsmasq
```

### 상태확인

```bash
sudo systemctl status dnsmasq --no-pager
```

### DNS 포트 확인:
```bash
sudo ss -tulnp | grep :53
```


# 호스트가 DNS 서버에 질의

### 네임서버 설정
 - DNS 서버에 질의
```bash
sudo nano /etc/resolv.conf #설정파일
```
### 맨위에 추가:
```bash
nameserver ${DNS서버Ip} #DNS 서버 등록
```

##### 로컬에서 사용하려면

`/etc/hosts` 파일에 ip , 도메인 등록
