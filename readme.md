# AWS Route 53 Updater

## About
This script will update an AWS Route 53 domain name to the local IP address of the system executing the script.  This is useful for updating Route 53 domains with dynamic IP addresses.

## Configuration
Update the route53Updater_settings.json file with the ZoneId and domain name to update.  Place the file in the same location as the python file.

## Prereq's
This script requires several prerequisites to function.

### AWS CLI
`sudo apt-get install -y awscli python3-pip`

`aws configure`

### Python Requirements
`pip3 install requests boto3`

## IAM Policy
Modify the policy below and attach it to the AWS IAM user that is configured in `aws configure`

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "route53:ChangeResourceRecordSets"
            ],
            "Resource": [
                "arn:aws:route53:::hostedzone/[ZoneID]"
            ]
        }
    ]
}
```
