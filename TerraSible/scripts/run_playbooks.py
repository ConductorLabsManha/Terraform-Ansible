import os

playbooks =  os.listdir('../ansible')
playbooks.sort()

for playbook in playbooks:
  playml = playbook.split('.')
  catanything = playbook.split('-')
  
  
  if playml[1] == 'yml':
    if catanything[0] != '0':
      os.system('ansible-playbook -i ~/.ansible-config/hosts ../ansible/' + playbook)

