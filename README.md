# Ansible Collection - pokerops.gluster

[![Build Status](https://github.com/pokerops/ansible-colllection-gluster/actions/workflows/molecule.yml/badge.svg)](https://github.com/pokerops/ansible-colllection-gluster/actions/wofklows/molecule.yml)
[![Ansible Galaxy](http://img.shields.io/badge/ansible--galaxy-pokerops.gluster.vim-blue.svg)](https://galaxy.ansible.com/ui/repo/published/pokerops/gluster/)

An [ansible collection](https://galaxy.ansible.com/ui/repo/published/pokerops/gluster) to install and configure [glusterfs](https://docs.gluster.org/en/main/)

## ToDo

- Collection supports geo-replication from one site to multiple sites (only one master and multiple slaves).
- Add support for RockyLinux / AlmaLinux

## Collection hostgroups

| Hostgroup                     |               Default | Description                  |
| :---------------------------- | --------------------: | :--------------------------- |
| gluster_server_hostgroup_name |      'gluster_server' | Gluster server hosts         |
| gluster_client_hostgroup_name |      'gluster_client' | Gluster client hosts         |
| gluster_update_skip_hostgroup | 'gluster_update_skip' | Gluster update exclude hosts |

## Collection variables

The following is the list of parameters intended for end-user manipulation:

Cluster wide parameters

| Parameter                     |    Default | Description                                                          | Required |
| :---------------------------- | ---------: | :------------------------------------------------------------------- | :------- |
| gluster_release               |         11 | Target Gluster release                                               | false    |
| gluster_volumes               |         [] | Gluster volumes to manage                                            | true     |
| gluster_owner_user            |       root | Owner user for gluster server volume paths                           | false    |
| gluster_owner_group           |       root | Owner group for gluster server volume paths                          | false    |
| gluster_directory_mode        |       0740 | ACL value for gluster volume paths                                   | false    |
| gluster_retries               |          5 | Number of retries for ansible tasks                                  | false    |
| gluster_delay                 |          5 | Time in seconds for retries in ansible tasks                         | false    |
| gluster_georeplica_user       | georeplica | Gluster geo replication user to establish a session                  | false    |
| gluster_georeplica_group      | georeplica | Gluster geo replication group to establish a session                 | false    |
| gluster_georeplica_manage     |      false | Gluster geo replication variable to assign clusters as slaves        | false    |
| gluster_server_slave_groupset |      slave | Variable to group slave hosts by a groupset. Useful for multi slaves | false    |
| gluster_nolog                 |       true | Allow to output logs for ansible tasks                               | false    |
| gluster_client_user           |       root | Owner group for gluster client mount paths                           | false    |
| gluster_client_group          |       root | Owner group for gluster client mount paths                           | false    |
| gluster_client_mode           |       0644 | ACL value for gluster client mount paths                             | false    |
| gluster_client_serial         |          1 | Number of gluster client nodes to execute in tasks                   | false    |
| gluster_reboot_timeout        |        300 | Time in seconds for gluster update reboot tasks                      | false    |

## Collection playbooks

- pokerops.gluster.install: Install gluster server and client. Also manage geo replication sessions

## Testing

Please make sure your environment has [docker](https://www.docker.com) installed in order to run role validation tests. Additional python dependencies are listed in the [requirements file](https://github.com/nephelaiio/ansible-role-requirements/blob/master/requirements.txt)

Role is tested against the following distributions (docker images):

- Ubuntu Focal
- Ubuntu Jammy
- Debian Bullseye

You can test the role directly from sources using command `molecule test`

## License

This project is licensed under the terms of the [MIT License](/LICENSE)
