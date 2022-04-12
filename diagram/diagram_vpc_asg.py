from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2, EC2AutoScaling
from diagrams.aws.network import VPC, PrivateSubnet, PublicSubnet, InternetGateway, NATGateway, ElbApplicationLoadBalancer
from diagrams.onprem.compute import Server

# Variables
title = "VPC with 2 public subnets and private subnet \n Private subnet has a autoscaling group for webservers. \n Single application loadbalancer which is high available and therefore in both public subnets"
outformat = "png"
filename = "diagram_vpc_asg"
direction = "TB"


with Diagram(
    name=title,
    direction=direction,
    filename=filename,
    outformat=outformat,
) as diag:
    # Non Clustered
    user = Server("user")

    # Cluster 
    with Cluster("vpc"):
        igw_gateway = InternetGateway("igw")

        with Cluster("Availability Zone: us-east-1b"):
            # Subcluster
            with Cluster("subnet_public2"):
                loadbalancer2 = ElbApplicationLoadBalancer("Application \n Load Balancer")

        with Cluster("Availability Zone: us-east-1a"):
            # Subcluster 
            with Cluster("subnet_public1"):
                loadbalancer1 = ElbApplicationLoadBalancer("Application \n Load Balancer")
                nat_gateway = NATGateway("nat_gateway")
            # Subcluster
            with Cluster("subnet_private1"):
                ec2_asg_web_server = EC2AutoScaling("Autoscaling Group \n Webserver")
 
    # Diagram
    user >> [loadbalancer1, 
             loadbalancer2] >> ec2_asg_web_server 

    ec2_asg_web_server >> nat_gateway >> igw_gateway >> Server("APT Ubuntu")

diag
