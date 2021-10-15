import json


def findMaxVuln(file: str) -> None:
    """
    Prints both the CVE with the most occurences in a given json object and a
    list with every CVE found that has that number of occurences.

    Parameters:
        file (str): JSON file containing the host and CVE information

    Returns:
        None
    """

    count = {}
    maxVulnList = []
    maxVuln = 0

    # compile the number of each existing vulneralbility
    with open(file, "r") as f:
        data = json.load(f)
        for host in data:
            for vuln in data[host]:
                if data[host][vuln]:
                    if vuln in count:
                        count[vuln] += 1
                    else:
                        count[vuln] = 1

    for vuln in count:
        if count[vuln] > maxVuln:
            maxVuln = count[vuln]
            maxVulnList = [vuln]
        elif count[vuln] == maxVuln:
            maxVulnList.append(vuln)
        else:
            pass

    print(maxVulnList, maxVuln)


def findVulnByYear(file: str, year: int) -> None:
    """
    Prints a dict with each host that has any CVEs created in the given year
     as the key and a list of the CVEs

    Parameters:
        file (str): JSON file containing the host and CVE information
        year (int): The year that you want CVEs from

    Returns:
        None

    """

    vulns = {}

    # get all the vulns of a specific year
    with open(file, "r") as f:
        data = json.load(f)
        for host in data:
            for vuln in data[host]:
                date = vuln[4:8]
                if int(date) == year:
                    desc = None
                    if data[host][vuln]:
                        desc = data[host][vuln][0]["description"]
                    if host in vulns:
                        info = {}
                        info["CVE"] = vuln
                        info["Description"] = desc
                        vulns[host].append(info)
                    else:
                        info = {}
                        info["CVE"] = vuln
                        info["Description"] = desc
                        vulns[host] = [info]

    print(json.dumps(vulns, indent=4))


def hostWithMostVulns(file: str) -> None:
    """
    Prints both the hosts with the largest amount of CVEs and the
    number of CVEs that those hosts have

    Parameters:
        file (str): JSON file containing the host and CVE information

    Returns:
        None
    """

    count = {}
    maxHosts = []
    maxNumVulns = 0

    with open(file, "r") as f:
        data = json.load(f)
        for host in data:
            count[host] = len(data[host])

    for host in count:
        if count[host] > maxNumVulns:
            maxNumVulns = count[host]
            maxHosts = [host]
        elif count[host] == maxNumVulns:
            maxHosts.append(host)
        else:
            pass

    print(maxHosts, maxNumVulns)
