#!/usr/bin/python3
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["104.196.168.90", "35.196.46.172"]


def do_deploy(archive_path):
    """ distributes the archive to the server """
    if not os.path.exists(archive_path):
        return False

    try:
         put(archive_path, "/tmp/")
         out = archive_path[9:-4]
         new_path = archive_path[9:]
         releases = "/data/web_static/releases"
         run(f"mkdir -p {releases}/{out}")
         run(f"tar -xzf /tmp/{new_path} -C {releases}/{out}/")
         run(f"rm /tmp/{new_path}")
         run(f"mv {releases}/{out}/web_static/* {releases}/{out}/")
         run(f"rm -fr {releases}/{out}/web_static")
         run(f"rm -fr /data/web_static/current")
         run(f"ln -s {releases}/{out}/ /data/web_static/current")
    except Exception:
         return False
    print("New version deployed!")
    return True
