#!/usr/bin/env python3

import subprocess
import os
import shutil
import shlex


def main():
    # checking disk space to make sure there is enough space
    du = shutil.disk_usage('/')
    free = du.free / du.total * 100
    if free > 5:

        #list of commands needed
        gnupg_installer = ["sudo", "apt", "install", "gnupg", "ca-certificates", "-y"]
        keys = ["sudo", "apt-key", "adv", "--keyserver", "hkp://keyserver.ubuntu.com:80", "--recv-keys", "3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF"]
        update = ["sudo", "apt-get", "update", "-y"]
        mono_devel_installer = ["sudo", "apt", "install", "mono-devel"]
        radarr_installer = ["sudo", "apt", "install", "curl", "mediainfo", "-y"]

        subprocess.run(gnupg_installer, capture_output=True)
        subprocess.run(keys)
        # Adding Mono's Ubuntu 20.04 Repository
        mono_repo = ["echo", "deb", "https://download.mono-project.com/repo/ubuntu", "stable-focal", "main", "|", "sudo", "tee", "/etc/apt/sources.list.d/mono-official-stable.list"]
        # adding key
        result = subprocess.run(mono_repo, capture_output=True)

        if (result.returncode == 0):
            subprocess.run(update, capture_output=True)
            subprocess.run(mono_devel_installer, capture_output=True) 
            #Installing Radar
            subprocess.run(radarr_installer, capture_output=True)
            curl_command = '''curl -L -O $( curl -s https://api.github.com/repos/Radarr/Radarr/releases | grep linux.tar.gz | grep browser_download_url | head -1 | cut -d \ -f 4 ) '''
            args = shlex.split(curl_command)
            subprocess.run(args, capture_output=True)
            # Extract zip file
            extract_command = ["tar", "-xvzf", "Radarr.*.linux.tar.gz"]
            subprocess.run(extract_command, capture_output=True)




if __name__ == '__main__':
    main()

