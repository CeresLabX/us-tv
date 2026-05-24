# US TV Playlist & EPG

Filtered to US-accessible, English-language channels only. Single group per channel.

**Playlist URL:** `https://CeresLabX.github.io/us-tv/playlist.m3u`

**EPG URL:** `https://CeresLabX.github.io/us-tv/epg.xml`

**Channel count:** ~676 channels

---

## Source

**iptv-org US** — `https://iptv-org.github.io/iptv/countries/us.m3u`

---

## Groups

General, News, Sports, Entertainment, Movies, Series, Kids, Religious, Lifestyle, Music, Documentary, Comedy, Culture, Business, Education, Outdoor, Local News, Local News | PNW

---

## Usage in TiviMate

1. Add playlist: `https://CeresLabX.github.io/us-tv/playlist.m3u`
2. Add EPG: `https://CeresLabX.github.io/us-tv/epg.xml`

---

## Auto-Update

Playlist and EPG regenerate every 12 hours via GitHub Actions (`update.yml` workflow).

Programme schedules are placeholder (3-hour blocks). This gives channel names, logos, and categories in TiviMate.

---

## Filtering Rules

### Always Applied
- **Source:** iptv-org US only (no Free-TV, no iptv-org English)
- **Language:** English only — no Spanish, no non-English channels
- **VOD platforms blocked:** Pluto TV, Plex, Roku Channel, Samsung TV Plus, Tubi
- **Non-Latin script blocked:** Cyrillic, Greek, Arabic, Hebrew, CJK, Devanagari
- **Single group per channel** — consolidated categories
- **No stream validation** — streams included as-is from iptv-org

### Permanently Blocked URLs & Domains
**154 dead streams + 18 dead domains** are permanently excluded. These will NEVER be re-added, even if they reappear in iptv-org updates.

Blocked domains:
- `tvpass.org` — subscription VOD, no free access
- `streamhoster.com` — platform shut down
- `cablecast.tv` — community TV platform
- `scientology.org` — Scientology Network
- `streamspot.com` — CDN shut down
- `fuel-streaming-prod01.fuelmedia.io`, `relentlessinnovations.net`, `bozztv.com`, `magictvbox.com`, `5centscdn.com`, `persiana.live`, `telered.live`, `servistreaming.com`, `kazmazpaz.ru`, `jlahozconsulting.com`, `rsc.cdn77.org`, `boo.tv`, `dai.google.com`

All 154 exact blocked URLs are stored in `build_filtered_playlist.py` under `REJECT_URLS`.

---

## Local News | PNW Channels

Hardcoded in `build_filtered_playlist.py` — survive every auto-refresh:
- **KGW 8 News Portland** (`KGWDT1.us`)
- **KATU News Portland** (`KATUDT1.us`)
- **KIRO 7 News Seattle** (`KIRODT1.us`)

---

## How to Re-Validate Streams (US Validation)

Run this from a **US-based machine** to catch new dead streams:

### Step 1: Download latest playlist
```powershell
curl.exe -s https://CeresLabX.github.io/us-tv/playlist.m3u -o playlist.m3u
```

### Step 2: Download validator
```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/CeresLabX/us-tv/main/validate-streams.ps1" -OutFile "validate-streams.ps1"
```

### Step 3: Run validation
```powershell
powershell -ExecutionPolicy Bypass -File validate-streams.ps1
```

### Step 4: Send results to Vectrix
After validation completes, send `failed-streams.txt` to Vectrix for analysis. Vectrix will:
1. Parse the failures
2. Add new dead URLs to `REJECT_URLS` in `build_filtered_playlist.py`
3. Add any new dead domains to `REJECT_DOMAINS`
4. Rebuild and push

**Important:** Validation must be run from a US IP. Canadian/US VPS tests are NOT representative of US availability. Use a US residential connection, VPN with US exit, or ask Kevin to run from his Windows PC.

---

## Key Files

| File | Purpose |
|------|---------|
| `build_filtered_playlist.py` | Main build script — source of truth for all filtering rules |
| `generate_epg.py` | EPG generator |
| `validate-streams.ps1` | PowerShell stream validator for US validation |
| `playlist.m3u` | Live playlist |
| `epg.xml` | Live EPG |
| `stream-validation-log.txt` | Full validation log |
| `failed-streams.txt` | Failed streams from last US validation |
