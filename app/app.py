
from flask import Flask, render_template, request, redirect, session, g
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lumina.db"

app = Flask(__name__)
app.secret_key = "lumina-market-local-lab-secret"  # intentionally weak for lab


def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_db(reset=False):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if reset:
        cur.executescript("""
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS reviews;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS support_messages;
        """)

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        name TEXT,
        email TEXT,
        phone TEXT,
        address TEXT,
        role TEXT
    );

    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT,
        name TEXT,
        category TEXT,
        price INTEGER,
        sale_price INTEGER,
        rating REAL,
        stock INTEGER,
        description TEXT,
        detail TEXT,
        color_class TEXT
    );

    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        user_id INTEGER,
        username TEXT,
        rating INTEGER,
        content TEXT,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        order_no TEXT,
        item_summary TEXT,
        total_price INTEGER,
        receiver TEXT,
        address TEXT,
        status TEXT,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS support_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        email TEXT,
        message TEXT,
        created_at TEXT
    );
    """)

    has_products = cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if has_products == 0:
        users = [
            ("admin", "admin1234", "관리자", "admin@lumina.local", "010-0000-0000", "서울시 중구 루미나타워 20F", "admin"),
            ("jasmine", "pass1234", "정빈", "jasmine@example.local", "010-1111-2222", "서울시 마포구 테스트로 12", "user"),
            ("guest", "guest", "게스트", "guest@example.local", "010-3333-4444", "부산시 해운대구 데모로 45", "user"),
            ("minseo", "minseo123", "김민서", "minseo@example.local", "010-5555-6666", "경기도 성남시 샘플로 88", "user"),
        ]
        products = [
            ("LUM-BAG-001", "Aero Daily Backpack", "Bags", 89000, 69000, 4.8, 32, "노트북과 일상 소지품을 깔끔하게 수납하는 데일리 백팩", "생활 방수 원단, 15인치 노트북 수납, 캐리어 결합 밴드, 내부 포켓 8개 구성", "bag"),
            ("LUM-HOOD-002", "Soft Layer Hoodie", "Fashion", 72000, 59000, 4.7, 18, "부드러운 터치감의 사계절 후드티", "기모 없는 미드웨이트 원단, 여유 있는 핏, 변형이 적은 이중 봉제", "hoodie"),
            ("LUM-MUG-003", "Morning Glass Mug", "Kitchen", 22000, 16900, 4.6, 54, "매일 쓰기 좋은 내열 유리 머그", "450ml 대용량, 전자레인지 사용 가능, 손잡이 열전도 최소화 설계", "mug"),
            ("LUM-LAMP-004", "Calm Desk Lamp", "Life", 49000, 39900, 4.9, 21, "눈부심을 줄인 무드형 데스크 램프", "3단계 밝기 조절, USB-C 충전, 12시간 사용 가능한 배터리", "lamp"),
            ("LUM-SHOE-005", "Urban Walk Sneakers", "Fashion", 129000, 99000, 4.5, 12, "가볍고 안정적인 착화감의 데일리 스니커즈", "쿠션 인솔, 미끄럼 방지 아웃솔, 통기성 메쉬 구조", "shoes"),
            ("LUM-KEY-006", "Quiet Work Keyboard", "Tech", 99000, 79000, 4.8, 15, "조용한 타건감의 업무용 무선 키보드", "저소음 스위치, 멀티 페어링 3대, USB-C 충전, 2.4GHz 동글 지원", "keyboard"),
            ("LUM-WATCH-007", "Minimal Smart Watch", "Tech", 159000, 129000, 4.4, 9, "필수 기능에 집중한 미니멀 스마트워치", "걸음 수, 심박수, 알림, 수면 기록, 7일 배터리", "watch"),
            ("LUM-CANDLE-008", "Forest Mood Candle", "Life", 32000, 24900, 4.7, 40, "숲 향을 담은 소이 왁스 캔들", "천연 소이 왁스, 우드 심지, 약 42시간 연소", "candle"),
        ]
        cur.executemany("INSERT INTO users(username,password,name,email,phone,address,role) VALUES (?,?,?,?,?,?,?)", users)
        cur.executemany("INSERT INTO products(sku,name,category,price,sale_price,rating,stock,description,detail,color_class) VALUES (?,?,?,?,?,?,?,?,?,?)", products)
        reviews = [
            (1, 2, "jasmine", 5, "수납공간이 생각보다 넓고 마감이 좋아요.", "2026-04-21 10:15"),
            (1, 3, "guest", 4, "출퇴근용으로 무난합니다. 배송도 빨랐어요.", "2026-04-22 18:43"),
            (2, 4, "minseo", 5, "핏이 예쁘고 색감이 사진이랑 거의 같아요.", "2026-04-23 09:10"),
            (4, 2, "jasmine", 5, "책상 분위기가 확 좋아졌습니다.", "2026-04-24 21:08"),
        ]
        cur.executemany("INSERT INTO reviews(product_id,user_id,username,rating,content,created_at) VALUES (?,?,?,?,?,?)", reviews)
        orders = [
            (1, "LM-20260420-0001", "관리자 테스트 주문", 299000, "관리자", "서울시 중구 루미나타워 20F", "배송완료", "2026-04-20 11:30"),
            (2, "LM-20260422-0002", "Aero Daily Backpack 외 1건", 85900, "정빈", "서울시 마포구 테스트로 12", "배송중", "2026-04-22 15:20"),
            (3, "LM-20260423-0003", "Morning Glass Mug", 16900, "게스트", "부산시 해운대구 데모로 45", "결제완료", "2026-04-23 20:05"),
            (4, "LM-20260424-0004", "Soft Layer Hoodie", 59000, "김민서", "경기도 성남시 샘플로 88", "상품준비중", "2026-04-24 08:50"),
        ]
        cur.executemany("INSERT INTO orders(user_id,order_no,item_summary,total_price,receiver,address,status,created_at) VALUES (?,?,?,?,?,?,?,?)", orders)
    conn.commit()
    conn.close()


def current_user():
    if not session.get("user_id"):
        return None
    return db().execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()


@app.before_request
def boot():
    if not DB_PATH.exists():
        init_db()


@app.route("/")
def home():
    products = db().execute("SELECT * FROM products ORDER BY id LIMIT 8").fetchall()
    new_items = db().execute("SELECT * FROM products ORDER BY id DESC LIMIT 4").fetchall()
    return render_template("index.html", products=products, new_items=new_items, user=current_user())


@app.route("/category/<name>")
def category(name):
    products = db().execute("SELECT * FROM products WHERE category=? ORDER BY id", (name,)).fetchall()
    return render_template("category.html", name=name, products=products, user=current_user())


@app.route("/product/<int:product_id>")
def product(product_id):
    p = db().execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    reviews = db().execute("SELECT * FROM reviews WHERE product_id=? ORDER BY id DESC", (product_id,)).fetchall()
    return render_template("product.html", p=p, reviews=reviews, user=current_user())


@app.route("/review", methods=["POST"])
def review():
    # Vulnerability: Stored XSS + unsafe SQL string interpolation
    product_id = request.form.get("product_id", "1")
    rating = request.form.get("rating", "5")
    content = request.form.get("content", "")
    user_id = session.get("user_id", 3)
    username = session.get("username", "guest")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    sql = f"""
    INSERT INTO reviews(product_id, user_id, username, rating, content, created_at)
    VALUES ({product_id}, {user_id}, '{username}', {rating}, '{content}', '{created_at}')
    """
    db().execute(sql)
    db().commit()
    return redirect(f"/product/{product_id}")


@app.route("/search")
def search():
    # Vulnerability: Reflected XSS + SQL Injection
    q = request.args.get("q", "")
    sql = f"""
    SELECT * FROM products
    WHERE name LIKE '%{q}%'
       OR description LIKE '%{q}%'
       OR category LIKE '%{q}%'
    ORDER BY id DESC
    """
    error = None
    try:
        products = db().execute(sql).fetchall()
    except Exception as e:
        products = []
        error = str(e)
    return render_template("search.html", q=q, products=products, error=error, user=current_user())


@app.route("/login", methods=["GET", "POST"])
def login():
    # Vulnerability: SQL Injection login bypass + open redirect via next
    error = None
    next_url = request.args.get("next", "/")
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        next_url = request.form.get("next", "/")
        sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        try:
            row = db().execute(sql).fetchone()
        except Exception as e:
            row = None
            error = str(e)
        if row:
            session["user_id"] = row["id"]
            session["username"] = row["username"]
            session["role"] = row["role"]
            resp = redirect(next_url)
            resp.set_cookie("last_login_user", row["username"])
            return resp
        if not error:
            error = "아이디 또는 비밀번호를 확인해주세요."
    return render_template("login.html", error=error, next_url=next_url, user=current_user())


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/cart")
def cart():
    ids = session.get("cart", [])
    items = []
    total = 0
    for pid in ids:
        p = db().execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        if p:
            items.append(p)
            total += p["sale_price"]
    return render_template("cart.html", items=items, total=total, user=current_user())


@app.route("/cart/add")
def cart_add():
    # Vulnerability: CSRF because state-changing GET request
    product_id = request.args.get("product_id", "1")
    cart = session.get("cart", [])
    cart.append(product_id)
    session["cart"] = cart
    return redirect(request.args.get("next", "/cart"))


@app.route("/cart/clear")
def cart_clear():
    session["cart"] = []
    return redirect("/cart")


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    # Vulnerability: CSRF on order creation
    if "user_id" not in session:
        return redirect("/login?next=/checkout")
    user = current_user()
    ids = session.get("cart", [])
    items = []
    total = 0
    for pid in ids:
        p = db().execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        if p:
            items.append(p)
            total += p["sale_price"]
    if request.method == "POST":
        receiver = request.form.get("receiver", user["name"])
        address = request.form.get("address", user["address"])
        item_summary = ", ".join([i["name"] for i in items]) if items else "빈 주문"
        order_no = "LM-" + datetime.now().strftime("%Y%m%d-%H%M%S")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        db().execute("""
            INSERT INTO orders(user_id, order_no, item_summary, total_price, receiver, address, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (session["user_id"], order_no, item_summary, total, receiver, address, "결제완료", created_at))
        db().commit()
        session["cart"] = []
        return redirect("/orders")
    return render_template("checkout.html", items=items, total=total, user=user)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    # Vulnerability: CSRF on profile update
    if "user_id" not in session:
        return redirect("/login?next=/profile")
    user = current_user()
    if request.method == "POST":
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        address = request.form.get("address", "")
        db().execute("UPDATE users SET email=?, phone=?, address=? WHERE id=?", (email, phone, address, session["user_id"]))
        db().commit()
        return redirect("/profile")
    return render_template("profile.html", user=user)


@app.route("/orders")
def orders():
    # Vulnerability: IDOR
    if "user_id" not in session:
        return redirect("/login?next=/orders")
    selected_user_id = request.args.get("user_id", session["user_id"])
    rows = db().execute(f"SELECT * FROM orders WHERE user_id={selected_user_id} ORDER BY id DESC").fetchall()
    return render_template("orders.html", orders=rows, selected_user_id=selected_user_id, user=current_user())


@app.route("/support", methods=["GET", "POST"])
def support():
    # Vulnerability: stored XSS visible to admin
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        message = request.form.get("message", "")
        user_id = session.get("user_id", 0)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        db().execute("""
            INSERT INTO support_messages(user_id, name, email, message, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, name, email, message, created_at))
        db().commit()
        return render_template("support_done.html", user=current_user())
    return render_template("support.html", user=current_user())


@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return render_template("forbidden.html", user=current_user()), 403
    users = db().execute("SELECT id, username, name, email, role FROM users ORDER BY id").fetchall()
    messages = db().execute("SELECT * FROM support_messages ORDER BY id DESC").fetchall()
    orders = db().execute("SELECT * FROM orders ORDER BY id DESC LIMIT 12").fetchall()
    return render_template("admin.html", users=users, messages=messages, orders=orders, user=current_user())


@app.route("/promo")
def promo():
    # Vulnerability: Open Redirect
    next_url = request.args.get("next", "/")
    return redirect(next_url)


@app.route("/reset-lab-database")
def reset_lab_database():
    init_db(reset=True)
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001, debug=True)
