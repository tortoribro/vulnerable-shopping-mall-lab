# Apache Reverse Proxy 구성

## 목적

사용자가 `http://www.shopping.host`로 접속하면 Apache가 80번 포트에서 요청을 받고, 내부 Flask 애플리케이션 `127.0.0.1:5001`으로 전달하도록 구성하였다.

## 활성화 모듈

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2
```

## VirtualHost 설정 
 
 - 경로: `/etc/apache2/sites-available/shopping.host.conf`


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
## 적용
```bash
sudo a2ensite shopping.host.conf
```
## 검증
```Bash
sudo apache2ctl configtest
sudo apache2ctl -S
curl -I http://www.shopping.host
```
## 결과

브라우저에서 포트 번호 없이 http://www.shopping.host로 Flask 쇼핑몰에 접속할 수 있음을 확인하였다.