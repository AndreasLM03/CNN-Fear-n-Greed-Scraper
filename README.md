# CNN Fear & Greed Collector

> *"Be fearful when others are greedy, and greedy when others are fearful."* — Warren Buffett

<img src="FnG Index.jpg" width="600">

Lightweight Docker container that fetches the [CNN Fear & Greed Index](https://money.cnn.com/data/fear-and-greed/) hourly and appends it to a CSV file. No browser, no Selenium — plain HTTP only.

---

## How it works

The container starts, fetches the current index via a direct JSON endpoint, writes one row to a CSV, and exits. Scheduling is handled outside the container (cron / systemd / Portainer).

**Data sources (no browser required):**

| Priority | Source | Endpoint |
|---|---|---|
| 1 | CNN Dataviz API | `production.dataviz.cnn.io/index/fearandgreed/graphdata` |

---

## Project structure

```
fng-collector/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── config.py       # constants (URLs, paths, log limits)
├── scraper.py      # HTTP fetch
├── storage.py      # CSV write with duplicate guard
├── main.py         # entry point
└── tests/
```

**Output CSV** (`/data/fng.csv`):
```csv
timestamp,value
2026-07-01T21:00:00,33
2026-07-01T22:00:00,35
```

---

## Run locally

```bash
mkdir -p ~/fng-data/logs

docker build -t fng-collector:latest .

docker run --rm \
  -v ~/fng-data:/data \
  -e TZ=Europe/Berlin \
  fng-collector:latest
```

---

## Deploy on Proxmox / Portainer

Pull the image directly from GitHub Container Registry:

```
ghcr.io/YOUR_GITHUB_USERNAME/fng-collector:latest
```

**Portainer → Add container:**

| Field | Value |
|---|---|
| Image | `ghcr.io/YOUR_GITHUB_USERNAME/fng-collector:latest` |
| Restart policy | Never |
| Volume | `/opt/fng-data` → `/data` (bind mount) |
| Env | `TZ=Europe/Berlin` |

**Hourly scheduling on the host:**

```bash
# crontab -e
0 * * * * docker run --rm -v /opt/fng-data:/data -e TZ=Europe/Berlin ghcr.io/YOUR_GITHUB_USERNAME/fng-collector:latest
```

Or with systemd timer — see [fng-collector/README.md](fng-collector/README.md).

---

## Dropbox sync via rclone (optional)

A separate rclone container syncs `/opt/fng-data` to Dropbox — no credentials in this codebase.

```bash
# daily sync (crontab -e on host)
30 2 * * * docker run --rm \
  -v /opt/fng-data:/data:ro \
  -v /opt/rclone-config:/config/rclone \
  rclone/rclone:latest sync /data dropbox:fng-backup \
  --config /config/rclone/rclone.conf
```

---

## CI/CD

Pushing to `main` triggers GitHub Actions → builds image → pushes to `ghcr.io`.  
See [`.github/workflows/docker.yml`](fng-collector/.github/workflows/docker.yml).
