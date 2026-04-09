import os
import time
import requests
import schedule
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(levelname)-8s - %(message)s')

INTERVAL = int(os.environ.get("INTERVAL", "15"))
IPV6_ENABLED = os.environ.get("IPV6_ENABLED", "no").lower() == "yes"

DEFAULT_IP_SERVICES = [
    "https://icanhazip.com",
    "https://api.ipify.org",
    "https://ifconfig.me/ip",
    "https://checkip.amazonaws.com"
]

DEFAULT_IPV6_SERVICES = [
    "https://api6.ipify.org",
    "https://ipv6.icanhazip.com",
    "https://v6.ident.me"
]

CUSTOM_IP_SERVICES = os.environ.get("IP_SERVICES", "")
if CUSTOM_IP_SERVICES:
    IP_SERVICES = [s.strip() for s in CUSTOM_IP_SERVICES.split(",")]
else:
    IP_SERVICES = DEFAULT_IP_SERVICES

CUSTOM_IPV6_SERVICES = os.environ.get("IP6_SERVICES", "")
if CUSTOM_IPV6_SERVICES:
    IPV6_SERVICES = [s.strip() for s in CUSTOM_IPV6_SERVICES.split(",")]
else:
    IPV6_SERVICES = DEFAULT_IPV6_SERVICES

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
            if ip and "." in ip:
                return ip
        except:
            continue
    return None

def get_ipv6():
    for url in IPV6_SERVICES:
        try:
            r = requests.get(url, timeout=5)
            ip = r.text.strip()
            if ip and ":" in ip:
                return ip
        except:
            continue
    return None

def update_providers(ip, label="IPv4"):
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
            logging.info(f"IP CHECK    - {p['domain']} -> {label}={ip} ({status})")
        except Exception as e:
            logging.error(f"FEHLER      - {p['domain']}: {e}")

def update_dns():
    banner("DDNS UPDATER IPV64.NET")

    # IPv4
    logging.info("IPv4 Detection gestartet...")
    ip = get_ip()
    if ip:
        logging.info(f"Oeffentliche IPv4: {ip}")
        update_providers(ip, "IPv4")
    else:
        logging.error("Keine gueltige IPv4-Adresse gefunden")

    # IPv6
    if IPV6_ENABLED:
        logging.info("IPv6 Detection gestartet...")
        ipv6 = get_ipv6()
        if ipv6:
            logging.info(f"Oeffentliche IPv6: {ipv6}")
            update_providers(ipv6, "IPv6")
        else:
            logging.warning("Keine gueltige IPv6-Adresse gefunden")
    else:
        logging.info("IPv6 ist deaktiviert (IPV6_ENABLED=no)")

    print("=" * 78)

schedule.every(INTERVAL).minutes.do(update_dns)
update_dns()
while True:
    schedule.run_pending()
    time.sleep(30)
