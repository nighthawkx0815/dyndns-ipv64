# DDNS Updater for IPv64.net

[![Docker Hub](https://img.shields.io/docker/pulls/nighthawkx00/dyndns-ipv64)](https://hub.docker.com/r/nighthawkx00/dyndns-ipv64)
[![GitHub](https://img.shields.io/badge/GitHub-nighthawkx0815%2Fdyndns--ipv64-blue)](https://github.com/nighthawkx0815/dyndns-ipv64)

Automatically updates your [IPv64.net](https://ipv64.net) DynDNS domains with your current public IPv4 and/or IPv6 address.
Supports multiple domains with individual API keys and multiple IP detection services with automatic fallback.

## Features

- Multiple domains with individual API keys
- IPv4 (A Record) and IPv6 (AAAA Record) support
- Automatic fallback across multiple IP detection services
- Configurable update interval
- Custom IP detection URLs supported
- No config file needed — fully configured via environment variables
- Works with default Docker bridge network — no `network_mode: host` required
- Automatically built and published to Docker Hub via GitHub Actions

## IP Detection Services (default)

### IPv4
The container tries these services in order until one responds:

1. `https://icanhazip.com`
2. `https://api.ipify.org`
3. `https://ifconfig.me/ip`
4. `https://checkip.amazonaws.com`

### IPv6
The container tries these services in order until one responds:

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

## Example Log Output

```
2026-04-09 08:00:00  INFO     - ==================== DDNS UPDATER IPV64.NET ====================
2026-04-09 08:00:00  INFO     - IPv4 Detection gestartet...
2026-04-09 08:00:01  INFO     - Oeffentliche IPv4: 87.153.193.198
2026-04-09 08:00:01  INFO     - DOMAIN      - yourdomain.ipv64.de
2026-04-09 08:00:01  INFO     - IP CHECK    - yourdomain.ipv64.de -> IPv4=87.153.193.198 (nochg)
2026-04-09 08:00:02  INFO     - IPv6 Detection gestartet...
2026-04-09 08:00:02  INFO     - Oeffentliche IPv6: 2a02:8109:abcd::1
2026-04-09 08:00:02  INFO     - DOMAIN      - yourdomain.ipv64.de
2026-04-09 08:00:02  INFO     - IP CHECK    - yourdomain.ipv64.de -> IPv6=2a02:8109:abcd::1 (nochg)
```

## API Key

Your API key can be found in your [IPv64.net account](https://ipv64.net/account) under **DynDNS**.

## Notes

- The container works with the default Docker bridge network
- Use `network_mode: host` only if your Docker bridge network has no internet access
- IPv6 requires your host and network to support native IPv6 connectivity
- Both A (IPv4) and AAAA (IPv6) records must exist in your IPv64.net account

## Links

- [Docker Hub](https://hub.docker.com/r/nighthawkx00/dyndns-ipv64)
- [GitHub Repository](https://github.com/nighthawkx0815/dyndns-ipv64)
- [IPv64.net](https://ipv64.net)
