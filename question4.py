import dns.resolver


def resolveIPFromDNS(name: str) -> None:
    """
    Resolve an IP address from a given DNS name

    Parameters:
        name (str): DNS name to get IP from

    Returns:
        None
    """

    result = dns.resolver.query(name, "A")

    # Print the record
    for val in result:
        print("A Record : ", val.to_text())
