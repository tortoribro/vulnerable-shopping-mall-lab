# SQL Injection 분석

```text
 기초적인 공격,방어기법을 정리를 해보았다.
```

## 1. 개요

SQL Injection은 사용자 입력값이 SQL 쿼리에 직접 삽입될 때 발생하는 취약점이다. 공격자는 쿼리 구조를 조작하여 인증 우회, 데이터 조회, 데이터 변조 등을 수행할 수 있다.

## 2. 취약 위치

| 기능 | URL | 파라미터 |
|---|---|---|
| 로그인 | /login | username, password |
| 검색 | /search | q |

## 3. 로그인 우회 공격

### 페이로드

```text
admin' -- 
```
### 조작된 SQL
```SQL
SELECT * FROM users WHERE username='admin' -- ' AND password='anything'
```

### 결과

비밀번호 조건이 주석 처리되어 관리자 계정으로 로그인되었다.

## 4. 검색 SQL Injection

### 페이로드

```
' OR '1'='1
```

## 결과

검색 조건이 조작되어 의도하지 않은 상품 데이터가 조회되었다.

## 5. 로그 분석

Apache access.log에서 다음과 같은 요청이 확인되었다.

``` text
GET /search?q=%27%20OR%20%271%27%3D%271 HTTP/1.1
POST /login HTTP/1.1
```

Flask security.log에서는 다음과 같은 의심 패턴이 확인되었다.

``` text
path=/login form={'username': "admin' -- ", 'password': '***MASKED***'} suspicious=True
path=/search args={'q': "' OR '1'='1"} suspicious=True
```

## 6. 취약 원인
사용자 입력값을 SQL 문자열에 직접 연결하였다.

## 7. 대응 방안
Prepared Statement를 사용한다.

```Python
user = db.execute(
    "SELECT * FROM users WHERE username=? AND password=?",
    (username, password)
).fetchone()
```

## 8. 결론

SQL Injection을 통해 인증 우회가 가능함을 확인하였고, Prepared Statement 적용을 통해 쿼리 조작을 방지할 수 있음을 정리하였다.
