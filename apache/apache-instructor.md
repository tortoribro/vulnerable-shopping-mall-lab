# Apache 관련 정리

## Apache 설치

```bash
sudo apt update
sudo apt install apache2 -y
```

### 1. Apache 상태 확인

```bash
sudo systemctl status apache2 --no-pager
```
 정상이면
 ```bash
  active (running)
 ```
### Apache 시작
```bash
sudo systemctl start apache2
```

### Apache 중지
```bash
sudo systemctl stop apache2
```
### Apache 재시작
```bash
sudo systemctl restart apache2
```
### 설정만 다시 불러오기
```bash
sudo systemctl reload apache2
```
### 부팅 시 자동 실행
```bash
sudo systemctl enable apache2
```
### 자동 실행 해제
```bash
sudo systemctl disable apache2
```
## 2. Apache 설정 검사 명령어

### `Apache 설정 수정 후 반드시 확인해야한다.`
```bash
sudo apache2ctl configtest
```
- 정상이면:
``` bash
Syntax OK
```
### 현재 Apache 가상호스트 구조 확인:
    - 이 명령이 매우 중요하다, 어떤 도메인이 어떤 conf파일에 연결됐는지 보여준다.
```bash
sudo apache2ctl -S
```
- 예상 예시
```bash
*:80    www.shopping.host (/etc/apache2/sites-enabled/shopping.local.conf:1)
        alias shopping.host
```
### 활성화된 모듈 확인:

```bash
apache2ctl -M
```

### 프록시 모듈만 확인:
``` bash
apache2ctl -M | grep proxy
```
- 정상이면

```bash
proxy_module
proxy_http_module
```

## 3. Apache 사이트 설정 파일 위치

### `Apache 사이트 설정은 보통 두 군데로 나뉜다.`

### 사용 가능한 설정 파일들이 있는 곳.

```bash
/etc/apache2/sites-available/
```
### 실제로 활성화된 설정 파일 링크가 있는 곳.

```bash
/etc/apache2/sites-enabled/
```
 - 설정파일 이름 :`shopping.local.conf`
 - 경로:`/etc/apache2/sites-available/shopping.local.conf`

### 설정파일 열기:
```bash
sudo nano /etc/apache2/sites-available/shopping.local.conf
```

### 활성화된 사이트 확인:

```bash
ls -l /etc/apache2/sites-enabled/
```
## 4. 사이트 활성화/비활성화

### 쇼핑몰 사이트 활성화
```bash
sudo a2ensite shopping.host.conf
```
### 쇼핑몰 사이트 비활성화
```bash
sudo a2dissite shopping.local.conf
```
### 기본 Apache 사이트 활성화
```bash
sudo a2ensite 000-default.conf
```
### 기본 Apache 사이트 비활성화
```bash
sudo a2dissite 000-default.conf
```
- 설정적용
```bash
sudo systemctl reload apache2
```
- 또는
```bash
sudo systemctl restart apache2
```

## 5. 정적 HTML 사이트용 Apache 설정
`/var/www/shopping_mall/index.html을 Apache가 직접 보여주는 구조다.`

``` apache
<VirtualHost *:80>
    ServerName shopping.host
    ServerAlias www.shopping.host

    DocumentRoot /var/www/shopping_mall

    ErrorLog ${APACHE_LOG_DIR}/shopping_mall_error.log
    CustomLog ${APACHE_LOG_DIR}/shopping_mall_access.log combined

    <Directory /var/www/shopping_mall>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```
- 핵심설정
``` apache
ServerName shopping.host
ServerAlias www.shopping.host
DocumentRoot /var/www/shopping_mall
```
- 의미:

설정|의미
|--|--|
ServerName	|대표 도메인
ServerAlias|	추가 도메인
DocumentRoot|	웹 파일이 있는 디렉토리
ErrorLog	|에러 로그 위치
CustomLog|	접속 로그 위치
Directory|	해당 폴더 접근 권한

## 6. Flask Reverse Prox
Flask 쇼핑몰을 Apache 뒤에 연결하는 구조
```bash
사용자 → Apache 80번 → Flask 127.0.0.1:5001
```
### 설정 파일:
```bash
sudo nano /etc/apache2/sites-available/shopping.host.conf
```
### 내용
```bash
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
### 핵심
```bash
ProxyPass / http://127.0.0.1:5001/
ProxyPassReverse / http://127.0.0.1:5001/
```
### 의미
```bash
http://www.shopping.host/login
↓
Apache
↓
http://127.0.0.1:5000/login
```
## 7. 7. Apache 프록시 모듈 명령어

`Flask Reverse Proxy를 쓰려면 필요하다.`

### 활성화
```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2
```
### 확인
```bash
apache2ctl -M | grep proxy
```
### 비활성화
```bash
sudo a2dismod proxy
sudo a2dismod proxy_http
sudo systemctl restart apache2
```

## 8. 웹 디렉토리 관련 명령어

### 디렉토리 만들기
```bash
sudo mkdir -p /var/www/shopping_mall
```
### 파일 목록 확인
```bash
ls -l /var/www/shopping_mall
```

### 테스트  index.html 만들기
```bash
echo "<h1>Shopping Mall OK</h1>" | sudo tee /var/www/shopping_mall/index.html
```

### 파일 권한 설정

```bash
sudo chown -R www-data:www-data /var/www/shopping_mall
sudo chmod -R 755 /var/www/shopping_mall
```
`www-data는 Apache가 사용하는 기본 계정`

## 9. 로그 확인 명령어
### 쇼핑물 접속 로그
```bash
sudo tail -f /var/log/apache2/shopping_mall_access.log
```
### 쇼핑몰 에러 로그
```bash
sudo tail -f /var/log/apache2/shopping_mall_error.log
```
### 최근 50줄만 보기
```bash
sudo tail -n 50 /var/log/apache2/error.log
```

### 특정 IP 검색
```bash
sudo grep "192.168.0.40" /var/log/apache2/shopping_mall_access.log
```

### SQL Injection 의심 문자열 검색
```bash
sudo grep -Ei "('|--|union|select|or|1=1)" /var/log/apache2/shopping_mall_access.log
```

### 특정 경로 검색
```bash
sudo grep "/login" /var/log/apache2/shopping_mall_access.log
```

```bash
sudo grep "/search" /var/log/apache2/shopping_mall_access.log
```

## 10. 접속 테스트 명령어

### localhost 접속확인
```bash
curl -I http://localhost
```

### 도메인 접속 확인

```bash
curl -I http://www.shopping.host
```
### 특정 Host 헤더로 가상호스트 확인
`이건 host/DNS 없이도 Apach vhost를 테스트 할 수 있어서 중요하다`

```bash
curl -I http://127.0.0.1 -H "Host: www.shopping.host"
```
정상이면
```bash
HTTP/1.1 200 OK
```
## Flash 직접확인
```bash
curl -I http://127.0.0.1:5000
```

## 11. 자주 쓰는 Apache 파일 경로
- Apache 전체 기본 설정.
```bash
/etc/apache2/apache2.conf
```
- Apache가 어떤 포트를 들을지 설정.
```bash
/etc/apache2/ports.conf
```
- 사용 가능한 사이트 설정.
```bash
/etc/apache2/sites-available/
```
- 활성화된 사이트 설정.
```bash
/etc/apache2/sites-enabled/
```
- Apache 기본 웹 루트.
```bash
/var/www/html
```
- 쇼핑몰 프로젝트/웹 루트.
```bash
/var/www/shopping_mall
```

- 기본 접속 로그.
```bash
/var/log/apache2/access.log
```

- 기본 에러 로그.

```bash
/var/log/apache2/error.log
```

- 쇼핑몰 접속 로그.

```bash
/var/log/apache2/shopping_mall_access.log
```

- 쇼핑몰 에러 로그.

```bash
/var/log/apache2/shopping_mall_error.log
```
## 12. 자주 나는 오류와 해결
증상| 원인 |해결
|--|--|--|
server not found	|도메인 해석 실패	|/etc/hosts 또는 DNS 확인
Apache 기본 페이지가 뜸|	vhost 적용 안 됨|	sudo apache2ctl -S 확인
403 Forbidden	|디렉토리 권한 문제	|chown, chmod, Directory 확인
404 Not Found	|파일 없음 또는 경로 문제	|DocumentRoot, index.html 확인
503 Service Unavailable	|Flask 꺼짐|	python app.py 또는 systemd 서비스 시작
502 Proxy Error	ProxyPass| 주소/포트 문제|	curl http://127.0.0.1:5001 확인
CSS 깨짐	|static 경로 문제	|Flask static 경로/프록시 확인
Syntax Error|	conf 문법 오류	|sudo apache2ctl configtest 확인
www만 안 됨|	ServerAlias 없음|	ServerAlias www.shopping.host 추가

## 최종 apache 설정

```bash
<VirtualHost *:80>
    ServerName shopping.host
    ServerAlias www.shopping.host

    ProxyPreserveHost On

    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/

    ErrorLog ${APACHE_LOG_DIR}/shopping_mall_error.log
    CustomLog ${APACHE_LOG_DIR}/shopping_mall_access.log combined
</VirtualHost>
```
설정 적용 전체 명령어

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2ensite shopping.local.conf
sudo a2dissite 000-default.conf
sudo apache2ctl configtest
sudo systemctl restart apache2
```
