import os
import time
import requests
import schedule
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(levelname)-8s - %(message)s')

INTERVAL = int(os.environ.get("INTERVAL", "15"))

DEFAULT_IP_SERVICES = [
    "https://icanhazip.com",
    "https://api.ipify.org",
    "https://ifconfig.me/ip",
    "https://checkip.amazonaws.com"
]

CUSTOM_IP_SERVICES = os.environ.get("IP_SERVICES", "")
if CUSTOM_IP_SERVICES:
    IP_SERVICES = [s.strip() for s in CUSTOM_IP_SERVICES.split(",")]
else:
    IP_SERVICES = DEFAULT_IP_SERVICES

PROVIDERS = []
i = 1
while True:
    domain = os.environ.get(f"DOMAIN_{i}")
    key = os.environ.get(f"KEY_{i}")
    if not domain or not key:
        break
    PROVIDERS.append({"domain": domain, "key": key})
    i += 1

def banner(text):
    line = "=" * 78
    print(line)
    print(f"{'':=<20} {text:^36} {'':=<20}")
    print(line)

def get_ip():
    for url in IP_SERVICES:
        try:
            r = requests.get(url, timeout=5)
            ip = r.text.strip()
            if ip:
                return ip
        except:
            continue
    return None

def update_dns():
    banner("DDNS UPDATER IPV64.NET")
    logging.info("IPv6 ist deaktiviert")
    logging.info("IPv4 Detection gestartet...")
    ip = get_ip()
    if not ip:
        logging.error("Keine gültige IPv4-Adresse gefunden")
        print("=" * 78)
        return
    logging.info(f"Öffentliche IPv4: {ip}")
    for p in PROVIDERS:
        try:
            r = requests.get(
                "https://ipv64.net/nic/update",
                params={"key": p["key"], "domain": p["domain"], "ip": ip},
                timeout=10
            )
            result = r.json()
            status = result.get("info", "unknown")
            logging.info(f"DOMAIN      - {p['domain']}")
            logging.info(f"IP CHECK    - {p['domain']} -> IPv4={ip} ({status})")
        except Exception as e:
            logging.error(f"FEHLER      - {p['domain']}: {e}")
    print("=" * 78)

schedule.every(INTERVAL).minutes.do(update_dns)
update_dns()
while True:
    schedule.run_pending()
    time.sleep(30)
