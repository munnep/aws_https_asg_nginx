# Manual steps

This document describes the manual steps for creating a autoscaling group with webservers behind an application load balancer which you can then connect to over the internet. The webserver is in a private subnet

See below diagram for how the setup is:
![diagram_vpc_asg.png](diagram_vpc_asg.png)




- Create a VPC with cidr block ```10.233.0.0/16```  
![](media/2021-12-08-13-51-43.png)  
- Create 3 subnets. 2 public subnets and 1 private subnet
    - patrick-public1-subnet (ip: ```10.233.1.0/24``` availability zone: ```us-east-1a```)  
    - patrick-public2-subnet (ip: ```10.233.2.0/24``` availability zone: ```us-east-1b```)  
    - patrick-private1-subnet (ip: ```10.233.11.0/24``` availability zone: ```us-east-1a```)  
![](media/2021-12-08-14-05-39.png)  
![](media/2021-12-08-14-05-55.png)  
![](media/2021-12-08-14-06-08.png)  
![](media/2021-12-08-14-06-23.png)  
- create an internet gateway  
![](media/2021-12-08-14-07-45.png)    
![](media/2021-12-08-14-08-09.png)  
- create a nat gateway which you attach to ```patrick-public1-subnet```   
![](media/2021-12-08-15-20-55.png)  
- create routing table for public  
![](media/2021-12-08-14-10-55.png)  
   - edit the routing table for internet access to the internet gateway
   ![](media/2021-12-08-14-12-18.png)  
- create routing table for private  
   ![](media/2021-12-08-14-13-32.png)  
   - edit the routing table for internet access to the nat gateway  
   ![](media/2021-12-08-14-14-41.png)   
- attach routing tables to subnets  
    - patrick-public-route to public subnets      
    ![](media/2021-12-08-14-16-18.png)      
    - patrick-private-route to private subnet   
     ![](media/2021-12-08-14-17-53.png)    
- create a security group that allows http and https from all locations    
![](media/2021-12-08-14-20-11.png)    
- 




- Auto Scaling - Launch Configurations  
![](media/20220412105223.png)    
- Create launch configuration. 
![](media/20220412105233.png)    
![](media/20220412105357.png)    
```
#cloud-config
runcmd:
  - apt-get install -y nginx
  - systemctl enable --no-block nginx 
  - systemctl start --no-block nginx 
````
![](media/20220412105528.png)    
![](media/20220412105804.png)    
![](media/20220412105841.png)    
- The launch configuration should now be visible  
![](media/20220412105859.png)    



- Import the certificate you want to use on the load balancer
- Go to AWS Certificate Manager  
- Select import   
![](media/20220412110433.png)    
- Copy your certificate information in     
![](media/20220412110524.png)    
- give the tag a name    
![](media/20220412110546.png)    
- review and select import    
![](media/20220412110600.png)    
- Certificate should now be available  
![](media/20220412110614.png)    


- loadbalancer create a target group which we at a later point connect to the Auto Scaling Group  
![](media/20220412110001.png)    
- Will have no targets yet  
![](media/20220412110024.png)    

- loadbalancer create a appplication load balancer which will connect to the load balancer target    
![](media/20220412110719.png)      
- following configuration  
![](media/20220412110756.png)      
![](media/20220412110828.png)      
![](media/20220412111159.png)      
- Auto Scaling groups. Will configure the group and connect it to auto scaling launch and the created load balancer
Make sure you switch to launch configuration   
![](media/20220412112039.png)      
![](media/20220412112100.png)      
![](media/20220412112128.png)    
![](media/20220412112205.png)    
![](media/20220412112237.png)    
![](media/20220412112253.png)    
![](media/20220412112313.png)    
![](media/20220412112326.png)    
- You should now see an instance being started   
![](media/20220412113300.png)       
- Alter the DNS record in route53 to point to the loadbalancer dns name    
![](media/20220412113441.png)    
- You should now be able to connect to your website   


### Test the autoscaling

After everything is working you should see one web server running and one web server as a target in the load balancer target group

EC2   
![](media/20220412113820.png)    

Load balancer target  
![](media/20220412113839.png)    

**Change the Auto scaling group to have 2 servers**
- Edit your Auto scaling group  
- Change the desired capacity to 2  
![](media/20220412113904.png)    

- After that you should see 2 EC2 instances and load balancer target with 2 instances    
![](media/20220412114410.png)  























- Auto Scaling groups. Will configure the group and connect it to auto scaling launch and the created load balancer  


- loadbalancer generated a DNS name which you can use to connect to the application server  


### Test the autoscaling

After everything is working you should see one web server running and one web server as a target in the load balancer target group

EC2   

Load balancer target  

**Change the Auto scaling group to have 2 servers**
- Edit your Auto scaling group  

- Change the desired capacity to 2  

- After that you should see 2 EC2 instances and load balancer target with 2 instances  


