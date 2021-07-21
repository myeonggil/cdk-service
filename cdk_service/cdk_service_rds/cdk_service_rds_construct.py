from aws_cdk import (
    aws_ec2,
    aws_rds,
    core
)


class CdkServiceRDSConstruct(core.Stack):
    def __init__(self, scope: core.Construct, id: str) -> None:
        super().__init__(scope, id)

        self.pri_rds = rds.DatabaseCluster(self, 'pri-rds', # stack name
            engine=rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_5_7_12), # DB engine(aurora mysql, oracle...) and version
            instance_props={
                "instance_type": ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.SMALL), # EC2 spec
                "vpc_subnets": {
                    "subnet_type": ec2.SubnetType.PRIVATE # private or public
                }, 
                "vpc": self.vpc, # vpc id
                "allow_major_version_upgrade": False, # major version upgrade status
                "auto_minor_version_upgrade": False, # auto version upgrade status
                "publicly_accessible": False, # public access status
                "security_groups": [
                self.rds_sg
                ], # securit groups
                "parameter_group": self.db_param # DB parameter group
            }, 
            instances=2, # HA
            parameter_group=self.db_param, # DB Cluster parameter group
            credentials=rds.Credentials.from_password('admin', core.SecretValue('mgju1q2w3e4r')) # DB id, pw
        )

    def create_subnet_group(self):
        pass

    def create_parameter_group(self):
        pass
