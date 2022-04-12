variable "tag_prefix" {
  description = "default prefix of names"
}

variable "region" {
  description = "region to create the environment"
}

variable "vpc_cidr" {
  description = "which private subnet do you want to use for the VPC. Subnet mask of /16"
}

