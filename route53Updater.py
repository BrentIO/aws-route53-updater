from requests import get
from datetime import datetime
import json
import boto3
import botocore
import socket
import logging
import logging.handlers as handlers
import os

##########################################################################################
## AWS Route 53 Updater                                                                 ##
## Copyright 2021, P5 Software                                                          ##
##########################################################################################
## *** Installation ***                                                                 ##
##                                                                                      ##
##    AWS CLI                                                                           ##
##     curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip" ##
##     unzip awscli-bundle.zip                                                          ##
##     sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws             ##
##     aws configure                                                                    ##
##                                                                                      ##
##    Python Requirements                                                               ##
##     pip3 install requests, boto3                                                     ##
##########################################################################################

applicationName = os.path.splitext(os.path.basename(__file__))[0]

logger = logging.getLogger(applicationName)

logger.setLevel(logging.INFO)

#Set Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#Log size maximum is 10MB
logHandler = handlers.RotatingFileHandler(applicationName + '.log', maxBytes=10485760, backupCount=1)

#Set the log level
logHandler.setLevel(logging.INFO)

logHandler.setFormatter(formatter)

logger.addHandler(logHandler)

def main():

    settings = {}
    route53Request = {}

    try:

        #Get the settings file
        with open('route53Updater_settings.json') as settingsFile:
            settings = json.load(settingsFile)

        #Retrieve the IP address from the external server
        ipAddress = get('https://icanhazip.com/').text.strip()

        #Get the IP address from the DNS server for the given DNS name
        resolvingIP = socket.gethostbyname(settings['name'])

        if ipAddress == resolvingIP:
            message = "External IP: " + ipAddress + ".  Resolving IP: " + resolvingIP + ".  No update necessary; Exiting."
            logger.info(message)
            print(message)
            quit()
        else:
            logger.info("External IP: " + ipAddress + ".  Resolving IP: " + resolvingIP + ".  DNS update required.")

        #Create the route 53 request
        route53Request['Comment'] = "Update " + str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        route53Request['Changes'] = []
        change = {}
        change['Action'] = "UPSERT"
        change['ResourceRecordSet'] = {}
        change['ResourceRecordSet']['Name'] = settings['name']
        change['ResourceRecordSet']['Type'] = settings['type']
        change['ResourceRecordSet']['TTL'] = settings['ttl']
        change['ResourceRecordSet']['ResourceRecords'] = []
        resourceRecord = {}
        resourceRecord['Value'] = ipAddress

        change['ResourceRecordSet']['ResourceRecords'].append(resourceRecord)
        route53Request['Changes'].append(change)

        client = boto3.client('route53')
        response = client.change_resource_record_sets(HostedZoneId = settings['zoneId'], ChangeBatch=route53Request)

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            message = settings['name'] + " Status: " + response['ChangeInfo']['Status']
            logger.info(message)
            print(message)

    except botocore.exceptions.ClientError as r53Ex:
        message = r53Ex.response['Error']['Message']
        logger.error(message)
        print(message)
        quit()
    
    except Exception as ex:
        message = ex
        logger.error(message)
        print(message)
        quit()

if __name__ == "__main__":
    main()