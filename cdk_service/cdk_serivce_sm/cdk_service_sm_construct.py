from aws_cdk import (
    aws_secretsmanager,
    core
)
import cdk_service.environment as env


class CdkServiceSMConstruct(core.Stack):
    def __init__(self, scope: core.Construct, name: str) -> None:
        super().__init__(scope, name)

    def create_secretsmanager(self, name):
        secret = aws_secretsmanager.Secret(self, name, **{
            'description': '', # 설명
            'encryption_key': '', # default KMS key
        })
