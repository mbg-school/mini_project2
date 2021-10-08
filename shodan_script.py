import shodan
import requests
import sys

def getVulnerabilities():

    SHODAN_API_KEY = "WvWmlWL28AKTwHZZDrDNMm1hbLuWOdCz"
    api = shodan.Shodan(SHODAN_API_KEY)

    target = "www.packtpub.com"

    dnsResolve = (
        "https://api.shodan.io/dns/resolve?hostnames=" + target + "&key=" + SHODAN_API_KEY
    )

    try:
        # First we need to resolve our targets domain to an IP
        resolved = requests.get(dnsResolve)
        hostIP = resolved.json()[target]

        # Then we need to do a Shodan search on that IP
        host = api.host(hostIP)
        print("IP: %s" % host["ip_str"])
        print("Organization: %s" % host.get("org", "n/a"))
        print("Operating System: %s" % host.get("os", "n/a"))

        # Print all banners
        for item in host["data"]:
            print("Port: %s" % item["port"])
            print("Banner: %s" % item["data"])

        # Print vuln information
        for item in host["vulns"]:
            CVE = item.replace("!", "")
            print("Vulns: %s" % item)
            exploits = api.exploits.search(CVE)
            for item in exploits["matches"]:
                if item.get("cve")[0] == CVE:
                    print(item.get("description"))
    except:
        "An error occured"


def getHosts(block:str, file:str):

    from censys.search import CensysHosts
    import pickle
    import json


    h = CensysHosts()
    count = 0
    hosts = {}

    
    # Multiple pages of search results
    # You can optionally pass in a number of results to be returned
    # each page and the number of pages you want returned.

    # cursor = None

    # while(True):
    #         for page in h.search("IP: " + block, per_page=100, cursor=cursor):
        
    #             print(page)
    #             # each page is a list of hosts ??
    #             #hosts += page
    #             for host in page:
    #                 # each host is a dictionary object
    #                 hosts[host['ip']] = host
    #                 count += 1
    #                 # hosts.append(host)
    #                 # json.dumps
    #                 #f.write(page)
    #                 #f.write(page)
                

    #             cursor = page.links.next
    #             if not cursor:
    #                 break

    for page in h.search("IP: " + block, per_page=100, pages=27):
        
        #print(page)
        # each page is a list of hosts ??
        #hosts += page
        for host in page:
            # each host is a dictionary object
            hosts[host['ip']] = host
            count += 1
            # hosts.append(host)
            # json.dumps
            #f.write(page)
            #f.write(page)
    
    with open(file, 'w') as f:
        json.dump(hosts, f, indent=4)
        
        
    print(count)

    # # View each result returned
    # # For `hosts` this looks like a mapping of IPs to view results
    # query = h.search("service.service_name: HTTP", per_page=5, pages=2)
    # print(query.view_all())
