# DDNS Updater for IPv64.net

[![Docker Hub](https://img.shields.io/docker/pulls/nighthawkx00/dyndns-ipv64)](https://hub.docker.com/r/nighthawkx00/dyndns-ipv64)
[![GitHub](https://img.shields.io/badge/GitHub-nighthawkx0815%2Fdyndns--ipv64-blue)](https://github.com/nighthawkx0815/dyndns-ipv64)

Automatically updates your [IPv64.net](https://ipv64.net) DynDNS domains with your current public IPv4 and/or IPv6 address.
Supports multiple domains with individual API keys and multiple IP detection services with automatic fallback.

## Features

- Multiple domains with individual API keys
- IPv4 (A Record) and IPv6 (AAAA Record) support
- **DNS pre-check** — compares current DNS with public IP before sending update (saves API calls)
- Automatic fallback across multiple IP detection services
- Configurable update interval
- Custom IP detection URLs supported
- No config file needed — fully configured via environment variables
- Works with default Docker bridge network — no `network_mode: host` required
- Automatically built and published to Docker Hub via GitHub Actions

## How it works

Before sending an update to IPv64.net, the container resolves the current DNS record of your domain and compares it to your public IP. An update is only sent if the IP has changed. This prevents unnecessary API calls and avoids hitting the IPv64.net rate limit (64 updates/24h).

## IP Detection Services (default)

### IPv4
1. `https://icanhazip.com`
2. `https://api.ipify.org`
3. `https://ifconfig.me/ip`
4. `https://checkip.amazonaws.com`

### IPv6
1. `https://api6.ipify.org`
2. `https://ipv6.icanhazip.com`
3. `https://v6.ident.me`

## Docker Compose Example

### IPv4 only (default)

```yaml
services:
  dyndns-ipv64:
    image: nighthawkx00/dyndns-ipv64:latest
    container_name: dyndns-ipv64
    restart: unless-stopped
    environment:
      - DOMAIN_1=yourdomain.ipv64.de
      - KEY_1=your_api_key_1
      - DOMAIN_2=yourdomain2.ipv64.net
      - KEY_2=your_api_key_2
      - INTERVAL=15
```

### IPv4 + IPv6 for all domains

```yaml
services:
  dyndns-ipv64:
    image: nighthawkx00/dyndns-ipv64:latest
    container_name: dyndns-ipv64
    restart: unless-stopped
    environment:
      - DOMAIN_1=yourdomain.ipv64.de
      - KEY_1=your_api_key_1
      - DOMAIN_2=yourdomain2.ipv64.net
      - KEY_2=your_api_key_2
      - INTERVAL=15
      - IPV6_ENABLED=yes
```

### Per-domain IPv6 control

Enable or disable IPv6 individually per domain using `IPV6_N`.
This overrides the global `IPV6_ENABLED` setting for that specific domain.

```yaml
services:
  dyndns-ipv64:
    image: nighthawkx00/dyndns-ipv64:latest
    container_name: dyndns-ipv64
    restart: unless-stopped
    environment:
      - DOMAIN_1=yourdomain.ipv64.de
      - KEY_1=your_api_key_1
      - IPV6_1=yes              # Domain 1: IPv4 + IPv6

      - DOMAIN_2=yourdomain2.ipv64.net
      - KEY_2=your_api_key_2
      - IPV6_2=no               # Domain 2: IPv4 only

      - INTERVAL=15
```

### Custom IP detection URLs

```yaml
services:
  dyndns-ipv64:
    image: nighthawkx00/dyndns-ipv64:latest
    container_name: dyndns-ipv64
    restart: unless-stopped
    environment:
      - DOMAIN_1=yourdomain.ipv64.de
      - KEY_1=your_api_key_1
      - IPV6_1=yes
      - INTERVAL=15
      - IP_SERVICES=https://icanhazip.com,https://api.ipify.org
      - IP6_SERVICES=https://api6.ipify.org,https://ipv6.icanhazip.com
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DOMAIN_1` | ✓ | — | First domain to update |
| `KEY_1` | ✓ | — | API key for DOMAIN_1 |
| `IPV6_1` | ✗ | — | IPv6 for DOMAIN_1: `yes` or `no` (overrides global) |
| `DOMAIN_2` | ✗ | — | Second domain (optional) |
| `KEY_2` | ✗ | — | API key for DOMAIN_2 |
| `IPV6_2` | ✗ | — | IPv6 for DOMAIN_2: `yes` or `no` (overrides global) |
| `DOMAIN_N` | ✗ | — | Add as many domains as needed |
| `KEY_N` | ✗ | — | API key for DOMAIN_N |
| `IPV6_N` | ✗ | — | IPv6 for DOMAIN_N: `yes` or `no` (overrides global) |
| `INTERVAL` | ✗ | `15` | Update interval in minutes |
| `IPV6_ENABLED` | ✗ | `no` | Global IPv6 default for all domains: `yes` or `no` |
| `IP_SERVICES` | ✗ | see above | Comma-separated custom IPv4 detection URLs |
| `IP6_SERVICES` | ✗ | see above | Comma-separated custom IPv6 detection URLs |

## API Response Codes

IPv64.net returns the following status codes after each update attempt:

| Status | Meaning |
|--------|---------|
| `nochg` | IP unchanged — no update necessary |
| `good` | IP successfully updated |
| `badauth` | Invalid API key |
| `nohost` | Domain not found in your account |
| `abuse` | Too many requests — rate limited |
| `Updateintervall overcommited` | Too many updates in a short time — wait and retry |

## Example Log Output

```
2026-04-09 08:00:00  INFO     - ==================== DDNS UPDATER IPV64.NET ====================
2026-04-09 08:00:00  INFO     - IPv4 Detection gestartet...
2026-04-09 08:00:01  INFO     - Oeffentliche IPv4: 87.153.193.198
2026-04-09 08:00:01  INFO     - --- yourdomain.ipv64.de ---
2026-04-09 08:00:01  INFO     - IP CHECK    - yourdomain.ipv64.de -> IPv4=87.153.193.198 (unveraendert, kein Update noetig)
2026-04-09 08:15:00  INFO     - --- yourdomain.ipv64.de ---
2026-04-09 08:15:01  INFO     - IP CHANGE   - yourdomain.ipv64.de -> IPv4 alt=87.153.193.198 neu=87.153.200.1
2026-04-09 08:15:02  INFO     - UPDATE      - yourdomain.ipv64.de -> IPv4=87.153.200.1 (good)
```

## API Key

Your API key can be found in your [IPv64.net account](https://ipv64.net/account) under **DynDNS**.

## Notes

- The container works with the default Docker bridge network
- Use `network_mode: host` only if your Docker bridge network has no internet access
- IPv6 requires your host and network to support native IPv6 connectivity
- Both A (IPv4) and AAAA (IPv6) records must exist in your IPv64.net account
- The DNS pre-check significantly reduces API calls and prevents rate limiting

## Links

- [Docker Hub](https://hub.docker.com/r/nighthawkx00/dyndns-ipv64)
- [GitHub Repository](https://github.com/nighthawkx0815/dyndns-ipv64)
- [IPv64.net](https://ipv64.net)
