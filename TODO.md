# Stuff for Vince to do in service of a V2 release

- remove data-loader and loader-raw
- rename datagram-loader to data-loader
- remove cassandra
- remove beehive-core
    - all python 3 based images should be pegged to a python minor version anyway
    - datagram-loader, message-router
- update beehive-cert to newer ubuntu lts
- update sshd to newer ubuntu lts
- remove mysql
    - need to update new node stuff in scripts and beehive-cert
- clean up bin scripts
- submodule a new afb into project
- submodule a new api into project
