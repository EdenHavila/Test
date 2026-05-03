## GitHub Copilot Chat

- Extension: 0.35.3 (prod)
- VS Code: 1.107.1 (994fd12f8d3a5aa16f17d42c041e5809167e845a)
- OS: win32 10.0.26200 x64
- GitHub Account: EdenHavila

## Network

User Settings:
```json
  "http.systemCertificatesNode": false,
  "github.copilot.advanced.debug.useElectronFetcher": true,
  "github.copilot.advanced.debug.useNodeFetcher": false,
  "github.copilot.advanced.debug.useNodeFetchFetcher": true
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 140.82.121.5 (152 ms)
- DNS ipv6 Lookup: Error (143 ms): getaddrinfo ENOTFOUND api.github.com
- Proxy URL: None (2 ms)
- Electron fetch (configured): HTTP 200 (1130 ms)
- Node.js https: HTTP 200 (742 ms)
- Node.js fetch: HTTP 200 (806 ms)

Connecting to https://api.individual.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.114.22 (131 ms)
- DNS ipv6 Lookup: Error (137 ms): getaddrinfo ENOTFOUND api.individual.githubcopilot.com
- Proxy URL: None (1 ms)
- Electron fetch (configured): HTTP 200 (974 ms)
- Node.js https: HTTP 200 (882 ms)
- Node.js fetch: HTTP 200 (1056 ms)

Connecting to https://proxy.individual.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 4.225.11.192 (137 ms)
- DNS ipv6 Lookup: Error (135 ms): getaddrinfo ENOTFOUND proxy.individual.githubcopilot.com
- Proxy URL: None (5 ms)
- Electron fetch (configured): HTTP 200 (889 ms)
- Node.js https: HTTP 200 (655 ms)
- Node.js fetch: HTTP 200 (842 ms)

Connecting to https://mobile.events.data.microsoft.com: HTTP 404 (537 ms)
Connecting to https://dc.services.visualstudio.com: HTTP 404 (1232 ms)
Connecting to https://copilot-telemetry.githubusercontent.com/_ping: HTTP 200 (943 ms)
Connecting to https://telemetry.individual.githubcopilot.com/_ping: HTTP 200 (1029 ms)
Connecting to https://default.exp-tas.com: HTTP 400 (806 ms)

Number of system certificates: 50

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).