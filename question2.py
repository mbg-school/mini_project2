import requests
import json
from censys.search import CensysHosts
import pandas as pd
import matplotlib.pyplot as plt

##### Graphing #####
def createBarGraph(file: str, title: str, num4Other: int = None):
    """
    Creates a Bar Graph from JSON data (file), which will optionally group those values <= num4Other into 'Other'
    category and remove them from original JSON data.
    
    Parameters:
        file (str): the JSON file to read the data from
        title (str): the title of the bar graph 
        num4Other (int): (optional) the number of entries to be aggregated into the "others" category 
    """
    # load file as dict
    with open(file, "r") as f:
        rawJsonData = json.load(f)

    jsonData = rawJsonData.copy()
    otherCount = 0
    otherKeys = []
    if num4Other:
        for key in rawJsonData.keys():
            if rawJsonData[key] <= num4Other:
                count = jsonData.pop(key)  # remove from list, add to 'others'
                otherCount += count
                otherKeys.append(key)

        # Add 'Others' key and value
        jsonData["Others"] = otherCount
        print(
            "The following keys were less than "
            + str(num4Other)
            + " and were aggregated into 'Others': \nexit"
            + str(otherKeys)
        )

    # convert to dataFrame
    df = pd.DataFrame({"Type": jsonData.keys(), "Count": jsonData.values()})
    ax = df.plot.bar(x="Type", y="Count", rot=0)

    # put count as text at top of each bar
    for index, value in enumerate(jsonData.values()):
        plt.text(index - 0.05, value + 1, str(value))

    plt.title(title)
    plt.show()  # show resulting bar chart


def createPieChart(file: str, title: str, num4Other: int = None):
    """
    Creates a Pie Chart from JSON data (file), which will optionally group those values <= num4Other into 'Other'
    category and remove them from original JSON data.
    
    Parameters:
        file (str): the JSON file to read the data from
        title (str): the title of the bar graph 
        num4Other (int): (optional) the number of entries to be aggregated into the "others" category 
    """
    # load file as dict
    with open(file, "r") as f:
        rawJsonData = json.load(f)

    jsonData = rawJsonData.copy()
    otherCount = 0
    otherKeys = []
    if num4Other:
        for key in rawJsonData.keys():
            if rawJsonData[key] <= num4Other:
                count = jsonData.pop(key)  # remove from list, add to 'others'
                otherCount += count
                otherKeys.append(key)

        # Add 'Others' key and value
        jsonData["Others"] = otherCount
        print(
            "The following keys were less than "
            + str(num4Other)
            + " and were aggregated into 'Others': \nexit"
            + str(otherKeys)
        )

    # convert to dataFrame
    df = pd.DataFrame({"Type": jsonData.keys(), "Count": jsonData.values() }, index=jsonData.keys() )
    ax = df.plot.pie(y="Count",rot=0, labels=None, autopct='%1.1f%%')

    # put count as text at top of each bar
    for index, value in enumerate(jsonData.values()):
        plt.text(index - 0.05, value + 1, str(value))

    plt.title(title)
    plt.legend(labels = jsonData.keys())
    plt.show()  # show resulting bar chart

### Censys API HTTP Aggregate Data Connection
def getAggregateData(block: str, field: str):
    """
    Uses the Censys API aggregation endpoint to aggregate hosts into "buckets" 
    
    Parameters:
        block (str): the IPv4 address block to query for hosts
        field (str): the Censys API aggregation field

    Returns:
        result (dict): Returns a dict with the bucket name (aggregation metric) as the key
                        and the total count of hosts that share that metric as the value. 
    """
    host = CensysHosts()  # create instance of Censys Host
    result = {}

    # Get all hosts on a block
    query = host.aggregate(block, field, 500)

    # iterate through each 'bucket' in JSON data
    for bucket in query["buckets"]:
        key = bucket["key"].lower()
        if key in result:
            result[key] += bucket["count"]
        else:
            result[key] = bucket["count"]

    return result


def saveDataToFile(ipBlock: str, field: str, fileName: str):
    """
    Uses the Censys API aggregation endpoint to aggregate hosts into "buckets" and saves/returns that Data to a JSON file. 
    
    Parameters:
        ipBlock (str): the IPv4 address block to query for hosts
        field (str): the Censys API aggregation field
        fileName (str): the fileName of the JSON file to save the resulting aggregation data

    Returns:
        jsonCounts (dict): Returns a dict with the bucket name (aggregation metric) as the key
                        and the total count of hosts that share that metric as the value. 
    """
    jsonCounts = getAggregateData(block="ip: " + ipBlock, field=field)

    with open(fileName, "w") as f:
        json.dump(jsonCounts, f, indent=4)

    print("Data saved to file: " + fileName)
    return jsonCounts
