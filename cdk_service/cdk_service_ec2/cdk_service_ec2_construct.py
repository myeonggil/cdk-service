from aws_cdk import (
    aws_ec2,
    aws_elasticloadbalancingv2,
    core
)
import cdk_service.environment as env

solrMasterAmi = aws_ec2.GenericLinuxImage({
    # graviton solr master from maimovie us-west-1
    'ap-northeast-2': env.SOLR_MASTER_AMI_NAME
})
solrSlaveAmi = aws_ec2.GenericLinuxImage({
    # graviton solr slave from maimovie us-west-1
    'ap-northeast-2': env.SOLR_SLAVE_AMI_NAME
})


class CdkServiceEC2Construct(core.Stack):
    def __init__(self, scope: core.Construct, name: str, vpc: object, securitygroup: object) -> None:
        super().__init__(scope, name)

        self.vpc = vpc
        # self.id = id
        self.bastion = aws_ec2.Instance(self, name, **{
            'instance_name': 'bastion',
            'vpc': self.vpc,
            'instance_type': aws_ec2.InstanceType.of(aws_ec2.InstanceClass.BURSTABLE4_GRAVITON, aws_ec2.InstanceSize.NANO),
            'vpc_subnets': {'subnet_type': aws_ec2.SubnetType.PUBLIC},
            'security_group': securitygroup,
            'machine_image': aws_ec2.GenericLinuxImage({
                # bastion from ssgcelebs
                'ap-northeast-2': 'ami-065bbf792e2f70fd9'
            }),
            'key_name': env.KEY_NAME
        })

    def create_solr(self, solr_securitygroup):
        # ju, 210429, 어떤 버티컬의 솔라를 생성할 것인가?
        # master solr
        self.solr_maimovie_kr_master = aws_ec2.Instance(self, 'finder-maimovie-kr', **{
            'instance_name': 'finder-maimovie-kr',
            'vpc': self.vpc,
            'instance_type': aws_ec2.InstanceType.of(aws_ec2.InstanceClass.MEMORY6_GRAVITON, aws_ec2.InstanceSize.LARGE),
            'vpc_subnets': {'subnet_type': aws_ec2.SubnetType.PUBLIC},
            'security_group': solr_securitygroup,
            'machine_image': solrMasterAmi,
            'key_name': 'triphi-ap-northeast-2'
        })

        self.solr_maimovie_kr_master = aws_ec2.Instance(self, 'finder-maimovie-kr-tv', **{
            'instance_name': 'finder-maimovie-kr-tv',
            'vpc': self.vpc,
            'instance_type': aws_ec2.InstanceType.of(aws_ec2.InstanceClass.MEMORY6_GRAVITON, aws_ec2.InstanceSize.LARGE),
            'vpc_subnets': {'subnet_type': aws_ec2.SubnetType.PUBLIC},
            'security_group': solr_securitygroup,
            'machine_image': solrMasterAmi,
            'key_name': 'triphi-ap-northeast-2'
        })

        self.solr_maimovie_kr_master = aws_ec2.Instance(self, 'rest-voice-finder-maimovie-kr', **{
            'instance_name': 'rest-voice-finder-maimovie-kr',
            'vpc': self.vpc,
            'instance_type': aws_ec2.InstanceType.of(aws_ec2.InstanceClass.MEMORY6_GRAVITON, aws_ec2.InstanceSize.LARGE),
            'vpc_subnets': {'subnet_type': aws_ec2.SubnetType.PUBLIC},
            'security_group': solr_securitygroup,
            'machine_image': solrMasterAmi,
            'key_name': 'triphi-ap-northeast-2'
        })

        # slave solr, 2개의 가용영역으로
        for idx, zone in enumerate(self.vpc.availability_zones):
            self.solr_maimovie_kr_slave = aws_ec2.Instance(self, f'finder-maimovie-kr-slave-{idx}', **{
                'instance_name': f'finder-maimovie-kr-slave-{idx}',
                'vpc': self.vpc,
                'instance_type': aws_ec2.InstanceType.of(aws_ec2.InstanceClass.MEMORY6_GRAVITON, aws_ec2.InstanceSize.LARGE),
                'vpc_subnets': {'subnet_type': aws_ec2.SubnetType.PRIVATE},
                'availability_zone': zone,
                'security_group': solr_securitygroup,
                'machine_image': solrSlaveAmi,
                'key_name': env.KEY_NAME
            })

            self.solr_maimovie_kr_tv_slave = aws_ec2.Instance(self, f'finder-maimovie-kr-tv-slave-{idx}', **{
                'instance_name': f'finder-maimovie-kr-tv-slave-{idx}',
                'vpc': self.vpc,
                'instance_type': aws_ec2.InstanceType.of(aws_ec2.InstanceClass.MEMORY6_GRAVITON,
                                                         aws_ec2.InstanceSize.LARGE),
                'vpc_subnets': {'subnet_type': aws_ec2.SubnetType.PRIVATE},
                'availability_zone': zone,
                'security_group': solr_securitygroup,
                'machine_image': solrSlaveAmi,
                'key_name': env.KEY_NAME
            })

            self.solr_maimovie_kr_voice_finder_slave = aws_ec2.Instance(self, f'rest-voice-finder-maimovie-kr-slave-{idx}', **{
                'instance_name': f'rest-voice-finder-maimovie-kr-slave-{idx}',
                'vpc': self.vpc,
                'instance_type': aws_ec2.InstanceType.of(aws_ec2.InstanceClass.MEMORY6_GRAVITON,
                                                         aws_ec2.InstanceSize.LARGE),
                'vpc_subnets': {'subnet_type': aws_ec2.SubnetType.PRIVATE},
                'availability_zone': zone,
                'security_group': solr_securitygroup,
                'machine_image': solrSlaveAmi,
                'key_name': env.KEY_NAME
            })

    def create_target_group(self, name, vpc_id):
        target_group = aws_elasticloadbalancingv2.CfnTargetGroup(self, name, **{
            'name': name,
            'targets': '',
            'target_type': '',
            'vpc_id': vpc_id,
            'port': 9100, # number of port
            'protocol': 'HTTP', # HTTP, TCP, UDP...
            'protocol_version': 'HTTP1'  # HTTP1, HTTP2, GRPC
        })

    def create_elastic_loadbalancer(self, name, Cfnvpc):
        # application
        application_load_balancer = aws_elasticloadbalancingv2.ApplicationLoadBalancer(self, name, **{
            'http2_enabled': '', # True, False
            'idle_timeout': 60, # default 60 seconds
            'ip_address_type': 'Ipv4', # Ipv4, Ipv6
            'security_group': '', # security_group id
            'vpc': Cfnvpc.vpc.vpc_id, # vpcid
            'vpc_subnets': '', # vpc_subnetid
            'load_balancer_name': name,
            'internet_facing': '' # True(public) or False(private)
        })

        # network
        network_load_balancer = aws_elasticloadbalancingv2.NetworkLoadBalancer(self, name, **{
            'cross_zone_enable': '', # 교차 가용영역 부하분산 True, False
            'vpc': Cfnvpc.vpc.vpc_id, # vpcid,
            'vpc_subnets': '', # vpc_subnetid
            'internet_facing': ''  # True(public) or False(private)
        })
