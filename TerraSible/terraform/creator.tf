provider "aws" {
access_key = "AKIAINMFPT42RDFG357Q"
secret_key = "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"
region     = "us-west-2"
}

resource "aws_instance" "web"{
ami           = "ami-00f7c900d2e7133e1"
instance_type = "t2.micro"
key_name      = "ellan"
associate_public_ip_address = "true"
subnet_id = "${aws_subnet.public-subnet.id}"
vpc_security_group_ids = ["${aws_security_group.sgweb.id}"]
source_dest_check = false
 tags {
  Name = "VMGitlab"
}

connection {
   type = "ssh"
   user = "centos"
   private_key = "${file("~/TerraSible/terraform/ellan.pem")}"
   timeout = "2m"
}
 
provisioner "remote-exec"  {
     inline = [
         "sudo yum install -y update",
         "sudo mkdir /home/ellan",
         "sudo sudo curl -sfSL https://get.docker.com/ | sh",
         "sudo sudo service docker restart"
   ]
}
provisioner "local-exec" {
     command = "python3 ~/TerraSible/scripts/run_init.py"
}
 
provisioner "local-exec" {
     command = "ansible -i ~/.ansible-config/hosts all -m ping"
}


provisioner "local-exec" {
     command ="python3 ~/TerraSible/scripts/run_playbooks.py"
}

}

resource "aws_instance" "other"{
ami           = "ami-00f7c900d2e7133e1"
instance_type = "t2.micro"
key_name      = "ellan"
associate_public_ip_address = "true"
subnet_id = "${aws_subnet.public-subnet.id}"
vpc_security_group_ids = ["${aws_security_group.sgweb.id}"]
source_dest_check = false
 tags {
  Name = "VMRancher"
}

connection {
   type = "ssh"
   user = "centos"
   private_key = "${file("~/TerraSible/terraform/ellan.pem")}"
   timeout = "2m"
}

provisioner "remote-exec"  {
     inline = [
         "sudo yum install -y update",
         "sudo mkdir /home/ellan",
         "sudo sudo curl -sfSL https://get.docker.com/ | sh",
         "sudo sudo service docker restart",
         "sudo docker pull rancher/rancher:v2.1.0",
         "sudo docker run -d --name=rancher --restart=unless-stopped -p 80:80 -p 443:443 rancher/rancher:v2.1.0"

   ]
}
}



