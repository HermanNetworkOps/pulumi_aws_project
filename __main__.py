"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import ecs
from pulumi_aws import ec2
import pulumi_awsx as awsx
subnets = 6
# create an AWS resource (VPC)
main = ec2.Vpc("main", cidr_block="10.100.0.0/16")
public_subnets = []
private_subnets = []
for i in range(0, subnets):
    if i % 2 == 0:
        pub_subnet = ec2.Subnet(f"pub_subnet-{i}", vpc_id = main.id, cidr_block = f"10.100.{i + 1}.0/24", availability_zone_id= "use1-az1",
        tags = {
                "Name": "pub_subnets",
               }
        )
        public_subnets.append(pub_subnet)
        
    else:
        priv_subnet = ec2.Subnet(f"priv_subnet-{i}", vpc_id = main.id, cidr_block = f"10.100.{i + 10}.0/24", availability_zone_id= "use1-az3",
        tags = {
            "Name": "priv_subnets",
        }
    )
        private_subnets.append(priv_subnet)

project_gateway = ec2.InternetGateway(
    "project_gateway",
    vpc_id=main.id,
)

public_rt = ec2.RouteTable(
    "project_routetable",
    vpc_id = main.id,
    tags = {
        "Name": "project_routetable",
    }
)
project_eip = ec2.Eip("project_eip", vpc = True)


public_rta = []
for index, subnet in enumerate(public_subnets):
    public_rtas = ec2.RouteTableAssociation(f"public_subnets{index}", route_table_id = public_rt.id, subnet_id = subnet.id)
    public_rta.append(public_rtas)

my_cluster = ecs.Cluster("my_cluster")

