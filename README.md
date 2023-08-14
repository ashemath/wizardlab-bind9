# Wizardlab-bind9

## Overview
This project will setup a BIND 9 DNS server using `docker compose`.
While this project could be usefull in other contexts, it's primary
purpose is to serve as a repository for Wizardlab's DNS service.

## Wizardlab?
[github.com/ashelab/wizardlab](https://github.com/ashemath/wizardlab)
Wizardlab is a testing/development environment that I design for
professional development and free entertainment. It's based around a
multimachine Vagrant file and configuring things with Ansible.

I have a need for DNS automation since I prefer to test against a real DNS
service, and I may need to switch up my subnet from time-to-time. Also,
I may need to have several projects on one machine, each on their own subnet,
so I need to be able to configure a simple DNS server will minimal manual
configuration.

In this project, I plan to automate setting up dns with this project
with Ansible using Jinja2 templating to configure the dns_settings file prior
to running the `docker compose` command.

If not automating this project with with Wizardlab and Ansible, you may edit
the dns_settings file some other way, and run `docker compose up -d`.


--------------------------------------------
This project is new and in development.
My plan is to have a minimal product ready in a few days. DNS is something
that Wizardlab needs to run other network services. Configuring `/etc/hosts/`
can only get you so far!

Plan:
- Build on debian bookworm base image
- Setup BIND 9 DNS server
- Configure a barebones DNS service by editing a single setup file, or
  setting a few shell variables.
- Defaults are not preconfigured, but examples are provided in dns_settings file comments.
- Configures a sensible initial configuration for an authoritative name server for a given
  domain name, on a given single /24 sized network.
- Networks out of host ports TCP/UDP 53, or optionally onto a configured linux bridge.

