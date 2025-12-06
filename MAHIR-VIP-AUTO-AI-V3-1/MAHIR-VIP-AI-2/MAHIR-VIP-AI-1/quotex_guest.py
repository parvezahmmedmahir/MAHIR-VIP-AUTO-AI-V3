
"""
MAHIR VIP AUTO AI - Guest Token Harvester
Attempts to obtain a valid Guest Session ID from Quotex via HTTP requests.
"""

import requests
import re
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_guest_token():
    """
    Scrapes the Quotex entry page to find a valid 'ssid' cookie or token.
    Returns: String (Token) or None
    """
    url = "https://qxbroker.com/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        session = requests.Session()
        # 1. Hit the demo trade landing page (verify=False to bypass local cert issues)
        response = session.get(url, headers=headers, timeout=10, verify=False)
        
        # 2. Extract Cookies
        cookies = session.cookies.get_dict()
        print("DEBUG Cookies Found:", cookies.keys())
        
        if 'ssid' in cookies:
            return cookies['ssid']
            
        # Fallback: Search in HTML for "token" using Regex
        # Sometimes it's hidden in window.settings
        token_match = re.search(r'"token":"([a-zA-Z0-9]+)"', response.text)
        if token_match:
            return token_match.group(1)

        return None

    except Exception as e:
        print(f"Error fetching guest token: {e}")
        return None

if __name__ == "__main__":
    print("Attempting to fetch Guest Token...")
    token = get_guest_token()
    if token:
        print(f"SUCCESS! Guest Token Found: {token[:10]}... (Len: {len(token)})")
    else:
        print("FAILED to retrieve Guest Token. Cloudflare/Server protection active.")
