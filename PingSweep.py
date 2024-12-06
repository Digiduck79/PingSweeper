#!/usr/bin/env python3

import argparse
import ipaddress
import socket
from ping3 import ping
from concurrent.futures import ThreadPoolExecutor

# Timeout for the ping request (in seconds)
timeout = 1

# ASCII Art for "Action ipscan"
ascii_art = """
      .aMMMb  .aMMMb dMMMMMMP dMP .aMMMb  dMMMMb
     dMP"dMP dMP"VMP   dMP   amr dMP"dMP dMP dMP
    dMMMMMP dMP       dMP   dMP dMP dMP dMP dMP
   dMP dMP dMP.aMP   dMP   dMP dMP.aMP dMP dMP
  dMP dMP  VMMMP"   dMP   dMP  VMMMP" dMP dMP

      dMP dMMMMb  .dMMMb  .aMMMb  .aMMMb  dMMMMb
     amr dMP.dMP dMP" VP dMP"VMP dMP"dMP dMP dMP
    dMP dMMMMP"  VMMMb  dMP     dMMMMMP dMP dMP
   dMP dMP     dP .dMP dMP.aMP dMP dMP dMP dMP
  dMP dMP      VMMMP"  VMMMP" dMP dMP dMP dMP
"""


# Function to check if a port is open on a given host
def check_ports(ip_str, ports_to_check):
    open_ports = []
    for port in ports_to_check:
        try:
            # Try to connect to the port using socket
            sock = socket.create_connection((ip_str, port), timeout=timeout)
            open_ports.append(port)
            sock.close()  # Close the connection if successful
        except (socket.timeout, socket.error):
            continue  # Skip if port is closed or connection fails
    return open_ports


# Function to ping the host and check for open ports
def ping_host(ip_str, ports_to_check):
    try:
        # Ping the host to check if it's reachable
        response_time = ping(ip_str, timeout=timeout)
        if response_time is not None:
            # If reachable, check for open ports
            open_ports = check_ports(ip_str, ports_to_check)
            if open_ports:
                ports_str = ', '.join(str(port) for port in open_ports)
                message = f"{ip_str} is reachable, response time: {response_time:.2f} ms, open ports: {ports_str}"
            else:
                message = f"{ip_str} is reachable, response time: {response_time:.2f} ms"
            return message, ip_str  # Return the message along with the IP address
    except Exception:
        # Skip unreachable or errored hosts without logging them
        return None


def ping_sweep(subnet, ports_to_check):
    network = ipaddress.ip_network(subnet, strict=False)

    # List to store the results and IPs
    results = []

    # Using ThreadPoolExecutor to run the pings and port checks in parallel
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Submit all tasks for pinging the hosts and checking ports
        future_results = executor.map(lambda ip: ping_host(str(ip), ports_to_check), network.hosts())

        # Collect the results
        for result in future_results:
            if result is not None:
                results.append(result)

    # Sort the results by IP in ascending order
    results.sort(key=lambda x: ipaddress.IPv4Address(x[1]))

    return results


def display_results(results, output_file=None):
    # Print the ASCII art first
    print(ascii_art)

    # Print or write the results to the console or file
    if output_file:
        with open(output_file, 'w') as f:
            f.write(ascii_art)  # Include the ASCII art in the output file
            f.write("Ping Sweep Results:\n")
            f.write("--------------------\n")
            for message, _ in results:
                f.write(message + '\n')
    else:
        print("Ping Sweep Results:")
        print("--------------------")
        for message, _ in results:
            print(message)


def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Perform a ping sweep across a subnet and check open ports.")
    parser.add_argument("subnet", help="The base IP of the subnet to scan (e.g., 192.168.1.0/24)")
    parser.add_argument("-o", "--output", help="File to output the results to", type=str)
    parser.add_argument("-p", "--ports", help="Comma-separated list of port numbers to scan (e.g., 22,80,443)",
                        type=str, default="80,443")
    args = parser.parse_args()

    # Parse the custom ports list
    ports_to_check = [int(port) for port in args.ports.split(",")]

    # Run the ping sweep
    results = ping_sweep(args.subnet, ports_to_check)

    # Display or output the results
    display_results(results, args.output)


if __name__ == "__main__":
    main()
