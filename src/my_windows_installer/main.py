# main script because this is still a single file program
# specific to installing dust

from pathlib import Path
import requests


def main():
    """Main function to run the installer."""
    INSTALLER_ROOT_PATH = Path.home() / ".my_installer"
    SOURCE_URL = "https://github.com/bootandy/dust/releases/download/v1.2.4/dust-v1.2.4-i686-pc-windows-gnu.zip"

    # create tmp dir
    TMP_WORKSPACE_PATH = INSTALLER_ROOT_PATH / "tmp"
    TMP_WORKSPACE_PATH.mkdir(parents=True, exist_ok=True)

    # download file
    response = requests.get(SOURCE_URL)

    # validate request
    if response.ok == False or response.status_code != 200:
        raise Exception(f"Request failed {response.status_code}")

    # save response file
    ZIP_FILE_NAME = "dust.zip"
    ZIP_FILE_PATH = TMP_WORKSPACE_PATH / ZIP_FILE_NAME
    with open(ZIP_FILE_PATH, "wb") as file:
        file.write(response.content)

    # unzip
    # install files
    # remove tmp dir


if __name__ == "__main__":
    main()
