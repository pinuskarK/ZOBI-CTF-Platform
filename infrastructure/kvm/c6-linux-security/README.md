# C6 KVM/libvirt Operations

## Observed environment

The live implementation notes record VM zobi-c6-cure on the libvirt network zobi_c6_isolated. The guest address observed was 10.10.20.50/24; the host bridge was virbr-c6 with gateway 10.10.20.1/24. The guest interface appeared as vnet0. The VM disk is not stored in Git.

## Read-only inventory

Run on the authorised Ubuntu host:

    sudo virsh list --all
    sudo virsh dominfo zobi-c6-cure
    sudo virsh domiflist zobi-c6-cure
    sudo virsh net-info zobi_c6_isolated
    sudo virsh net-dumpxml zobi_c6_isolated
    sudo virsh domifaddr zobi-c6-cure

Some guests do not report addresses through the guest agent, so an empty domifaddr result is not conclusive. Verify the address from the guest console as well.

## Connectivity and console

    ping -c 4 10.10.20.50
    nc -zv -w 3 10.10.20.50 22
    sudo ss -ltnp | grep 5900

The recorded VNC listener was host loopback 127.0.0.1:5900. Keep VNC on loopback and use an SSH tunnel for remote console access. Do not publish port 5900 to the LAN.

## Recovery

Use only an approved snapshot or a documented rebuild procedure. Do not delete the VM disk, redefine the libvirt network, or reset the VM before preserving the current state and confirming the recovery owner. Record pre/post VM state, network settings, and a successful post-recovery challenge test.

The values above are observed project notes, not proof that the live host currently has the same configuration. Capture fresh evidence before the final demonstration.
