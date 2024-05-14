# Ansible Collection - sysengquick.proxmox

This collection is used to deploy linux cloud images to a proxmox VE server.

## Playbooks

This collection includes the following playbooks:

- create_cloud_vm

  This playbook is used to create a cloud VM in your proxmox server.
  It does this by calling importing two role tasks: cloud_image.main and api.create_vm.

  You must supply the proper role variables when using this playbook.
  This could be with extra vars or an import_playbook task with a vars section.

  Example:

  ```yaml
  ---
  - name: Lookup vault file path
      hosts: localhost
      gather_facts: false

      tasks:
        - name: Register the vault file path
          ansible.builtin.set_fact:
          vault_file_path: "{{ playbook_dir }}/vars/vault/proxmox.yaml"

  - name: Run create_cloud_vm playbook
    ansible.builtin.import_playbook: sysengquick.proxmox.create_cloud_vm
    vars:
      global_cloud_image_name: fedora
      global_cloud_image_storage: nas
      global_proxmox_api:
        host: pve.example.net  # Your proxmox API host
        user: root@pam  # The user the token is associated with
        token_id: ansible  # The token ID
        token_secret: "{{ vault.proxmox_api.token_secret }}"  # The token secret
      api_create_vm_values:
        name: ubuntu-noble.example.net  # Name of the server to create
        cloud_init:
          sshkeys: |
            ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINQRZM5OpaNZztF6Sg0dUofqZKkeW9RpCwpm+r0XA3QP user@example
        cpu_cores: 4
        disk:
          - {}
          - size: 20
        memory: 4096
        network:
          - {}
          - ipconfig: ip=10.10.10.254/24
            bridge: vmbr1
        node: pve  # node on which to create the host
        onboot: true
      vault: |-
        {{
          lookup('ansible.builtin.file', hostvars['localhost']['vault_file_path'])
          | ansible.builtin.unvault('vault')
          | from_yaml
        }}
  ```

  Not all values are required.
  Consult role documentation for more informatrion.

## Roles

This collection includes the following roles:

- api

  Make API calls to the proxmox server.

  Tasks:

  - create_vm

    Uses the proxmox API to create a new VM from a qcow2 cloud image file.
    Expects the cloud_image file to exist in the specified storage.
    Uses the cloud_image lookup plugin to get the image filename.

  - storage_path

    Pulls the folder path for a given proxmox storage ID.
    Used by the cloud_image role to store the cloud image file.

  See the role docs for further information.

  ```sh
  ansible-doc sysengquick.proxmox.api
  ```

- cloud_image

  Download cloud_image file to the proxmox server.

  See the role docs for further information.

  ```sh
  ansible-doc sysengquick.proxmox.cloud_image
  ```

## Plugins

### Lookup Plugins

- cloud_image

  This plugin is used to find download information for cloud image files for various linux distributions.

  See the plugin docs for further information.

  ```sh
  ansible-doc -t lookup sysengquick.proxmox.cloud_image
  ```

### Filter Plugins

- checksum
- disk_config
- network_config
- qcow2_image_name

The filter plugins are helpers for roles.
They are not intended to be used outside these roles, and are likely not helpful anywhere else.

See the plugin docs for further information.

```sh
ansible-doc -t filter sysengquick.proxmox.checksum
ansible-doc -t filter sysengquick.proxmox.disk_config
ansible-doc -t filter sysengquick.proxmox.network_config
ansible-doc -t filter sysengquick.proxmox.qcow2_image_name
```
