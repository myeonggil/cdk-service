from aws_cdk import (
    aws_ec2,
    core
)
import cdk_service.environment as env

CIDR_BLOCK = env.CIDR_BLOCK
CIDRS = {
    'WORKFLEX': '211.245.120.76/32',
    'MYCELEBS1': '211.202.87.144/32',
    'MYCELEBS2': '211.202.87.145/32'
}


class CdkServiceVpcConstruct(core.Stack):
    @property
    def buckets(self):
        return tuple(self._buckets)

    def __init__(self, scope: core.Construct, id: str) -> None:
        super().__init__(scope, id)