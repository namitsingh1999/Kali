import requests

def request(url):
    try:
        return requests.get("https://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "facebook.com"

with open("/home/kali/Downloads/files-and-dirs-wordlist.txt", "r") as dir_wordlist_file:
    for line in dir_wordlist_file:
        word = line.strip()
        test_url = target_url + "/" + word
        response = request(test_url)
        if response:
            print("[+] Discovered URL --> " + test_url)

request(target_url)