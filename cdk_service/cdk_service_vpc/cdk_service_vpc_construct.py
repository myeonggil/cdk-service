from aws_cdk import (
    aws_ec2,
    core
)
import cdk_service.environment as env

CIDR_BLOCK = env.CIDR_BLOCK
CIDRS = {
    'MYIP': env.MY_IP
}

class CdkServiceVpcConstruct(core.Stack):
    def __init__(self, scope: core.Construct, id: str) -> None:
        super().__init__(scope, id)

    def _create_vpc(self):
        aws_ec2.Vpc(self, vpc, 
            cidr=CIDR_BLOCK, 
            max_azs=2, # number of availability zone(ap-northeast-2a, ap-northeast-2b) 
            nat_gateways=2, # number of network address translation per availability zone 
            subnet_configuration=[
            {
                'subnetType': aws_ec2.SubnetType.PRIVATE, # type of subnet(private or public)
                'cidrMask': 24, # number of prefix(/24, /20, ...)
                'name': 'private' # name of subnet(str)
            },
            {
                'subnetType': aws_ec2.SubnetType.PUBLIC, # type of subnet(private or public)
                'cidrMask': 24, # number of prefix(/24, /20, ...)
                'name': 'public' # name of subnet(str)
            }]
      )

    def _create_securitygroup(self):
        aws_ec2.SecurityGroup(self, 'bastion', # stack name
            vpc=self.vpc, # vpc object
            security_group_name='bastion', # security group name
            description='Security group for EC2 bastion' # description for 
        )
        bastion_securitygroup.add_ingress_rule(aws_ec2.Peer.ipv4(CIDRS['MYIP']), # allow inbound ipv4/prefix
            aws_ec2.Port.tcp(22) # protocol number
        )
        bastion_securitygroup.add_ingress_rule(aws_ec2.Peer.ipv4('10.0.0.0/8'), # allow inbound ipv4/prefix
            aws_ec2.Port.tcp(22) # protocol number
        )
