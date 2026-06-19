set allow-duplicate-variables := true

import '.devbox/virtenv/pokerops.ansible-utils.molecule/justfile'

MOLECULE_SCENARIO := 'install'
MOLECULE_KVM_IMAGE := 'https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img'
