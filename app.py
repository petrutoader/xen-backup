#!/usr/bin/python

import commands, time

path = '/mnt/nfs/xen-backups'
date = commands.getoutput("date '+%Y-%m-%d'")
commands.getoutput('mkdir ' + path + '/' + date)

def get_backup_vms():
    result = []

    cmd = "xe vm-list is-control-domain=false is-a-snapshot=false"
    output = commands.getoutput(cmd)

    toIterate = output.split("\n\n\n")

    for vm in toIterate:
        lines = vm.splitlines()
        uuid = lines[0].split(":")[1][1:]
        name = lines[1].split(":")[1][1:]
        result += [(uuid, name)]

    return result

def backup_vm(uuid, filename, timestamp, name):
   cmd = "xe vm-snapshot uuid=" + uuid + " new-name-label='" + timestamp + "'"
   print cmd
   snapshot_uuid = commands.getoutput(cmd)
   print "snapshot uuid " + snapshot_uuid

   cmd = "xe template-param-set is-a-template=false uuid=" + snapshot_uuid
   print cmd
   commands.getoutput(cmd)

   cmd = "xe vm-export vm=" + snapshot_uuid + " filename='" + path + "/" + date + "/" + filename + "'"
   print cmd
   commands.getoutput(cmd)

   cmd = "xe vm-uninstall uuid=" + snapshot_uuid + " force=true"
   print cmd
   commands.getoutput(cmd)
   print "Done!\n"

for (uuid, name) in get_backup_vms():
   timestamp = time.strftime("%Y%m%d-%H%M", time.gmtime())
   print timestamp, uuid, name
   filename = timestamp + " " + name + ".xva"
   backup_vm(uuid, filename, timestamp, name)
