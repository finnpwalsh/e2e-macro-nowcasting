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
# Subnets
# ------------------------------------------

resource "aws_subnet" "public_a" {
    vpc_id                  = aws_vpc.this.id
    availability_zone       = data.aws_availability_zones.available.names[0]
    cidr_block              = "10.20.0.0/20"
    map_public_ip_on_launch = true
}

resource "aws_subnet" "public_b" {
    vpc_id                  = aws_vpc.this.id
    availability_zone       = data.aws_availability_zones.available.names[1]
    cidr_block              = "10.20.16.0/20"
    map_public_ip_on_launch = true
}

resource "aws_subnet" "private_a" {
    vpc_id = aws_vpc.this.id
    availability_zone = data.aws_availability_zones.available.names[0]
    cidr_block = "10.20.32.0/20"
}

resource "aws_subnet" "private_b" {
    vpc_id = aws_vpc.this.id
    availability_zone = data.aws_availability_zones.available.names[1]
    cidr_block = "10.20.48.0/20"
}

# ------------------------------------------
# Public Route Table
# ------------------------------------------

resource "aws_route_table" "public" {
    vpc_id = aws_vpc.this.id
}

resource "aws_route" "public_default" {
    route_table_id         = aws.route_table.public.id
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
# NAT
# ------------------------------------------

resource "aws_eip" "nat" {
    domain = "vpc"
}

resource "aws_nat_gateway" "this" {
    allocation_id = aws_eip.nat.id
    subnet_id     = aws_subnet.public_a.id
    depends_on    = [aws_internet_gateway.this]
}

# ------------------------------------------
# Private Route Table
# ------------------------------------------

resource "aws_route_table" "private" {
    vpc_id = aws_vpc.this.id
}

resource "aws_route" "private_default" {
    route_table_id         = aws.route_table.private.id
    destination_cidr_block = "0.0.0.0/0"
    nat_gateway_id        = aws_internet_gateway.this.id
}

resource "aws_route_table_association" "private_a" {
    subnet_id = aws_subnet.private_a.id
    route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_b" {
    subnet_id = aws_subnet.private_b.id
    route_table_id = aws_route_table.private.id
}