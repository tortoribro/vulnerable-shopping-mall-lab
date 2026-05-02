# UFW 방화벽 설정

## 목적

외부에서 Flask 5001번 포트에 직접 접근하지 못하게 하고, Apache 80번 포트만 접근하도록 제한하였다.

## 정책

| 포트 | 용도 | 정책 |
|---|---|---|
| 80/tcp | Apache HTTP | 허용 |
| 53 | DNS | 실습망에서 허용 |
| 5001/tcp | Flask 직접 접근 | 차단 |

## 명령어

```bash
allow = 허용
deny  = 차단
delete = 규칙 삭제
status numbered = 규칙 번호 확인
```
예시
```bash
sudo ufw allow 80/tcp
sudo ufw deny 5000/tcp
sudo ufw allow from 172.30.1.98 to any port 80 proto tcp # 특정 ip ,포트만 적용
```
기본 정책 확인

```bash
sudo ufw status verbose
```
방화벽 정책 설정
```bash
sudo ufw allow 80/tcp
sudo ufw allow 53
sudo ufw deny 5001/tcp
sudo ufw status numbered
```
### 방화벽 켜기
```bash
sudo ufw enable
```
### 방화벽 끄기
```bash
sudo ufw disable
```
### 방화벽 상태확인
```bash
sudo ufw status
```
### 방화벽 번호로규칙확인
```bash
sudo ufw status numbered
```
### 3번 규칙 삭제
```bash
sudo ufw delete 3
```

### ufw 로그 활성화
```bash
sudo ufw logging on
```
### 로그 확인:

```bash
sudo tail -f /var/log/ufw.log
sudo journalctl -k | grep UFW
```
`flask 로그: tail -f /var/www/shopping_mall/logs/security.log`

### 주의
`1. deny 규칙보다 allow 규칙 순서가 중요할 수 있음

UFW는 위에서 아래로 규칙을 본다.
그래서 특정 IP를 막고 싶은데 앞에 넓은 allow가 있으면 허용될 수 있다.`

예:

```bash
[ 1] 80/tcp ALLOW IN Anywhere
[ 2] 80/tcp DENY IN 172.30.1.50
## 이럴 땐 더 구체적인 deny를 위에 넣어야 한다.
sudo ufw insert 1 deny from 172.30.1.50 to any port 80 proto tcp
```

### 웹 테스트

```bash
curl -I http://172.30.1.94
curl -I http://www.shopping.host
```

## 보안 의미

Flask 애플리케이션은 외부에 직접 노출하지 않고 Apache Reverse Proxy를 통해서만 접근하도록 구성하였다.
