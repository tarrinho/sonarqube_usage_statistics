# 2021-07-09 - Pedro Tarrinho - Goal - extract all events from Sonarqube in order to generate statistics of usage

import json
import time
import subprocess
import os

date = "3021-04-08T18:17:07%2B0000"
# define an environment variable like:  export SONARQUBE_TOKEN="token"
token = os.getenv('SONARQUBE_TOKEN') 
# define an environment variable like:  export SONARQUBE_URL="url"
url = os.getenv('SONARQUBE_URL') 
number_entries = "1000"
curl = "/usr/bin/curl"
print('count ; id_number ; componentName ; status ; submittedAt ; executedAt ; executedTimeMs ; submitterLogin ;  hasScannerContext ; warningCount')
id_number=0;
while True:
    command = curl + ' -u ' + token +': ' + url + '?ps=' + number_entries + '\&type=REPORT\&maxExecutedAt=' + date + ' 2>/dev/null'

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.stdout.read()
    try:
        full_json_with_tasks = json.loads(output)
    except:
        print("error")
    
    try:
        full_json = full_json_with_tasks['tasks']
    except:
        print("error")
        break

    # if no more tasks break while
    if full_json == [] : 
        break

    for entry in full_json:
    
        entry_parsed = json.loads(json.dumps(entry))
        try:
            id_number += 1
            print(id_number, ";" , entry_parsed['id'], " ; ", entry_parsed['componentName'], " ; " , entry_parsed['status'], " ; " , entry_parsed['submittedAt'], " ; " , entry_parsed['executedAt'], " ; " , entry_parsed['executionTimeMs'], " ; " , entry_parsed['submitterLogin'][:-5], " ; " , entry_parsed['hasScannerContext'], " ; " , entry_parsed['warningCount'])
            last_entry_date = entry_parsed['submittedAt']
        except:
            print("EXCEPTION: field not found - ", entry_parsed['id'])
            break

    date = last_entry_date.replace("+","%2B")
#print("Total: " , id_number)
