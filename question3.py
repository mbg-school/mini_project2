import shodan
import json


def getVulnerabilities(hostIP: str) -> dict:
    """
    Creates a dictionary containing host IP, its CVEs and any known
    information about each specific CVE

    Parameters:
        hostIP (str): the host IP address you want the vulnerabilities for

    Returns:
        vulnerabilities (dict): Returns a dict with the host IP as the key with
                                a list of the CVEs with their info as the field
    """

    vulnerabilities = {}
    SHODAN_API_KEY = "WvWmlWL28AKTwHZZDrDNMm1hbLuWOdCz"
    api = shodan.Shodan(SHODAN_API_KEY)

    try:
        # Then we need to do a Shodan search on that IP
        host = api.host(hostIP)
        if host["vulns"]:
            vulnerabilities[hostIP] = {}
            # Print vuln information
            for item in host["vulns"]:
                CVE = item.replace("!", "")
                # print("Vulns: %s" % item)
                exploits = api.exploits.search(CVE)

                vulnerabilities[hostIP][item] = exploits["matches"]

    except:
        "An error occured"

    return vulnerabilities


def findVulnerabilities(host_file: str, dest_file: str) -> None:
    """
    Finds the vulnerabilities for each host given.

    Loads a json file with the hosts that you want to find vulnerabilities for,
    loops through the hosts and retrieves a list of the CVEs found for that host.
    Once the vulnerabilites for each host is found the entire new dictionary is saved
    to a new json file.

    Parameters:
        host_file (str): file with the host IPs that we want vulnerabilities for.
        dest_file (str): file location to save the new dictionary

    Returns:
        None
    """

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


def getHosts(block: str, file: str) -> None:
    """
    Use the Censys API to get all hosts within a block.

    Performs a Censys search with a given CIDR block as the filter and
    extracts the host IP addresses from the page information returned from
    the API call. Saves the host IPs to a new json file.

    Parameters:
        block (str): The CIDR block from which you want host IPs
        file (str): The file to save the found host IPs to

    Returns:
        None
    """

    from censys.search import CensysHosts
    import pickle
    import json

    h = CensysHosts()
    count = 0
    hosts = {}

    for page in h.search("IP: " + block, per_page=100, pages=27):
        for host in page:
            # each host is a dictionary object
            hosts[host["ip"]] = host
            count += 1

    with open(file, "w") as f:
        json.dump(hosts, f, indent=4)

    print(count)
