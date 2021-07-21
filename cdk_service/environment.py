import requests, json


data = requests.get("http://ip.jsontest.com/").json()
MY_IP = data['ip'] + '/32'

KEY_NAME = 'mgju-ap-northeast-2-210718'
BASTION_AMI_NAME = ''
SOLR_MASTER_AMI_NAME = ''
SOLR_SLAVE_AMI_NAME = ''
CIDR_BLOCK = '10.0.0.0/16'