import requests
import re

from aws_cdk import CfnOutput, Stack
from aws_cdk import (
    aws_ec2 as ec2
)
from constructs import Construct

res = requests.get("http://ipconfig.kr")
myip = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', res.text)[1]


class CdkSecurityGroupStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.security_group = ec2.SecurityGroup(
            self,
            construct_id,
            vpc=vpc,
            security_group_name="ec2"
        )
        self.security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(f'{myip}/32'),
            connection=ec2.Port.tcp(22)
        )
