import subprocess
import os

os.system("rm -rf ~/.aws")
os.system("cp --force -r ../utils/aws ~/")
os.system("mv ~/aws ~/.aws")

proc = subprocess.Popen(["aws ec2 describe-instances --query 'Reservations[*].Instances[*].PublicIpAddress' --output=text --profile ellan"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

out = str(out)

out = out.replace("\\n", ",")
out = out[:len(out)-2]
out = out.replace("b'", "")

ips = out.split(",")

print ("program output:", ips)

os.system("rm -rf ~/.ssh/ellan.pem")
os.system('cp --force ../utils/ssh/ellan.pem ~/.ssh')
os.system('chmod 400 ~/.ssh/ellan.pem')

os.system('rm -rf ~/.ansible-config')
os.system('cp --force -r ../utils/ansible-config ~/')
os.system('mv --force ~/ansible-config ~/.ansible-config')

os.system('rm -rf ~/.ansible.cfg')
os.system('cp --force -r ../utils/ansible-config/ansible.cfg ~/')
os.system('mv --force ~/ansible.cfg ~/.ansible.cfg')


fl = open('hosts', 'a')

fl.write('[gitlab]\n')
fl.write(ips[0]+'\n')
fl.write('[gitlab:vars]\n')
fl.write('ansible_ssh_user=centos\n')
fl.write('ansible_ssh_private_key_file = ~/.ssh/ellan.pem')
fl.write('\n\n')

fl.write('[rancher]\n')
fl.write(ips[1]+'\n')
fl.write('[rancher:vars]\n')
fl.write('ansible_ssh_user=centos\n')
fl.write('ansible_ssh_private_key_file = ~/.ssh/ellan.pem')


os.system('mv hosts ~/.ansible-config/hosts')
