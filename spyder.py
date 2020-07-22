import requests

def request(url):
    try:
        return requests.get("https://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "facebook.com"

with open("/home/kali/Downloads/subdomains-wodlist.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = word + "." + target_url
        response = request(test_url)
        if response:
            print("[+] Discovered subdomains --> " + test_url)

request(target_url)