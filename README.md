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
`build_files.py` reads `domain.json`, parses the requested properities of the domain,
and stages up the generated `zones.*` and `*.db` files in the `bind/` and 
`bind/{primary,secondary}` subdirectories.

Running `docker compose up -d` brings up a BIND DNS service fitting the parameters
specified in `domain.json`.

- Edit `domain.json`
- Run `build_files.py`
- Run `docker compose up -d`
- Profit.

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


With this project, I automate setting up dns with Ansible using Jinja2
templating. I craft `domain.json` based on role-specific variables and host_facts. 
I instruct the host to execute `build_files.py`, the `docker compose up -d` command.

If not automating this project with with Wizardlab and Ansible, you may edit
the files under `bind/` some other way, and run `docker compose up -d`.

