# AWS Route 53 Updater

## About
This script will update an AWS Route 53 domain name to the local IP address of the system executing the script.  This is useful for updating Route 53 domains with dynamic IP addresses.

## Configuration
Update the route53Updater_settings.json file with the ZoneId and domain name to update.  Place the file in the same location as the python file.

## Prereq's
This script requires several prerequisites to function.

### AWS CLI
`curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"`
`unzip awscli-bundle.zip`
`sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws`
`aws configure`

### Python Requirements
`pip3 install requests, boto3`