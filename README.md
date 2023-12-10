# Wizardlab-bind9

## Overview
This project will setup a BIND 9 DNS server using `docker compose`.
While this project could be useful in other contexts, it's primary
purpose is to serve as a repository for Wizardlab's DNS service automation.

## Wizardlab?
[github.com/ashelab/wizardlab](https://github.com/ashemath/wizardlab)

Wizardlab is a testing/development environment that I design for
professional development and free entertainment. It's based around a
multimachine Vagrant file and configuring things with Ansible.

## Motivation
I needed a DNS server to deliver authoritative DNS services for
isolated training/development networks. Long term, I need something reliable
that I can build on to manage DNS on private cloud provider networks.

Wizardlab-bind9 is my idea of using Docker and Python to accomplish this
mission.

## Design
Having a BIND server on Docker allows us to drive dns over a variety of
network interfaces. By default, this project will override host network ports
`53/udp` and `53/tcp`. In a isolated network context, that's probably what you
want, but please use caution.

Wizardlab-bind9 is designed so we can craft/modify the single `domain.json`.
Specifying the domain name, forwarders, and all the records that we'd like
in that one file.

When the container starts, `build_files.py` reads `domain.json` and 
`options.json`, parses the requested properities of the domain, and stages up
the generated `zones.*`, `*.db`, and `named.conf.*` files in the
`/bind/etc_bind/` and `bind/etc_bind/{primary,secondary}` subdirectories.

Next, the staged files are copied from `/bind/etc_bind/*` to `/etc/bind/`
and the `named` service is started with the command `named -4 -g`.
The BIND service runs in the forground, so all the debug output gets caught
by Docker's default logging service.

To summarize:

- Edit `domain.json`
- Run `docker compose up -d`
- Profit.

There's a bit of magic happening between `domain.json` and the 
`build_files.py` command. The 2nd RR is overritten by a python
call that determines the assigned IP address for the container.
This means that the BIND server can add the appropriate "glue"
record reflecting the IP docker assigned the container.

What this means is that any IP you specify for rr_data for the 2nd
RR in the `domain.json` file will be overwritten. This may not be
what you like, so feel free to edit `build_file.py` if you do not
need this feature.

## Current status 
### Update 12/9/23
I added a reverse DNS zone file.

### Initial Upload
In it's current form, it sets up a single domain effectively.
`Domain name`, `primary` zone status, acl groups, and as many resource records
as you need can be set up in the one `domain.json` file.
Server settings that contribute to `/etc/bind/named.conf.options` can be set in
the `bind/options.json` file.

`build_files.py` supports reading the `options.json` and `domain.json` files.
I am working on having it reconcile additional `*.json` files, combining into
one or more configured "zones" that can run on a single container, but I 
would like to focus on configuration that needs just the single SOA and a few
RRs for now.

## Ideas for `build_files.py`:
- CLI like interface with common sense prompts that writes out the
  `domain.json` file.
- Prompts to build a new `*.db` or edit an existing one. Providing defaults when
appropriate.
- Incrementing the serial
appropriately.

