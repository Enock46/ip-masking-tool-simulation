import requests
import random
import json

# simple ip masking
import requests

def ip_masking_tool(target_url, proxy_ip, proxy_port):
    """
    Sends a request to the target URL using a proxy to mask the user's real IP address.
    Args:
        target_url (str): The URL to send the request to.
        proxy_ip (str): The IP address of the proxy server.
        proxy_port (int): The port of the proxy server.
    """
    proxies = {
        "http": f"http://{proxy_ip}:{proxy_port}",
        "https": f"http://{proxy_ip}:{proxy_port}",
    }

    try:
        print(f"Sending request to {target_url} using proxy {proxy_ip}:{proxy_port}...")
        response = requests.get(target_url, proxies=proxies, timeout=5)
        print("\nRequest successful!")
        print("Response status code:", response.status_code)
        print("Response headers:", response.headers)
    except requests.exceptions.RequestException as e:
        print("\nRequest failed!")
        print("Error:", e)

# Example Usage
print("Welcome to the Basic IP Masking Tool!")
target = input("Enter the target URL (e.g., https://httpbin.org/ip): ").strip()
proxy_ip = input("Enter the proxy IP address: ").strip()
proxy_port = int(input("Enter the proxy port: "))
ip_masking_tool(target, proxy_ip, proxy_port)


#  advanced version if ip masking

def fetch_proxies():
    """Fetches free proxy list from an online source."""
    proxy_list_url = "https://www.proxy-list.download/api/v1/get?type=http"
    try:
        response = requests.get(proxy_list_url, timeout=5)
        proxies = response.text.splitlines()
        print(f"Fetched {len(proxies)} proxies!")
        return proxies
    except requests.exceptions.RequestException as e:
        print("Failed to fetch proxy list:", e)
        return []

def validate_proxy(proxy):
    """Checks if a proxy is functional."""
    test_url = "https://httpbin.org/ip"
    try:
        response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            print(f"Proxy {proxy} is valid!")
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def get_geolocation(ip):
    """Fetches geolocation details of an IP address."""
    geo_api_url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(geo_api_url, timeout=5)
        return response.json()
    except requests.exceptions.RequestException:
        return {}

def ip_masking_tool(target_url, proxies):
    """
    Sends a request to the target URL using a random proxy from the list.
    """
    for _ in range(5):  # Retry mechanism
        proxy = random.choice(proxies)
        print(f"Trying proxy: {proxy}")
        try:
            response = requests.get(target_url, proxies={"http": proxy, "https": proxy}, timeout=5)
            if response.status_code == 200:
                print("\nRequest successful!")
                print("Response status code:", response.status_code)
                print("Response headers:", response.headers)

                # Geolocation of the masked IP
                masked_ip = response.json().get("origin", proxy)
                geolocation = get_geolocation(masked_ip)
                print("Geolocation of masked IP:", json.dumps(geolocation, indent=2))
                return
        except requests.exceptions.RequestException:
            print(f"Proxy {proxy} failed. Trying another...")
    print("\nAll proxies failed! Unable to mask IP.")

# Main function
if __name__ == "__main__":
    print("Welcome to the Enhanced IP Masking Tool!")
    target = input("Enter the target URL (e.g., https://httpbin.org/ip): ").strip()

    print("Fetching proxy list...")
    proxies = fetch_proxies()
    if not proxies:
        print("No proxies available. Exiting...")
    else:
        valid_proxies = [proxy for proxy in proxies if validate_proxy(proxy)]
        if not valid_proxies:
            print("No valid proxies found. Exiting...")
        else:
            ip_masking_tool(target, valid_proxies)
