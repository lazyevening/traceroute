import argparse
import subprocess
import re
import ipwhois


def get_AS_info(ip):
    obj = ipwhois.IPWhois(ip)
    res = obj.lookup_whois()
    return res["asn"] + " COUNTRY: " + str(res['nets'][0]["country"]) + " CITY: " + str(res['nets'][0]["city"])


def decode_line(line):
    decoded_line = line.decode('CP866')
    match_local_ip = re.findall(r"192\.168\.\d{1,3}\.\d{1,3}", decoded_line)
    match_ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", decoded_line)
    match_miss = re.findall(r"\* {8}\* {8}\*", decoded_line)
    if match_local_ip:
        return f"IP: {match_ip[0]}, ASN: Local"
    elif match_ip:
        return f"IP: {match_ip[0]}, ASN: {get_AS_info(match_ip[0])}"
    elif match_miss:
        return f"****"


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
    for line in main():
        print(line)
