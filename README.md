# LUMINA Market - 취약 온라인 쇼핑몰 실습
This project is intentionally vulnerable and must only be used in an isolated local lab environment.
Do not deploy this application to the public internet.

본 프로젝트는 정보보호 학습을 위해 의도적으로 취약하게 만든 웹 애플리케이션입니다.
공인 IP, 클라우드 서버, 회사망, 학교망 등 외부 접근 가능한 환경에 배포하면 안 됩니다.

권장 구조:

```text
Ubuntu VM = 취약 쇼핑몰 서버
Kali VM   = 점검/공격 클라이언트
Network   = Host-only 또는 내부 네트워크
```

외부 공개 금지:

```text
공인 IP 서버, 클라우드 서버, 회사망, 학교망, 포트포워딩, DMZ
```
##  프로젝트 목적

- Flask 기반 웹 애플리케이션 구축
- Apache Reverse Proxy 구성
- DNS 서버 구성
- UFW 방화벽 정책 설정
- SQL Injection, XSS, CSRF, IDOR 취약점 재현
- Apache 로그 및 Flask 로그 기반 공격 흔적 분석
- 취약 코드와 안전한 코드 비교
- 포트폴리오용 보안 분석 보고서 작성


##  실습 환경

| 구분 | 내용 |
|---|---|
| 가상화 | Oracle VirtualBox |
| 서버 | Ubuntu Linux |
| 공격/점검 클라이언트 | Kali Linux |
| 웹 프레임워크 | Python Flask |
| 웹 서버 | Apache2 |
| 데이터베이스 | SQLite |
| DNS | dnsmasq |
| 방화벽 | UFW |
| 도메인 | www.shopping.host |


##  전체 아키텍처

```text
Kali Client
    |
    | DNS Query: www.shopping.host
    v
Ubuntu DNS Server dnsmasq
    |
    | A Record: www.shopping.host -> Ubuntu IP
    v
Kali Browser
    |
    | HTTP Request
    v
Ubuntu Apache2 Reverse Proxy
    |
    | ProxyPass
    v
Flask Shopping Mall App
    |
    v
SQLite Database
```
##  구현기능
 - 상품목록
 - 상품 상세 페이지
 - 검색 기능
 - 로그인
 - 장바구니
 - 주문 내역
 - 마이페이지
 - 고객센터 문의
 - 관리자 페이지

 ## 취약점 목록

| 취약점 | 위치 | 실습 |
|---|---|---|
| Stored XSS | 상품 후기 | `/product/1` 리뷰 입력 |
| Reflected XSS | 검색 | `/search?q=` |
| SQL Injection | 로그인 | `/login` |
| SQL Injection | 검색 | `/search?q=` |
| CSRF | 장바구니 | `/cart/add?product_id=1` |
| CSRF | 프로필 수정 | `/profile` |
| CSRF | 주문 생성 | `/checkout` |
| IDOR | 주문 내역 | `/orders?user_id=1` |
| Stored XSS | 고객 문의 → 관리자 | `/support`, `/admin` |
| Open Redirect | 이벤트 이동 | `/promo?next=` |

## 7. 프로젝트 디렉토리 구조

```
vulnerable-shopping-mall-lab/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── app/
│   ├── app.py
│   ├── templates/
│   ├── static/
│   └── database/
│
├── apache/
│   ├── shopping.local.conf
│   └── reverse-proxy.md
│
├── dns/
│   ├── lab-dns.conf
│   └── dnsmasq-setup.md
│
├── firewall/
│   └── ufw-rules.md
│
├── attacks/
│   ├── sql-injection.md
│   ├── xss.md
│   ├── csrf.md
│   └── idor.md
│
├── logs-analysis/
│   ├── apache-log-analysis.md
│   ├── flask-security-log-analysis.md
│   └── sample-logs.md
│
├── docs/
│   ├── environment.md
│   ├── architecture.md
│   ├── troubleshooting.md
│   └── report.md
│
└── images/
    ├── main-page.png
    ├── login-sqli.png
    ├── xss-result.png
    ├── csrf-result.png
    ├── dns-test.png
    ├── apache-log.png
    └── ufw-status.png
```


## 8. 실행방법
### 8.1 패키지 설치
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv unzip -y
```
```bash
unzip lumina_vuln_shop.zip
cd lumina_vuln_shop
```
### 8.2 Flask 애플리케이션 실행
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
### 8.2 Flask 직접 접속:
 ```text
  http://127.0.0.1:5001
 ```

### 8.3 Apache Reverse Proxy 접속
Apache를 Reverse Proxy로 구성하면 다음 주소로 접속할 수 있습니다.

``` bash
 http://www.shopping.host
```
Apache는 80번 포트에서 요청을 받고, 내부 Flask 애플리케이션으로 요청을 전달합니다.

```bash
Apache 80/tcp -> Flask 127.0.0.1:5001
```

## 9. Apache Reverse Proxy 설정

`Apache 설치`
```bash
sudo apt update
sudo apt install apache2 -y
```
Apache 프록시 모듈 활성화:
```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2
```
VirtualHost 설정 (예시):
`설정파일: shopping.host.conf`
`경로:/etc/apache2/sites-available/shopping.host.conf`
```apache

<VirtualHost *:80>
    ServerName shopping.host
    ServerAlias www.shopping.host

    ProxyPreserveHost On

    ProxyPass / http://127.0.0.1:5001/
    ProxyPassReverse / http://127.0.0.1:5001/

    ErrorLog ${APACHE_LOG_DIR}/shopping_mall_error.log
    CustomLog ${APACHE_LOG_DIR}/shopping_mall_access.log combined
</VirtualHost>
```
사이트 활성화
```bash
sudo a2ensite shopping.host.conf
```
설정 검사:
```Bash
sudo apache2ctl configtest
sudo apache2ctl -S
sudo systemctl restart apache2
```

## 10.DNS서버 구성

kali Linux 가상환경을 사용하여 DNS서버를 구축하였습니다.

설치
```bash
 sudo apt update
 sudo apt install dnsmasq dnsutils -y-y
 ```

예시 설정 파일:
`설정파일이름:lab-dns.conf`
`경로:/etc/dnsmasq.d/lab-dns.conf`
```conf
listen-address=Kali_IP #DNS 서버 주소
bind-interfaces

server=1.1.1.1
server=8.8.8.8

address=/shopping.host/Ubuntu_IP #웹서버 주소
address=/www.shopping.host/Ubuntu_IP
address=/admin.shopping.host/Ubuntu_IP

```

DNS 서버 재시작:

```Bash
sudo systemctl restart dnsmasq
sudo systemctl status dnsmasq --no-pager
```
DNS 질의 테스트:

```Bash
dig @Kali_IP www.shopping.host
nslookup www.shopping.host Kali_IP
```

호스트환경에서 DNS 서버를 사용하도록 설정 (클라이언트 컴퓨터에서 설정):
`경로:/etc/resolv.conf`
```bash
nameserver Kali_IP # DNS서버로 질의
```

## 11. UFW 방화벽 정책
Reverse Proxy 구조에서는 외부에서 Apache 80번 포트만 접근하도록 구성합니다.

포트 |용도|	정책
|---|---|---|
80/tcp|	Apache HTTP	|허용
53|	DNS	|실습망에서 허용
5001/tcp|	Flask 직접 접근	|차단

명령어:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 53
sudo ufw deny 5001/tcp
sudo ufw status numbered
```
보안 목적:

```bash
외부/Kali -> Apache 80번 접근
Apache -> 내부 Flask 127.0.0.1:5001 접근
외부/Kali -> Flask 5001번 직접 접근 차단
```

--- 각종공격들 추가예정

## 13 로그분석
13.1 Apache Access Log
로그 위치:

```bash
 /var/log/apache2/shopping_mall_access.log
```
실시간확인:

```bash
sudo tail -f /var/log/apache2/shopping_mall_access.log
```
SQL Injection 의심 요청 검색:

```bash
sudo grep -Ei "('|--|union|select|or|1=1)" /var/log/apache2/shopping_mall_access.log
```

특정 경로 검색:
```bash
sudo grep "/login" /var/log/apache2/shopping_mall_access.log
sudo grep "/search" /var/log/apache2/shopping_mall_access.log
```

13.2 Apache Error Log

로그 위치:

```bash
/var/log/apache2/shopping_mall_error.log
```
확인:

```bash
sudo tail -f /var/log/apache2/shopping_mall_error.log
```

13.3 Flask Security Log

Flask에서 별도 보안 로그를 구성한 경우:

```bash
logs/security.log
```
확인:

```bash
tail -f logs/security.log
```
예시 로그:

```bash
ip=192.168.0.40 method=POST path=/login form={'username': "admin' -- ", 'password': '***MASKED***'} suspicious=True
ip=192.168.0.40 method=GET path=/search args={'q': "' OR '1'='1"} suspicious=True
```

분석 포인트:

```bash
공격자 IP
요청 메서드
요청 경로
파라미터
페이로드
User-Agent
의심 여부
```
## 14.주요 점검 명령어

Apache

```bash
sudo systemctl status apache2 --no-pager
sudo apache2ctl configtest
sudo apache2ctl -S
sudo tail -f /var/log/apache2/shopping_mall_access.log
```
Flask
```Bash
cd /var/www/shopping_mall
source venv/bin/activate
python app.py
curl -I http://127.0.0.1:5000
```
DNS

```bash
sudo systemctl status dnsmasq --no-pager
sudo ss -tulnp | grep :53
dig @Ubuntu_IP www.shopping.host
nslookup www.shopping.host Ubuntu_IP
```
UFW
```bash
sudo ufw status numbered
sudo ufw allow 80/tcp
sudo ufw allow 53
sudo ufw deny 5000/tcp
```

## 15. 보안 대응 방안
|취약점	|대응 방안|
|--|--|
SQL Injection|	Prepared Statement 사용
XSS	HTML |Escaping, CSP, 입력값 검증
CSRF|	CSRF Token, SameSite Cookie
IDOR|	객체 단위 권한 검증
Open Redirect|	허용 도메인 검증
로그 분석|	Apache/Flask 로그 수집 및 의심 패턴 탐지
포트 노출|	UFW로 5000번 직접 접근 차단
운영 구조|	Apache Reverse Proxy 적용


## 16. 프로젝트를 통해 학습한 내용

본 프로젝트를 통해 다음 내용을 학습했습니다.

- Flask 웹 애플리케이션 구조
- Apache VirtualHost 설정
- Apache Reverse Proxy 구성
- 내부 DNS 서버 구축
- UFW 방화벽 정책 설정
- SQL Injection 공격 원리
- XSS 공격 원리
- CSRF 공격 원리
- IDOR 취약점 원리
- Apache access.log 분석
- Flask 애플리케이션 로그 분석
- 취약 코드와 안전 코드 비교
- 실습 결과를 보고서화하는 방법


17. 향후 개선 방향

향후 다음 기능을 추가하여 프로젝트를 확장할 수 있습니다.

- 로그인 실패 횟수 제한
- 비밀번호 해시 저장
- CSRF Token 적용
- 보안 헤더 적용
- HTTPS 구성
- ModSecurity WAF 연동
- Fail2ban 연동
- Suricata 또는 Wazuh 연동
- Docker 기반 배포 환경 구성
- 취약 버전과 보안 패치 버전 비교
