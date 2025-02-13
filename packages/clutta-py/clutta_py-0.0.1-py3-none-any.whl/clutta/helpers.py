import json
import platform
import shutil
import subprocess
import urllib3
from .constants import API_BASE_URL
from .exceptions import UnsupportedPlatformError

def check_os_type():
    os_type=platform.system().lower()
    supported_types=["linux","windows","darwin"]

    if os_type not in supported_types:
        raise UnsupportedPlatformError(f"OS type not supported: {os_type}")
        

def get_latest_cli_version():
    url = API_BASE_URL
    try:
        http = urllib3.PoolManager()
        resp = http.request("GET", url)
        if resp.status==200:
            data = resp.json()
            return data.get("tag_name")
        else:
            raise Exception(f"Failed to fetch release info. Status code: {resp.status}")

        # # Sending the GET request
        # with urllib3.urlopen(url) as response:
        #     # Checking if the response is successful (status code 200)
        #     if response.status == 200:
        #         # Parsing the JSON response
        #         data = json.load(response)
        #         return data.get("tag_name")
        #     else:
        #         raise Exception(f"Failed to fetch release info. Status code: {response.status}")
    except Exception as e:
        raise Exception(f"An error occurred while fetching release info: {e}")

def get_installed_cli_version():
    try:
        result = subprocess.run(
            ["clutta", "--version"],
            capture_output=True, text=True
        )
        print(result)
        output = result.stdout.strip()
        return output
    except FileNotFoundError:
        return None

def ensure_cli():

    # 1. Check if OS is supported
    check_os_type()

    # 2. Check if clutta CLI is installed
    if not shutil.which("clutta"):
        print("Clutta is NOT installed. Please go to https://github.com/sefastech/clutta-cli-releases and install Clutta before using this SDK.")
        return False
    
    # 3. Check if installed version is the latest version
    installed_version= get_installed_cli_version()
    latest_version= get_latest_cli_version()
    if installed_version!=latest_version:
        print("Clutta is outdated! Installed: %s, Latest: %s\n", installed_version, latest_version)
        return False
    
    print(f"Clutta CLI {get_installed_cli_version()} is good to go!")
    return True       

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(f"{result.stdout}")
        if result.stderr:
            print(f"stderr: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        
