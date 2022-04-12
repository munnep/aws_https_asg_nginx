variable "tag_prefix" {
  description = "default prefix of names"
}

variable "region" {
  description = "region to create the environment"
}

variable "vpc_cidr" {
  description = "which private subnet do you want to use for the VPC. Subnet mask of /16"
}

variable "ami" {
  description = "Must be an Ubuntu image that is available in the region you choose"
}

variable "dns_hostname" {
  type        = string
  description = "DNS name you use to access the website"
}

variable "dns_zonename" {
  type        = string
  description = "DNS zone the record should be created in"
}

variable "certificate_email" {
  type        = string
  description = "email adress that the certificate will be associated with on Let's Encrypt"
}


variable "asg_min_size" {
  description = "Autoscaling group minimal size"
}

variable "asg_max_size" {
  description = "Autoscaling group maximal size"
}

variable "asg_desired_capacity" {
  description = "Autoscaling group running number of instances"
}

