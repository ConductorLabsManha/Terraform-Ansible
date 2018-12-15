import subprocess
import os

proc = subprocess.Popen(["aws ec2 describe-instances --query 'Reservations[*].Instances[*].PublicIpAddress' --output=text --profile ellan"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

out = str(out)

out = out.replace("\\n", ",")
out = out[:len(out)-2]
out = out.replace("b'", "")

ips = out.split(",")

print ("program output:", ips)

try:
   os.system('mv ellan.pem ~/.ssh')
   os.system('chmod 400 ~/.ssh/ellan.pem')
except:
   pass

try:
   os.system('rm -rf ~/.ansible-config/hosts')
except:
   pass

fl = open('hosts', 'a')

try:
   os.system('mv hosts ~/.ansible-config/hosts')
except:
   pass

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
