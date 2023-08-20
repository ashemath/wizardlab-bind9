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

## wizardlab-bind9: Motivation
I have a need for DNS automation since I would like to demo settings for production,
and I like to design configuration that can transition easily and scale in
production.

## wizardlab-bind9: Design
Having a BIND server on Docker allows us to drive dns over a variety of network interfaces.
By default, this project will override host network ports `53/udp` and `53/tcp`.
In a isolated network context, that's probably what you want, but please use
caution. 

Wizardlab-bind9 is designed so that one can craft a single `domain.json`.
When the container sstarts, `build_files.py` reads `domain.json`, parses the
requested properities of the domain, and stages up the generated `zones.*`
,`*.db`, and `named.conf.*` files in the `/bind/etc_bind/` and 
`bind/etc_bind/{primary,secondary}` subdirectories.

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
In it's current form, it sets up a single domain effectively.
`Domain name`, `primary` zone status,`fowarders`, acl groups, and as many resource records
as you need can be set up in the one file.


`build_files.py` supports reading a single `domain.json` file. I am working on
having it reconcile multiple `*.json` files, combining into one or more configured
"zones" that can run on a single container, but I would like to focus on 
configuration that needs just the single SOA and a few RRs for now.

## Ideas for `build_files.py`:
- CLI like interface with common sense prompts that writes out the
  `domain.json` file.
- Prompts to build a new `*.db` or edit an existing one. Providing defaults when
appropriate.
- Incrementing the serial
appropriately.

