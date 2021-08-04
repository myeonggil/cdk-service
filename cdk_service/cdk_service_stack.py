import environment as env
from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds, 
    core
)
CIDR_BLOCK = env.CIDR_BLOCK
CIDRS = {
    'MYIP': env.MY_IP
}


class CdkServiceStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # create vpc sevice
        self.vpc, self.pri_sub, self.pub_sub = self.create_vpc()

        # create securitygroup service
        self.bastion_sg, self.rds_sg = self.create_securitygroup()

        # create bastion ec2
        self.create_ec2()

        # create rds subnet group
        self.pri_rds_sub, self.pub_rds_sub = self.create_subnet_group()

        # create rds param group
        self.db_param = self.create_parameter_group()

        # create rds
        self.pri_rds, self.pub_rds = self.create_rds()

    def create_vpc(self):
        pri_subnetids = []
        pub_subnetids = []
        vpc = ec2.Vpc(self, 'vpc', cidr=CIDR_BLOCK,
                      max_azs=2,
                      nat_gateways=2,
                      subnet_configuration=[
                        {
                            'subnetType': ec2.SubnetType.PRIVATE,
                            'cidrMask': 24,
                            'name': 'private'
                        },
                        {
                            'subnetType': ec2.SubnetType.PUBLIC,
                            'cidrMask': 24,
                            'name': 'public'
                        }]
        )
        pri_selection = vpc.select_subnets(
            subnet_type=ec2.SubnetType.PRIVATE
        )
        pub_selection = vpc.select_subnets(
            subnet_type=ec2.SubnetType.PUBLIC
        )
        for selection in pri_selection.subnets:
            pri_subnetids.append(selection.subnet_id)
        for selection in pub_selection.subnets:
            pub_subnetids.append(selection.subnet_id)
        
        return vpc, pri_subnetids, pub_subnetids

    def create_securitygroup(self):
        bastion_securitygroup = ec2.SecurityGroup(self, 'sg-bastion', vpc=self.vpc,
            security_group_name='bastion',
            description='Security group for EC2 bastion'
        )
        bastion_securitygroup.add_ingress_rule(ec2.Peer.ipv4(CIDRS['MYIP']), ec2.Port.tcp(22))
        bastion_securitygroup.add_ingress_rule(ec2.Peer.ipv4('10.0.0.0/8'), ec2.Port.tcp(22))

        rds_securitygroup = ec2.SecurityGroup(self, 'sg-rds', vpc=self.vpc,
            security_group_name='rds',
            description='Security group for RDS'
        )
        rds_securitygroup.add_ingress_rule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(3306))


        return bastion_securitygroup, rds_securitygroup

    def create_ec2(self):
        bastion = ec2.Instance(self, 'bastion', **{
            'instance_name': 'bastion',
            'vpc': self.vpc,
            'instance_type': ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE4_GRAVITON, ec2.InstanceSize.NANO),
            'vpc_subnets': {'subnet_type': ec2.SubnetType.PUBLIC},
            'security_group': self.bastion_sg,
            'machine_image': ec2.GenericLinuxImage({
                # bastion from default
                'ap-northeast-2': 'ami-065bbf792e2f70fd9'
            }),
            'key_name': env.KEY_NAME
        })

        # return bastion

    def create_subnet_group(self):
        pri_rds_sub = rds.CfnDBSubnetGroup(self, 'pri-subnet-group', 
            db_subnet_group_description='DB subnet area for internal', 
            subnet_ids=self.pri_sub, 
            db_subnet_group_name='pri-subnet-group'
        )
        pub_rds_sub = rds.CfnDBSubnetGroup(self, 'pub-subnet-group', 
            db_subnet_group_description='DB subnet area for public', 
            subnet_ids=self.pub_sub, 
            db_subnet_group_name='pub-subnet-group'
        )

        return pri_rds_sub, pub_rds_sub

    def create_parameter_group(self):
        db_param_group = rds.ParameterGroup(self, 'aurora-db-mysql57', 
            engine=rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_5_7_12), 
            description='parameter group for db instance', 
            parameters={
                'max_connections': '2000'
            }
        )

        return db_param_group

    def create_rds(self):
        pri_rds = None
        pri_rds = rds.DatabaseCluster(self, 'pri-rds', 
            engine=rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_5_7_12), 
            instance_props={
                "instance_type": ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.SMALL), 
                "vpc_subnets": {
                    "subnet_type": ec2.SubnetType.PRIVATE
                }, 
                "vpc": self.vpc, 
                "allow_major_version_upgrade": False, 
                "auto_minor_version_upgrade": False, 
                "publicly_accessible": False, 
                "security_groups": [self.rds_sg], 
                "parameter_group": self.db_param
            }, 
            instances=2, 
            parameter_group=self.db_param, 
            credentials=rds.Credentials.from_password('admin', core.SecretValue('mgju1q2w3e4r'))
        )
        pub_rds = None
        # pub_rds = rds.DatabaseCluster(self, 'pub-rds', 
        #     engine=rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_5_7_12), 
        #     instance_props={
        #         "instance_type": ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE4_GRAVITON, ec2.InstanceSize.NANO), 
        #         "vpc_subnets": {
        #             "subnet_type": ec2.SubnetType.PUBLIC
        #         }, 
        #         "vpc": self.vpc, 
        #         "allow_major_version_upgrade": False, 
        #         "auto_minor_version_upgrade": False, 
        #         "publicly_accessible": True
        #     }, 
        #     instances=2, 
        #     parameter_group=self.db_param
        # )

        return pri_rds, pub_rds

