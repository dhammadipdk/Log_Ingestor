# cli/cli.py
import argparse
import json
import requests
from datetime import datetime

BASE_URL = 'http://localhost:3000'

def search_logs(search_criteria):
    url = f'{BASE_URL}/search'
    headers = {'Content-Type': 'application/json'}
    
    # Constructing the payload from the search criteria
    payload = {key: value for key, value in search_criteria.items()}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        
        # Check if the response content is not empty
        if response.text:
            return response.json()
        else:
            print('No results found.')
            return []
    except requests.exceptions.HTTPError as err:
        print(f"Error searching logs: {err.response.text}")
        return []

def filter_logs(filter_criteria):
    url = f'{BASE_URL}/filter'
    filters = {key: value for key, value in filter_criteria.items() if value is not None}

    response = requests.get(url, params=filters)

    try:
        response.raise_for_status()
        
        # Check if the response content is not empty
        if response.text:
            return response.json()
        else:
            print('No results found.')
            return []
    except requests.exceptions.HTTPError as err:
        print(f"Error filtering logs: {err.response.text}")
        return []

def ingest_log(log_data):
    url = f'{BASE_URL}/ingest'
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=json.dumps(log_data), headers=headers)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.HTTPError as err:
        print(f"Error ingesting log: {err.response.text}")

def display_results(logs):
    if not logs:
        print('No results found.')
        return

    for log in logs:
        print(log)

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def main():
    parser = argparse.ArgumentParser(description='Log Query CLI')
    parser.add_argument('--search', help='Perform a search with key-value pairs (e.g., --search level=error message="Failed to connect")')
    parser.add_argument('--filter-level', help='Filter logs by level')
    parser.add_argument('--filter-resourceId', help='Filter logs by resourceId')
    parser.add_argument('--filter-timestamp', help='Filter logs by timestamp')
    parser.add_argument('--filter-traceId', help='Filter logs by traceId')
    parser.add_argument('--filter-spanId', help='Filter logs by spanId')
    parser.add_argument('--filter-message', help='Filter logs by message')
    parser.add_argument('--filter-commit', help='Filter logs by commit')
    parser.add_argument('--filter-parentResourceId', help='Filter logs by parentResourceId')
    parser.add_argument('--ingest-json', help='Ingest log data from a JSON string')
    parser.add_argument('--ingest-file', help='Ingest log data from a JSON file')

    args = parser.parse_args()

    logs = []

    if args.search:
        search_criteria = {}
        pairs = args.search.split()
        i = 0
        while i < len(pairs):
            elements = pairs[i].split('=')
            if len(elements) == 2:
                key, value = elements
                # Handling values with spaces
                while i + 1 < len(pairs) and '=' not in pairs[i + 1]:
                    i += 1
                    value += ' ' + pairs[i]
                search_criteria[key] = value
            else:
                print(f"Ignoring invalid search criteria: {pairs[i]}")

            i += 1

        logs = search_logs(search_criteria)
    elif any(vars(args).values()):
        filter_criteria = {
            'level': args.filter_level,
            'resourceId': args.filter_resourceId,
            'traceId': args.filter_traceId,
            'spanId': args.filter_spanId,
            'message': args.filter_message,
            'commit': args.filter_commit,
            'metadata.parentResourceId': args.filter_parentResourceId,
            'timestamp': args.filter_timestamp
        }

        logs = filter_logs(filter_criteria)
    elif args.ingest_json:
        log_data = json.loads(args.ingest_json)
        ingest_log(log_data)
    elif args.ingest_file:
        log_data = load_json_file(args.ingest_file)
        ingest_log(log_data)
    else:
        print('Please provide a valid command. Use --help for assistance.')

    display_results(logs)

if __name__ == '__main__':
    main()