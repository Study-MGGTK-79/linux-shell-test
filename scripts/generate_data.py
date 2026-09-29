#!/usr/bin/env python3
"""
Генератор наборов данных для практической работы по Linux Shell.
Все данные генерируются детерминированно с фиксированным seed=42.
"""

import os
import random
import shutil

random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROJECT_DIR = os.path.join(BASE_DIR, "project")

os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------------------------------------------
# TASK 1: data/server.log
# 35,000 строк. Ровно 3,421 запросов со статусом 404.
# ---------------------------------------------------------
print("[1/5] Генерация data/server.log...")
TOTAL_SERVER_LOGS = 35000
TARGET_404_COUNT = 3421

ip_pool = [f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}" for _ in range(300)] + \
          [f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}" for _ in range(300)] + \
          [f"172.16.{random.randint(1, 254)}.{random.randint(1, 254)}" for _ in range(200)] + \
          [f"203.0.113.{random.randint(1, 254)}" for _ in range(100)] + \
          [f"198.51.100.{random.randint(1, 254)}" for _ in range(100)]

urls_200 = [
    "/index.html", "/about.html", "/contact.html", "/services.html",
    "/api/v1/products", "/api/v1/users", "/api/v1/orders", "/api/v1/cart",
    "/static/css/styles.css", "/static/css/theme.css", "/static/js/app.js",
    "/static/js/vendor.js", "/assets/images/logo.png", "/assets/images/banner.jpg",
    "/favicon.ico", "/robots.txt", "/sitemap.xml", "/docs/overview",
    "/help/faq", "/catalog/category/electronics", "/catalog/category/furniture"
]

urls_404 = [
    "/old-index.html", "/missing.png", "/wp-login.php", "/administrator/index.php",
    "/phpmyadmin/index.php", "/api/v2/deprecated", "/backup.tar.gz", "/dump.sql",
    "/temp.txt", "/test.php", "/hidden/admin", "/config.json.bak",
    "/assets/images/old-logo.svg", "/downloads/report-2022.pdf", "/debug/vars",
    "/cgi-bin/test.cgi", "/.git/config", "/.env", "/v1/old-endpoint"
]

other_urls = [
    "/login", "/logout", "/checkout", "/register", "/search?q=test",
    "/api/v1/auth", "/download/manual.pdf", "/api/v1/upload"
]

statuses = [404] * TARGET_404_COUNT
other_statuses = [200] * 24000 + [201] * 800 + [301] * 1200 + [302] * 1500 + [304] * 2000 + [400] * 500 + [401] * 600 + [403] * 500 + [500] * 350 + [502] * 129
needed_others = TOTAL_SERVER_LOGS - TARGET_404_COUNT
statuses.extend(random.choices(other_statuses, k=needed_others))
random.shuffle(statuses)

server_log_lines = []
day = 28
month_str = "Sep"
year = 2026

sec_counter = 0
for status in statuses:
    ip = random.choice(ip_pool)
    hour = (sec_counter // 3600) % 24
    minute = (sec_counter // 60) % 60
    second = sec_counter % 60
    sec_counter += random.choice([0, 1, 2])
    timestamp = f"{day:02d}/{month_str}/{year}:{hour:02d}:{minute:02d}:{second:02d} +0300"
    
    if status == 404:
        method = "GET"
        url = random.choice(urls_404)
        size = random.choice([s for s in range(150, 350) if s != 404])
    elif status == 200:
        method = random.choice(["GET", "GET", "GET", "POST", "HEAD"])
        url = random.choice(urls_200)
        size = random.choice([s for s in range(500, 25000) if s != 404])
    elif status in (301, 302, 304):
        method = "GET"
        url = random.choice(other_urls)
        size = 0 if status == 304 else random.choice([120, 180, 240])
    elif status in (401, 403, 400):
        method = random.choice(["GET", "POST"])
        url = random.choice(other_urls)
        size = random.choice([180, 220, 290])
    else:
        method = random.choice(["GET", "POST"])
        url = random.choice(urls_200)
        size = random.choice([320, 540, 610])
        
    line = f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status} {size}'
    server_log_lines.append(line)

with open(os.path.join(DATA_DIR, "server.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(server_log_lines) + "\n")

print(f"  OK: 35000 строк создано (код 404: {TARGET_404_COUNT})")


# ---------------------------------------------------------
# TASK 2: data/logins.txt
# 25,000 строк. Топ: m_ivanov (1,582). Второе место: alex_k (1,340).
# ---------------------------------------------------------
print("[2/5] Генерация data/logins.txt...")
TOTAL_LOGINS = 25000
TOP_USER = "m_ivanov"
TOP_USER_COUNT = 1582
RUNNER_UP_USER = "alex_k"
RUNNER_UP_COUNT = 1340

other_users = [
    "anna_m", "k_petrov", "elena_v", "d_sidorov", "v_smirnov", "olga_p",
    "dmitry_s", "natalia_k", "sergey_b", "maria_t", "artem_f", "yulia_n",
    "igor_v", "tatiana_m", "maxim_g", "ekaterina_s", "roman_k", "svetl_m",
    "denis_l", "polina_v", "andrey_k", "marina_z", "nikita_r", "ksenia_b",
    "valery_p", "alina_t", "timur_k", "daria_f", "vlad_m", "irina_s",
    "evgeny_v", "sofia_l", "pavel_k", "anastasia_r", "gleb_s", "veronica_m",
    "kirill_t", "victoria_k", "stanislav_p", "yana_g", "stepan_b", "olesya_k",
    "danil_m", "lyubov_v", "ilya_f", "nadezhda_s", "egor_k", "larisa_t",
    "vadim_s", "zhanna_p", "boris_k", "tamara_v", "mikhail_z", "galina_m",
    "anton_k", "dina_s", "fedor_b", "guest_user", "service_acc", "deployer"
]

login_entries = [TOP_USER] * TOP_USER_COUNT
login_entries.extend([RUNNER_UP_USER] * RUNNER_UP_COUNT)

remaining_count = TOTAL_LOGINS - (TOP_USER_COUNT + RUNNER_UP_COUNT)
weights = [random.randint(10, 100) for _ in other_users]
total_w = sum(weights)
for u, w in zip(other_users, weights):
    cnt = int(remaining_count * (w / total_w))
    cnt = min(cnt, RUNNER_UP_COUNT - 100)
    login_entries.extend([u] * cnt)

while len(login_entries) < TOTAL_LOGINS:
    login_entries.append(random.choice(other_users))
while len(login_entries) > TOTAL_LOGINS:
    login_entries.pop()

random.shuffle(login_entries)

with open(os.path.join(DATA_DIR, "logins.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(login_entries) + "\n")

print(f"  OK: 25000 строк создано (топ: {TOP_USER} -> {TOP_USER_COUNT})")


# ---------------------------------------------------------
# TASK 3: data/products.csv
# 10,000 товаров. Максимальная цена: SKU-58421 (499990).
# Второе место: 489500.
# ---------------------------------------------------------
print("[3/5] Генерация data/products.csv...")
TOTAL_PRODUCTS = 10000
MAX_PRICE_SKU = "SKU-58421"
MAX_PRICE = 499990
RUNNER_UP_MAX_PRICE = 489500

categories = [
    "Electronics", "Computers", "Peripherals", "Audio", "Furniture",
    "Accessories", "Networking", "Storage", "Office"
]

adjectives = ["Wireless", "Mechanical", "Ergonomic", "Ultra HD", "Pro", "Gaming",
              "Portable", "Smart", "Compact", "Heavy-Duty", "Silent", "Fast"]
item_types = ["Keyboard", "Mouse", "Monitor 27\"", "Monitor 34\"", "Headset", "Desk Lamp",
              "Standing Desk", "Office Chair", "External SSD 1TB", "External SSD 2TB",
              "USB-C Hub", "Router AX3000", "Microphone", "Webcam 4K", "Docking Station",
              "Flash Drive 128GB", "Cable Organizer", "Power Bank 20000mAh", "Graphics Tablet"]

products = []
products.append((MAX_PRICE_SKU, "Enterprise Server Rack 42U", "Computers", MAX_PRICE))
products.append(("SKU-10001", "Precision Laser Workstation", "Computers", RUNNER_UP_MAX_PRICE))

sku_counter = 10002
for _ in range(TOTAL_PRODUCTS - 2):
    sku = f"SKU-{sku_counter}"
    sku_counter += 1
    cat = random.choice(categories)
    name = f"{random.choice(adjectives)} {random.choice(item_types)}"
    price = random.randint(150, RUNNER_UP_MAX_PRICE - 100)
    products.append((sku, name, cat, price))

random.shuffle(products)

with open(os.path.join(DATA_DIR, "products.csv"), "w", encoding="utf-8") as f:
    f.write("SKU,Name,Category,Price\n")
    for sku, name, cat, price in products:
        f.write(f"{sku},{name},{cat},{price}\n")

print(f"  OK: 10000 товаров создано (макс SKU: {MAX_PRICE_SKU} с ценой {MAX_PRICE})")


# ---------------------------------------------------------
# TASK 4: project/ дерево каталогов
# ~330 файлов, ровно 37 обычных файлов .conf
# ---------------------------------------------------------
print("[4/5] Генерация дерева project/...")
if os.path.exists(PROJECT_DIR):
    shutil.rmtree(PROJECT_DIR)
os.makedirs(PROJECT_DIR, exist_ok=True)

subdirs = [
    "apps/api/controllers", "apps/api/models", "apps/api/services", "apps/api/config",
    "apps/web/src/components", "apps/web/src/styles", "apps/web/public",
    "apps/worker/jobs", "apps/worker/queues", "apps/worker/config",
    "common/auth", "common/database", "common/logging", "common/utils",
    "config/environments", "config/ssl", "config/templates",
    "deploy/docker", "deploy/helm", "deploy/k8s", "deploy/terraform",
    "docs/api", "docs/architecture", "docs/guides",
    "infra/ansible/roles", "infra/ansible/playbooks", "infra/monitoring/grafana",
    "infra/monitoring/prometheus", "infra/nginx", "infra/nginx/sites-available",
    "modules/billing/services", "modules/billing/handlers",
    "modules/notifications/providers", "modules/reports/generators",
    "scripts/db", "scripts/maintenance", "scripts/ci",
    "tests/e2e", "tests/integration", "tests/unit"
]

for sd in subdirs:
    os.makedirs(os.path.join(PROJECT_DIR, sd), exist_ok=True)

os.makedirs(os.path.join(PROJECT_DIR, "infra/nginx/vhosts.conf"), exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "common/legacy.conf"), exist_ok=True)

with open(os.path.join(PROJECT_DIR, "infra/nginx/vhosts.conf", "README.txt"), "w") as f:
    f.write("Virtual host definitions directory\n")
with open(os.path.join(PROJECT_DIR, "common/legacy.conf", "notes.md"), "w") as f:
    f.write("Legacy notes\n")

conf_locations = [
    "apps/api/config/api.conf",
    "apps/api/config/security.conf",
    "apps/api/config/jwt.conf",
    "apps/worker/config/worker.conf",
    "apps/worker/config/queues.conf",
    "apps/worker/config/redis.conf",
    "common/database/db.conf",
    "common/database/pool.conf",
    "common/database/replica.conf",
    "common/logging/logger.conf",
    "common/logging/rotation.conf",
    "config/environments/development.conf",
    "config/environments/staging.conf",
    "config/environments/production.conf",
    "config/environments/testing.conf",
    "config/ssl/tls.conf",
    "config/templates/base.conf",
    "deploy/docker/daemon.conf",
    "deploy/docker/sysctl.conf",
    "deploy/k8s/coredns.conf",
    "infra/monitoring/grafana/grafana.conf",
    "infra/monitoring/prometheus/prometheus.conf",
    "infra/monitoring/prometheus/alerts.conf",
    "infra/nginx/nginx.conf",
    "infra/nginx/fastcgi.conf",
    "infra/nginx/proxy.conf",
    "infra/nginx/sites-available/default.conf",
    "infra/nginx/sites-available/app.conf",
    "infra/nginx/sites-available/metrics.conf",
    "modules/billing/services/payment.conf",
    "modules/notifications/providers/smtp.conf",
    "modules/notifications/providers/sms.conf",
    "modules/reports/generators/export.conf",
    "scripts/db/backup.conf",
    "scripts/maintenance/cleanup.conf",
    "app.conf",
    "sys.conf"
]

for loc in conf_locations:
    full_path = os.path.join(PROJECT_DIR, loc)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(f"# Configuration file: {os.path.basename(loc)}\nenabled = true\nworkers = 4\ntimeout = 30\n")

other_file_types = [
    (".py", "#!/usr/bin/env python3\npass\n"),
    (".js", "// JavaScript source code\nexport default {};\n"),
    (".ts", "// TypeScript module\nexport interface Config { id: string; }\n"),
    (".json", '{\n  "version": "1.0.0",\n  "status": "ok"\n}\n'),
    (".yaml", "version: '3.8'\nservices:\n  app:\n    image: app:latest\n"),
    (".yml", "name: CI Pipeline\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n"),
    (".md", "# Documentation\nDetails regarding the subsystem.\n"),
    (".sql", "CREATE TABLE IF NOT EXISTS audit_logs (id SERIAL PRIMARY KEY);\n"),
    (".sh", "#!/bin/bash\nset -euo pipefail\necho 'Running task...'\n"),
    (".txt", "General text notes and references.\n"),
    (".conf.bak", "# Backup configuration file\n"),
    (".conf.old", "# Old configuration\n"),
    (".conf.tmp", "# Temporary config\n"),
    (".config", "# Alternate config format\n")
]

for sd in subdirs:
    num_files = random.randint(5, 9)
    for i in range(num_files):
        ext, content = random.choice(other_file_types)
        filename = f"item_{i}_{random.randint(100, 999)}{ext}"
        filepath = os.path.join(PROJECT_DIR, sd, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

with open(os.path.join(PROJECT_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write("# Project Core\nEnterprise microservice framework.\n")
with open(os.path.join(PROJECT_DIR, "main.py"), "w", encoding="utf-8") as f:
    f.write("#!/usr/bin/env python3\nprint('Project service running')\n")
with open(os.path.join(PROJECT_DIR, "package.json"), "w", encoding="utf-8") as f:
    f.write('{\n  "name": "enterprise-project",\n  "private": true\n}\n')

print(f"  OK: Дерево проекта создано (обычных файлов .conf: {len(conf_locations)})")


# ---------------------------------------------------------
# TASK 5: data/auth.log
# 18,000 строк. Ровно 164 уникальных IP с "Failed password".
# ---------------------------------------------------------
print("[5/5] Генерация data/auth.log...")
TOTAL_AUTH_LINES = 18000
TARGET_FAILED_UNIQUE_IPS = 164

failed_ips = [f"{random.randint(45, 220)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
              for _ in range(TARGET_FAILED_UNIQUE_IPS)]
failed_ips = list(set(failed_ips))
while len(failed_ips) < TARGET_FAILED_UNIQUE_IPS:
    new_ip = f"{random.randint(45, 220)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
    if new_ip not in failed_ips:
        failed_ips.append(new_ip)

legit_ips = [f"192.168.1.{i}" for i in range(10, 50)] + [f"10.0.0.{i}" for i in range(10, 50)]
auth_usernames = ["root", "admin", "ubuntu", "test", "guest", "deploy", "oracle", "postgres",
                  "user1", "developer", "git", "webmaster", "operator", "backup"]

auth_lines = []
pid = 2000

for ip in failed_ips:
    day = random.randint(10, 29)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    sec = random.randint(0, 59)
    ts = f"Sep {day:02d} {hour:02d}:{minute:02d}:{sec:02d}"
    user = random.choice(auth_usernames)
    port = random.randint(30000, 65000)
    pid = (pid + 1) % 50000 + 1000
    line = f"{ts} server sshd[{pid}]: Failed password for {user} from {ip} port {port} ssh2"
    auth_lines.append((ts, line))

additional_failed_count = 6500
for _ in range(additional_failed_count):
    day = random.randint(10, 29)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    sec = random.randint(0, 59)
    ts = f"Sep {day:02d} {hour:02d}:{minute:02d}:{sec:02d}"
    ip = random.choice(failed_ips)
    user = random.choice(auth_usernames)
    port = random.randint(30000, 65000)
    pid = (pid + 1) % 50000 + 1000
    line = f"{ts} server sshd[{pid}]: Failed password for {user} from {ip} port {port} ssh2"
    auth_lines.append((ts, line))

remaining_auth = TOTAL_AUTH_LINES - len(auth_lines)
for _ in range(remaining_auth):
    day = random.randint(10, 29)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    sec = random.randint(0, 59)
    ts = f"Sep {day:02d} {hour:02d}:{minute:02d}:{sec:02d}"
    event_type = random.choice(["accepted_pwd", "accepted_key", "session_open", "session_close", "disconnect"])
    pid = (pid + 1) % 50000 + 1000
    user = random.choice(["deploy", "ubuntu", "alex_k", "developer", "backup"])
    ip = random.choice(legit_ips)
    port = random.randint(30000, 65000)
    
    if event_type == "accepted_pwd":
        line = f"{ts} server sshd[{pid}]: Accepted password for {user} from {ip} port {port} ssh2"
    elif event_type == "accepted_key":
        line = f"{ts} server sshd[{pid}]: Accepted publickey for {user} from {ip} port {port} ssh2"
    elif event_type == "session_open":
        line = f"{ts} server systemd-logind[789]: New session 42 of user {user}."
    elif event_type == "session_close":
        line = f"{ts} server systemd-logind[789]: Removed session 42."
    else:
        line = f"{ts} server sshd[{pid}]: Received disconnect from {ip} port {port}:11: disconnected by user"
        
    auth_lines.append((ts, line))

auth_lines.sort(key=lambda x: x[0])
final_auth_lines = [item[1] for item in auth_lines]

with open(os.path.join(DATA_DIR, "auth.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(final_auth_lines) + "\n")

print(f"  OK: 18000 строк создано (уникальных IP с неудачным входом: {TARGET_FAILED_UNIQUE_IPS})")
print("\nУспешно! Все наборы данных сгенерированы.")
