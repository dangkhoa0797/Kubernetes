#!/bin/bash
#nfs server
sudo apt install nfs-kernel-server
mkdir -p /nfs_volumes
chmod -R 777 /nfs_volumes
echo "/nfs_volumes *(rw,sync,no_subtree_check,no_root_squash,insecure)">>/etc/exports
sudo exportfs -rv
showmount -e
systemctl restart nfs-kernel-server rpcbind
#nfs client (worker)
sudo apt install nfs-common
mount -t nfs 10.0.68.96:/nfs_volumes /mnt