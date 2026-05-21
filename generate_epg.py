#!/usr/bin/env python3
"""
Generate EPG XML from iptv-org US M3U playlist.
Outputs XMLTV format for use in IPTV players like TiMATE.
"""

import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re
import sys

M3U_URL = "https://iptv-org.github.io/iptv/countries/us.m3u"
OUTPUT_FILE = "epg.xml"

def fetch_m3u():
    req = urllib.request.Request(
        M3U_URL,
        headers={'User-Agent': 'Mozilla/5.0 (compatible; TV EPG Generator)'}
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        # Normalize CRLF -> LF
        raw = response.read().decode('utf-8', errors='replace')
        return raw.replace('\r\n', '\n').replace('\r', '\n')

def parse_m3u(content):
    channels = []
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#EXTINF:'):
            # Extract attributes and channel name
            # Format: #EXTINF:-1 tvg-id="..." tvg-logo="..." group-title="...",Channel Name
            extinf = line[8:]  # strip '#EXTINF:'
            # Find the channel name after the last comma
            comma_idx = extinf.rfind(',')
            channel_name = extinf[comma_idx+1:].strip() if comma_idx != -1 else ''
            extinf_attrs = extinf[:comma_idx] if comma_idx != -1 else extinf
            
            tvg_id = ''
            tvg_logo = ''
            group_title = ''
            
            # Parse tvg-id
            m = re.search(r'tvg-id="([^"]*)"', extinf_attrs)
            if m: tvg_id = m.group(1)
            m = re.search(r'tvg-logo="([^"]*)"', extinf_attrs)
            if m: tvg_logo = m.group(1)
            m = re.search(r'group-title="([^"]*)"', extinf_attrs)
            if m: group_title = m.group(1)
            
            # Get URL from next non-empty line
            j = i + 1
            url = ''
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                url = lines[j].strip()
            
            # Strip resolution (720p), (1080p), etc. and bracketed tags like [Geo-blocked], [Not 24/7]
            clean_name = re.sub(r'\s*\(\d{3,4}[ip]\)\s*', '', channel_name)
            clean_name = re.sub(r'\s*\[[^\]]+\]\s*', '', clean_name).strip()

            # Extract language from tvg-id suffix (e.g. "EWTN.us@Spanish" -> "Spanish")
            LANGUAGE_CODES = {
                'english', 'en', 'espanol', 'spanish', 'es',
                'french', 'fr', 'francais',
                'chinese', 'zh', 'mandarin',
                'korean', 'ko', 'korean',
                'arabic', 'ar',
                'hindi', 'hi',
                'portuguese', 'pt', 'brasil', 'brazilian',
                'german', 'de', 'deutsch',
                'italian', 'it',
                'japanese', 'ja', 'jp',
                'russian', 'ru',
                'vietnamese', 'vi',
                'tagalog', 'filipino', 'tl',
                'polish', 'pl',
                'dutch', 'nl',
                'turkish', 'tr',
                'greek', 'el',
                'hebrew', 'he',
                'persian', 'fa', 'farsi',
                'urdu',
                'bengali', 'bn',
                'malayalam', 'ml',
                'tamil', 'ta',
                'telugu', 'te',
                'punjabi', 'pa',
                'gujarati', 'gu',
                'marathi', 'mr',
                'nepali', 'ne',
            }
            language = ''
            at_idx = tvg_id.rfind('@')
            if at_idx != -1:
                lang_candidate = tvg_id[at_idx+1:].lower()
                if lang_candidate in LANGUAGE_CODES:
                    # Capitalize properly
                    language = lang_candidate.title()
                    if language == 'Es': language = 'Spanish'
                    elif language == 'Zh': language = 'Chinese'
                    elif language == 'Ko': language = 'Korean'
                    elif language == 'Ar': language = 'Arabic'
                    elif language == 'Hi': language = 'Hindi'
                    elif language == 'Pt': language = 'Portuguese'
                    elif language == 'De': language = 'German'
                    elif language == 'It': language = 'Italian'
                    elif language == 'Ja': language = 'Japanese'
                    elif language == 'Ru': language = 'Russian'
                    elif language == 'Vi': language = 'Vietnamese'
                    elif language == 'Tl': language = 'Tagalog'
                    elif language == 'Pl': language = 'Polish'
                    elif language == 'Nl': language = 'Dutch'
                    elif language == 'Tr': language = 'Turkish'
                    elif language == 'El': language = 'Greek'
                    elif language == 'He': language = 'Hebrew'
                    elif language == 'Fa': language = 'Persian'
                    elif language == 'Bn': language = 'Bengali'
                    elif language == 'Ml': language = 'Malayalam'
                    elif language == 'Ta': language = 'Tamil'
                    elif language == 'Te': language = 'Telugu'
                    elif language == 'Pa': language = 'Punjabi'
                    elif language == 'Gu': language = 'Gujarati'
                    elif language == 'Mr': language = 'Marathi'
                    elif language == 'Ne': language = 'Nepali'
                    elif language == 'Espanol': language = 'Spanish'
                    elif language == 'Francais': language = 'French'
                    elif language == 'Deutsch': language = 'German'
                    elif language == 'Brasileiro': language = 'Portuguese'
                    elif language == 'Farsi': language = 'Persian'
                    elif language == 'Filipino': language = 'Tagalog'

            if tvg_id and clean_name:
                channels.append({
                    'id': tvg_id,
                    'name': clean_name,
                    'language': language,
                    'logo': tvg_logo,
                    'category': group_title,
                    'url': url
                })
            i = j if j > i else i + 1
        else:
            i += 1
    
    return channels

def generate_epg(channels):
    """Generate XMLTV EPG with placeholder programmes for each channel."""
    now = datetime.utcnow()
    
    # Start from last hour boundary
    start_time = now.replace(minute=0, second=0, microsecond=0)
    if now.hour >= 12:
        start_time = start_time.replace(hour=12)
    else:
        start_time = start_time.replace(hour=0)
    
    tv = ET.Element('tv')
    tv.set('generator-info-name', 'iptv-org US EPG Generator')
    tv.set('generator-info-url', 'https://github.com/CeresLabX/us-tv-epg')
    
    # Add channels
    for ch in channels:
        channel_el = ET.SubElement(tv, 'channel')
        channel_el.set('id', ch['id'])
        
        display_name = ET.SubElement(channel_el, 'display-name')
        display_name.set('lang', ch.get('language', 'en'))
        display_name.text = ch['name']

        if ch.get('language'):
            lang_el = ET.SubElement(channel_el, 'lang')
            lang_el.text = ch['language']

        if ch['logo']:
            icon = ET.SubElement(channel_el, 'icon')
            icon.set('src', ch['logo'])
        
        if ch['category']:
            category = ET.SubElement(channel_el, 'category')
            category.set('lang', 'en')
            category.text = ch['category']
    
    # 48 hrs of programmes: 16 x 3-hour blocks, rotating through content types
    programme_blocks = [
        ("Live Broadcast", "Live programming stream"),
        ("Morning Edition", "News and current events"),
        ("Midday Entertainment", "Variety and entertainment content"),
        ("Afternoon Programming", "General programming"),
        ("Evening Prime", "Prime time entertainment"),
        ("Late Night", "Late night programming"),
        ("Overnight Re-run", "Archived programming replay"),
        ("Early Morning", "Early morning programming"),
        ("Live Broadcast", "Live programming stream"),
        ("Morning Edition", "News and current events"),
        ("Midday Entertainment", "Variety and entertainment content"),
        ("Afternoon Programming", "General programming"),
        ("Evening Prime", "Prime time entertainment"),
        ("Late Night", "Late night programming"),
        ("Overnight Re-run", "Archived programming replay"),
        ("Early Morning", "Early morning programming"),
    ]
    
    for ch in channels:
        block_start = start_time
        for title, desc in programme_blocks:
            block_end = block_start + timedelta(hours=3)
            
            prog = ET.SubElement(tv, 'programme')
            prog.set('channel', ch['id'])
            prog.set('start', block_start.strftime('%Y%m%d%H%M%S') + ' +0000')
            prog.set('stop', block_end.strftime('%Y%m%d%H%M%S') + ' +0000')
            
            prog_lang = ch.get('language', 'en')
            title_el = ET.SubElement(prog, 'title')
            title_el.set('lang', prog_lang)
            title_el.text = f"{ch['name']} - {title}"

            desc_el = ET.SubElement(prog, 'desc')
            desc_el.set('lang', prog_lang)
            desc_el.text = f"{ch['category']} | {desc}" if ch['category'] else desc
            
            category_el = ET.SubElement(prog, 'category')
            category_el.set('lang', 'en')
            category_el.text = ch['category'] or 'Entertainment'
            
            block_start = block_end
    
    return tv

def main():
    print(f"Fetching M3U playlist from {M3U_URL}...")
    content = fetch_m3u()
    
    print("Parsing channels...")
    channels = parse_m3u(content)
    print(f"Found {len(channels)} channels")
    
    if not channels:
        print("ERROR: No channels parsed from M3U!", file=sys.stderr)
        sys.exit(1)
    
    print("Generating EPG XML...")
    tv = generate_epg(channels)
    
    # Write with XML declaration
    tree = ET.ElementTree(tv)
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding='utf-8', xml_declaration=False)
    
    print(f"EPG written to {OUTPUT_FILE}")
    print(f"URL: https://CeresLabX.github.io/us-tv-epg/epg.xml")

if __name__ == '__main__':
    main()
