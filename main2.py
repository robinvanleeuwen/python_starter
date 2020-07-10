import argparse
import configparser
import json
import sys

import requests


def show_ini_file_help(ini_file: str):
    print(f"Failed to retrieve API credentials from '{ini_file}'")
    print()
    print("The .ini file should have the following sections and options:")
    print("-" * 80)
    print("[credentials]")
    print("api_key = my_very_difficulty_api_key_string")
    print("interface_id = my_interface_id_number")
    print("-" * 80)


def main(case_id: int, ini_file: str):
    # Read the ini-file
    config = configparser.ConfigParser()
    config.read(ini_file)

    # Try to get arguments from the read ini-file
    try:
        api_key = config.get("credentials", "api_key")
        interface_id = config.get("credentials", "interface_id")
    # If that fails run a function and exit the program
    except Exception as e:
        show_ini_file_help(ini_file)
        sys.exit(1)

    # Reading the ini file and getting the credentials went well...
    # So continue with what you already had:

    headers = {
        'API-Key': api_key,
        'API-Interface-ID': interface_id
    }

    url = f"https://beheercursus.zaaksysteem.net/api/v1/case/get_by_number/{case_id}"

    print("-" * 80)
    print(f"Getting information about case {case_id} from API...")

    response = requests.request("GET", url, headers=headers)
    status_code = response.status_code

    # Because we always want the ["result"] section you can do:
    result = json.loads(response.text)["result"]  # <--- Immediatly get the ["result"] section

    # Instead of: result = json.loads(response.text)
    # and then every time type: result["result"]["the_section_that_i_need"]
    #                         : result["result"]["another_section_that_i_need"]

    # If the status code is not 200, something went wrong...
    if status_code != 200:
        print("-" * 80)
        print(f"Failure executing request...")
        print("-" * 80)
        print(f"Error Message : {result['instance']['message']}")
        print(f"Error Type    : {result['instance']['type']}")
        print("-" * 80)

        sys.exit(1)

    print("-" * 80)
    case_uuid = result["instance"]["id"]
    print(f"The UUID of case {case_id}: {case_uuid}")
    print("-" * 80)


if __name__ == "__main__":

    # Initialize parser
    parser = argparse.ArgumentParser()

    # Add some command line arguments that can be used
    parser.add_argument("--case", help="The case ID (default: 783)")
    parser.add_argument("--ini", help="The .ini file (default: 'my_ini_file.ini')")

    # Parse the given arguments, if any
    args = parser.parse_args()

    # If no --case <id> is given, default to case_id 783
    if args.case is None:
        args.case = 783

    # If no --ini <file> is given, default to "my_ini_file.ini"
    if args.ini is None:
        args.ini = "my_ini_file.ini"

    # Run the main - function
    main(case_id=args.case, ini_file=args.ini)
