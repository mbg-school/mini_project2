import requests
import json
from censys.search import CensysHosts
import pandas as pd
import matplotlib.pyplot as plt

# import matplotlib.pyplot as plt
# import numpy as np

##### Graphing #####

def createBarGraph(file:str, num4Other:int = None):
    """Create a Bar Graph from JSON data (file), which will group those values <= num4Other into 'Other'
        category and remove them from original JSON data."""
    # load file as dict
    with open(file, 'r') as f:
        rawJsonData = json.load(f)

    jsonData = rawJsonData.copy()
    otherCount = 0
    otherKeys = []
    if num4Other:
        for key in rawJsonData.keys():
            if rawJsonData[key] <= num4Other:
                count = jsonData.pop(key) #remove from list, add to 'others'
                otherCount += count
                otherKeys.append(key)
        
        # Add 'Others' key and value
        jsonData['Others'] = otherCount
        print("The following keys were less than " + str(num4Other) + " and were aggregated into 'Others': \n" + str(otherKeys))

    # convert to dataFrame
    df = pd.DataFrame({'Type': jsonData.keys(), 'Count': jsonData.values()})
    ax = df.plot.bar(x='Type', y='Count', rot=0)
    plt.show() # show resulting bar chart

### Censys API HTTP Aggregate Data Connection
def getAggregateData(block: str, field: str):
    host = CensysHosts()  # create instance of Censys Host
    result = {}

    # Get all hosts on a block
    query = host.aggregate(block, field, 500)

    # iterate through each 'bucket' in JSON data
    for bucket in query["buckets"]:
        result[bucket["key"]] = bucket["count"]

    return result


def saveDataToFile(ipBlock:str, field:str, fileName:str):
    jsonCounts = getAggregateData(block="ip: " + ipBlock, field=field)

    with open(fileName, 'w') as f:
        json.dump(jsonCounts, f)

    print("Data saved to file: " + fileName)
    return jsonCounts
