def find_unused_port(start_range = 4000):
    """Find a port that is not used by gevent. This allows for multiple instances of this app to run at once"""
    import psutil
    # get all used ports from netstat, and filter out the ports that are in use by 'localhost'
    port_blacklist = []
    for netstat in psutil.net_connections():
        if netstat[3][0] == '127.0.0.1':
            port_blacklist.append(netstat[3][1])

    # check if the port is blacklisted
    port_to_try = start_range - 1
    port_open = False
    while port_open == False:
        port_to_try += 1
        if port_to_try not in port_blacklist:
            port_open = True
        print(f"port {port_to_try} is open: {port_open}")
    return port_to_try