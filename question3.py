import json


def countCommonVulns(file: str):

    count = {}

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

    print(json.dumps(count, indent=4))


def countCommonYears(file: str):

    count = {}

    # compile the number of each existing vulneralbility by year
    with open(file, "r") as f:
        data = json.load(f)
        for host in data:
            for vuln in data[host]:
                date = vuln[4:8]
                if data[host][vuln]:
                    if date in count:
                        count[date] += 1
                    else:
                        count[date] = 1

    print(json.dumps(count, indent=4))


if __name__ == "__main__":
    countCommonVulns("152.46.3.0/data/vulnerabilities.json")
    countCommonYears("152.46.3.0/data/vulnerabilities.json")
