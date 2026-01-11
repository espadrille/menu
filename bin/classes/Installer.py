# Import des modules
import importlib
import subprocess
import sys


# Definition de la classe Installer

class Installer(object):
    def __init__(self, package_list: list = []):
        for package in package_list:
            self.ensure_module_installed(package)
    
    # Méthodes publiques
    def ensure_module_installed(self, module_name: str):
      '''
        Verifie si un module d'extension est installe. Si ce n'est pas le cas, on tente de l'installer.
      '''
      try:
          importlib.import_module(module_name)
      except ImportError:
          print(f"Module manquant '{module_name}'. Tentative d'installation...")
          
          # Tentative d'installation du paquet manquant
          if not self.install_with_pip(module_name):
              self.install_with_os_installer(module_name)

          try:
              # Re-import du module apres installation
              importlib.invalidate_caches()
              importlib.import_module(module_name)
              print(f"Module installe : '{module_name}'.")
          except subprocess.CalledProcessError:
              print(f"Error: Le module '{module_name}' n'a pas pu être importé.")
              sys.exit(1)

    def install_with_pip(self, package_name: str):
        '''
        Installe un package avec pip.
        '''
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"Package installe : '{package_name}'.")
            return True
        except subprocess.CalledProcessError:
            print(f"Error: Impossible d'installer le package '{package_name}' avec pip.")
            return False

    def install_with_os_installer(self, package_name: str):
        '''
        Installe un package avec l'installeur du systeme.
        '''

        # Detection du systeme d'exploitation
        os_info = {}
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.rstrip().split("=", 1)
                        os_info[key] = value.strip('"')
        except FileNotFoundError:
            print(f"Impossible de detecter la distribution (/etc/os-release semble absent).")
            return False
        
        distro_id = os_info.get("ID", "").lower()
        distro_like = os_info.get("ID_LIKE", "").lower()
        if distro_id == "ubuntu" or "debian" in distro_like or "debian" == distro_id:
            install_cmd = ["sudo", "apt-get", "install", "-y", f"python3-{package_name}"]
        
        elif distro_id == "fedora" or "rhel" in distro_like or "centos" in distro_like:
            install_cmd = ["sudo", "dnf", "install", "-y", f"python-{package_name}"]
        
        elif distro_id == "arch" or "arch" in distro_like:
            install_cmd = ["sudo", "pacman", "-Syu", "--noconfirm", f"python-{package_name}"]
        
        elif "suse" in distro_id or "suse" in distro_like:
            install_cmd = ["sudo", "zypper", "install", "-y", f"python-{package_name}"]  

        try:
            subprocess.check_call(install_cmd)
            print(f"Package installe : '{package_name}'.")
            return True
        except subprocess.CalledProcessError:
            print(f"Error: Impossible d'installer le package '{package_name}' avec l'installeur du systeme.")
            print(f"       La commande \"{' '.join(install_cmd)}\" a echoue.")
            return False
