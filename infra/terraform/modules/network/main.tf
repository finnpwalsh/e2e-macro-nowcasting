data "aws_availability_zones" "available" {}

resource "aws_vpc" "this" {
    cidr_block           = var.vpc_cidr
    enable_dns_support   = true
    enable_dns_hostnames = true
}

resource "aws_internet_gateway" "this" {
    vpc_id = aws_vpc.this.id
}

# ------------------------------------------
# Public Subnets
# ------------------------------------------

resource "aws_subnet" "public_a" {
    vpc_id                  = aws_vpc.this.id
    availability_zone       = data.aws_availability_zones.available.names[0]
    cidr_block              = cidrsubnet(var.vpc_cidr, 4, 0)
    map_public_ip_on_launch = true
}

resource "aws_subnet" "public_b" {
    vpc_id                  = aws_vpc.this.id
    availability_zone       = data.aws_availability_zones.available.names[1]
    cidr_block              = cidrsubnet(var.vpc_cidr, 4, 1)
    map_public_ip_on_launch = true
}

# ------------------------------------------
# Route Table
# ------------------------------------------

resource "aws_route_table" "public" {
    vpc_id = aws_vpc.this.id
}

resource "aws_route" "public_default" {
    route_table_id         = aws_route_table.public.id
    destination_cidr_block = "0.0.0.0/0"
    gateway_id             = aws_internet_gateway.this.id
}

resource "aws_route_table_association" "public_a" {
    subnet_id      = aws_subnet.public_a.id
    route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_b" {
    subnet_id      = aws_subnet.public_b.id
    route_table_id = aws_route_table.public.id
}

# ------------------------------------------
# SVC Security Group
# ------------------------------------------

resource "aws_security_group" "svc" {
    name   = "${var.project}-${var.env}-svc-sg"
    vpc_id = aws_vpc.this.id
    
    ingress {
        from_port   = var.svc_port
        to_port     = var.svc_port
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}