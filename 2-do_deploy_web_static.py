#!/usr/bin/python3
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["104.196.168.90", "35.196.46.172"]


def do_deploy(archive_path):
    """
    distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        tar_filename = archive_path.split("/")[-1]
        filename = tar_filename.split(".")[0]
        run('sudo mkdir -p /data/web_static/releases/{}'.format(filename))
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format
            (tar_filename, filename))
        run('sudo rm -rf /tmp/{}'.format(tar_filename))
        run('sudo mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(filename, filename))
        run('sudo rm -rf /data/web_static/releases/{}/web_static'
            .format(filename))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/{} /data/web_static/current'
            .format(filename))
        return True
    except Exception as error:
        return False
