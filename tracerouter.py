import argparse
import subprocess
import re


def decode_line(line):
    decoded_line = line.decode('CP866')
    print(decoded_line)
    match_ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", decoded_line)
    match_miss = re.findall(r"\* {8}\* {8}\*", decoded_line)
    if match_ip:
        return match_ip
    elif match_miss:
        return "****"


def trace(address: str):
    route = []
    data = subprocess.check_output(["tracert", address]).splitlines()
    for line in data:
        dec_line = decode_line(line)
        if dec_line is not None:
            route.append(dec_line)
    route = route[1:]
    return route


def main():
    parser = argparse.ArgumentParser(description="Tracerouter")
    parser.add_argument("address", help="IP-address or domain name")
    args = parser.parse_args()
    return trace(args.address)


if __name__ == '__main__':
    print(main())
