from aws_cdk import (
    aws_iam,
    core
)
import cdk_service.environment as env


class CdkServiceIAMConstruct(core.Stack):
    def __init__(self, scope: core.Construct, name: str) -> None:
        super().__init__(scope, name)

    def create_policy(self):
        policy = aws_iam.CfnPolicy(self, name, **{
            'policy_document': '',
            'policy_name': '',
            'groups': '',
            'users': ''
        })
