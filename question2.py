import requests
import json
from censys.search import CensysHosts

# import matplotlib.pyplot as plt
# import numpy as np

##### Graphing #####


### Censys API HTTP Connection
def getAggregateData(block: str, field: str):
    host = CensysHosts()  # create instance of Censys Host
    result = {}

    # Get all hosts on a block
    query = host.aggregate(block, field, 500)

    # iterate through each 'bucket' in JSON data
    for bucket in query["buckets"]:
        result[bucket["key"]] = bucket["count"]

    return result


def main():
    protocolCounts = getAggregateData(
        block="ip: 152.14.0.0/16", field="services.service_name"
    )
    # graph data
    # graphFromDict(protocolCounts)

    #


if __name__ == "__main__":
    main()
