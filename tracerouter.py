import argparse
import subprocess
import re


def trace(address: str):
    route = []
    data = subprocess.check_output(["tracert", address]).splitlines()
    for line in data:
        decoded_line = line.decode('CP866')
        # print(decoded_line)
        match = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", decoded_line)
        if match:
            route.append(match)
    route = route[1:]
    return route


def main():
    parser = argparse.ArgumentParser(description="Tracerouter")
    parser.add_argument("address", help="IP-address or domain name")
    args = parser.parse_args()
    return trace(args.address)


if __name__ == '__main__':
    print(main())
