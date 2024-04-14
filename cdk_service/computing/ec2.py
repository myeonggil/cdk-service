from aws_cdk import CfnOutput, Stack
from aws_cdk import (
    aws_ec2 as ec2
)
from constructs import Construct

ec2_type = "t2.micro"
key_name = ""
linux_ami = ec2.AmazonLinuxImage(
    generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
    edition=ec2.AmazonLinuxEdition.STANDARD,
    virtualization=ec2.AmazonLinuxVirt.HVM,
    storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
)


class CdkEC2Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, sg: ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # create bastion
        self.bastion_instance = ec2.BastionHostLinux(
            self,
            construct_id,
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            instance_name="myBastionLinux",
            instance_type=ec2.InstanceType(instance_type_identifier="t2.micro")
        )

        self.bastion_instance.connections.add_security_group(sg)
