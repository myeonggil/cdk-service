#!/usr/bin/env python3

from aws_cdk import core
import aws_account
from cdk_service.cdk_service_stack import CdkServiceStack

# ju, 210430, 프로필 정보(계정 번호, 리전)
ACCOUNT = aws_account.ACCOUNT
env_info = core.Environment(account=ACCOUNT, region='ap-northeast-2')

app = core.App()
CdkServiceStack(app, "cdkService", env=env_info)

app.synth()
