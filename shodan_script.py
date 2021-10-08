import shodan
import requests
import sys
import json

def getVulnerabilities(hostIP:str):
    # returns a dictionary of the hosts with vulnerabilities
    # { ip : [  ]    }
    vulnerableHosts = {}
    SHODAN_API_KEY = "WvWmlWL28AKTwHZZDrDNMm1hbLuWOdCz"
    api = shodan.Shodan(SHODAN_API_KEY)

    try:
        # Then we need to do a Shodan search on that IP
        host = api.host(hostIP)
        if host["vulns"]:
            vulnerableHosts[hostIP] = {}
            # Print vuln information
            for item in host["vulns"]:
                CVE = item.replace("!", "")
                #print("Vulns: %s" % item)
                exploits = api.exploits.search(CVE)

                vulnerableHosts[hostIP][item] = exploits["matches"]

    except:
        "An error occured"

    return(vulnerableHosts)

def findVulnerabilities(host_file:str, dest_file:str):
    with open(host_file, "r") as f:
        rawJsonData = json.load(f)
    
    vulnerabilities = {}
    # get hosts from json file
    hosts = rawJsonData.keys()

    for host in hosts:
        vulnerabilities.update(getVulnerabilities(host))

    print(json.dumps(vulnerabilities, indent=4))

    with open(dest_file, "w") as f:
        json.dump(vulnerabilities, f, indent=4)


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

    for page in h.search("IP: " + block, per_page=100, pages=27):
        for host in page:
            # each host is a dictionary object
            hosts[host['ip']] = host
            count += 1

    
    with open(file, 'w') as f:
        json.dump(hosts, f, indent=4)
        
    print(count)