# DDNS Updater for IPv64.net

[![Docker Hub](https://img.shields.io/docker/pulls/nighthawkx00/dyndns-ipv64)](https://hub.docker.com/r/nighthawkx00/dyndns-ipv64)

> Docker Hub: [hub.docker.com/r/nighthawkx00/dyndns-ipv64](https://hub.docker.com/r/nighthawkx00/dyndns-ipv64)

Automatically updates your [IPv64.net](https://ipv64.net) DynDNS domains with your current public IPv4 address.
Supports multiple domains with individual API keys and multiple IP detection services with automatic fallback.

## Features

- Multiple domains with individual API keys
- Automatic fallback across multiple IP detection services
- Configurable update interval
- Custom IP detection URLs supported
- No config file needed — fully configured via environment variables
- Works with default Docker bridge network — no `network_mode: host` required
- Automatically built and published to Docker Hub via GitHub Actions

## IP Detection Services (default)

The container tries these services in order until one responds:

1. `https://icanhazip.com`
2. `https://api.ipify.org`
3. `https://ifconfig.me/ip`
4. `https://checkip.amazonaws.com`

## Docker Compose Example

```yaml
services:
  dyndns-ipv64:
    image: DEIN_USERNAME/dyndns-ipv64:latest
    container_name: dyndns-ipv64
    restart: unless-stopped
    environment:
      - DOMAIN_1=yourdomain.ipv64.de
      - KEY_1=your_api_key_1
      - DOMAIN_2=yourdomain2.ipv64.net
      - KEY_2=your_api_key_2
      - INTERVAL=15
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DOMAIN_1` | ✓ | — | First domain to update |
| `KEY_1` | ✓ | — | API key for DOMAIN_1 |
| `DOMAIN_2` | ✗ | — | Second domain (optional) |
| `KEY_2` | ✗ | — | API key for DOMAIN_2 |
| `DOMAIN_N` | ✗ | — | Add as many domains as needed |
| `KEY_N` | ✗ | — | API key for DOMAIN_N |
| `INTERVAL` | ✗ | `15` | Update interval in minutes |
| `IP_SERVICES` | ✗ | see above | Comma-separated custom IP detection URLs |

## Custom IP Detection URLs

Override the default IP detection services:

```yaml
environment:
  - IP_SERVICES=https://icanhazip.com,https://api.ipify.org
```

## API Response Codes

IPv64.net returns the following status codes after each update attempt:

| Status | Meaning |
|--------|---------|
| `nochg` | IP unchanged — no update necessary |
| `good` | IP successfully updated |
| `badauth` | Invalid API key |
| `nohost` | Domain not found in your account |
| `abuse` | Too many requests — rate limited |

## API Key

Your API key can be found in your [IPv64.net account](https://ipv64.net/account) under **DynDNS**.

## Notes

- The container works with the default Docker bridge network
- Use `network_mode: host` only if your Docker bridge network has no internet access
- IPv6 is not supported — IPv4 only
