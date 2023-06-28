# SSHMos

This is a Python script that performs SSH brute-forcing on a list of IP addresses using the Hydra tool. It checks if the IP is alive, determines if SSH anonymous login is allowed, and then attempts to brute-force SSH credentials using a list of usernames and passwords.

## Prerequisites

- Python 3.6 or higher
- Hydra (installed on your system)

## Usage

1. Clone the repository to your local machine.

git clone https://github.com/your-username/ssh-brute-force-tool.git

2. Install the required Python packages.

pip install -r requirements.txt

3.  Prepare your input files:
    Create a text file containing the list of IP addresses, with one IP address per line.
    Create a text file containing the list of usernames, with one username per line.
    Create a text file containing the list of passwords, with one password per line.
   
5.  Run the script with the appropriate command-line arguments.
    Replace ip_addresses.txt with the path to your IP addresses file.
    Replace usernames.txt with the path to your usernames file.
    Replace passwords.txt with the path to your passwords file.
    -p is an optional argument to specify the number of processes to use for concurrent execution (default is 1).
python SSHMos.py ip_addresses.txt -U usernames.txt -P passwords.txt -p 4

## Output

The script will perform the following steps for each IP address:

  Check if the IP is alive and print the result.
  Check if SSH anonymous login is allowed and print the result.
  If anonymous login is not allowed, attempt to brute-force SSH credentials using Hydra.
  If successful credentials are found, print the result.
  If no valid credentials are found, print a message indicating so.

## Disclaimer

This tool is intended for educational and ethical purposes only. The misuse of this tool for any unauthorized activities is strictly prohibited. The author assumes no liability for any damages or misuse of this tool.








   
