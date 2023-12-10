#!/bin/python3

import json
import socket
from datetime import datetime

# Import the .json data
with open("/bind/domain.json","r") as f:
    data = json.load(f)
    f.close()
with open("/bind/56.168.192.in-addr.arpa.json","r") as f:
    addr_arpa_data = json.load(f)
    f.close()
with open("/bind/options.json","r") as f:
    options = json.load(f)
    f.close()

# Define default IP for glue RR
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = str(s.getsockname()[0])
    s.close()
    return ip

local_ip = get_ip_address()
def adjust_glue(data):
    ip = get_ip_address()
    data["records"][1]["rr_data"]=ip

# Templating functions
# build_soa_db
def build_soa(data):
    origin = data["domain"]
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d00") # Need to design increment function for updates
    soa ="""\
$TTL 2d
$ORIGIN """+origin+""".
@\tIN\tSOA\tns1."""+origin+""". hostmaster."""+origin+""" (
\t\t\t\t\t"""+timestamp+""" ; serial
\t\t\t\t\t12h ; refresh
\t\t\t\t\t15m ; update retry
\t\t\t\t\t3w ; expiry
\t\t\t\t\t2h ; minimum
\t\t\t\t\t)"""
    return soa

def build_rr(name,rr_type,rr_data):
    return f"{name:<10}IN\t{rr_type:20}\t{rr_data:<30}\n"

def build_rr_db(data):
    records = data["records"]
    rr_db = ""
    for i in records:
        rr_db += build_rr(i["name"], i["rr_type"], i["rr_data"])
    return rr_db

def build_zones_entry(data):
    domain = data["domain"]
    if (data["primary"]=="true"):
        ztype = "primary"
        file = "/etc/bind/primary/" + domain + ".db"
    else:
        ztype = "secondary"
        file = "/etc/bind/secondary/" + domain + ".db"
    return "zone \"" + f"{domain}" + "\"\t{ type " + f"{ztype}" + "; file \"" + f"{file}" + "\"; };\n"

# write db (RRs)
def write_db(data):
    with open("/bind/etc_bind/primary/"+data["domain"]+".db","w") as db:
        db.write(build_soa(data))
        db.write("\n; ########### RRs Below #########\n")
        db.write(build_rr_db(data))
    db.close()

# write out a zones.* file
def write_zone(data):
    with open("/bind/etc_bind/zones."+ data["domain"], "w") as zf:
        zf.write(build_zones_entry(data))
    zf.close()
    return

# Adjust named.conf.local to include the new zones.* file
def adjust_local(data):
    entry = "include \"/etc/bind/zones."+ data["domain"] + "\";"

    with open("/bind/etc_bind/named.conf.local", "r") as local:
        text=local.read()
        test = text.find(entry)
        local.close()
    
    if (test == -1):
        with open("/bind/etc_bind/named.conf.local", "a") as local:
            local.write(entry)
            local.close()
    return

# Adjust named.conf.options (ACL groups, Forwarders)
def write_options(data,options):
    with open("/bind/etc_bind/named.conf.options", "w") as optfile:
        optfile.write("acl " + data["acl_id"] + " {\n")
        for cidr in data["acl_cidrs"]:
            optfile.write("\t"+cidr+";\n")
        optfile.write("};\n")
        optfile.write("options {\n")
        optfile.write("\tdirectory \"/var/cache/bind/\";\n")
        optfile.write("\tversion \"not currently available.\";\n")
        optfile.write("\tallow-query { " + data["acl_id"] + "; };\n")
        optfile.write("\tallow-query-cache { " + data["acl_id"] + "; };\n")
        optfile.write("\tallow-recursion { " + data["acl_id"] + "; };\n")
        optfile.write("\trecursion " + options["recursion"]+ ";\n")
        optfile.write("\tforwarders {\n")
        for fwd in options["forwarders"]:
            optfile.write("\t\t"+ fwd + ";\n")
        optfile.write("\t};\n")
        optfile.write("\tdnssec-validation "+options["dnssec-validation"]+ ";\n")
        optfile.write("\tlisten-on-v6 { any; };\n")
        optfile.write("};\n")
        optfile.close()
    return

adjust_glue(data)
adjust_glue(addr_arpa_data)
write_db(data)
write_zone(data)
write_zone(addr_arpa_data)
adjust_local(data)
adjust_local(addr_arpa_data)
write_options(data,options)
