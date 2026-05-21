# US TV EPG

Two playlists available:

---

## Custom US-English Playlist (Recommended)

Filtered to US-accessible, English-language channels only. Geo-blocked and non-English channels removed.

**Playlist URL:** `https://CeresLabX.github.io/us-tv-epg/custom_playlist.m3u`

**EPG URL:** `https://CeresLabX.github.io/us-tv-epg/epg.xml`

**Channel count:** ~667 channels

---

## Full US Playlist (All Channels)

Complete iptv-org US playlist — all languages, all regions, including geo-restricted streams.

**Playlist URL:** `https://CeresLabX.github.io/us-tv-epg/full_playlist.m3u`

**EPG URL:** `https://CeresLabX.github.io/us-tv-epg/epg_full.xml`

**Channel count:** ~1,322 channels

---

## Usage in TiMATE

**Custom (recommended):**
1. Add playlist: `https://CeresLabX.github.io/us-tv-epg/custom_playlist.m3u`
2. Add EPG: `https://CeresLabX.github.io/us-tv-epg/epg.xml`

**Full:**
1. Add playlist: `https://CeresLabX.github.io/us-tv-epg/full_playlist.m3u`
2. Add EPG: `https://CeresLabX.github.io/us-tv-epg/epg_full.xml`

---

## Auto-Update

Both playlists and EPGs regenerate every 12 hours via cron job. The custom playlist filters out newly added non-English and geo-blocked channels automatically.

## Filtering Logic

Custom playlist includes only channels that are:
- **US-accessible** — no BBC UK, Canada-only, Australia-only, etc.
- **English or US-originating** — English-language channels, US local stations, major networks

## Note

Programme schedules are placeholder (3-hour blocks). This gives channel names, logos, and categories in TiMATE.
