# main script because this is still a single file program
# specific to installing dust

from pathlib import Path
import requests
import shutil


def main():
    """Main function to run the installer."""
    
    # unviversal variables
    INSTALLER_ROOT_PATH = Path.home() / ".my_installer"
    THIS_DIR = Path(__file__).parent
    APPS_DIR = Path.home() / "home/.local/apps"
    BIN_DIR = Path.home() / "home/.local/bin"

    # app specific variables
    SOURCE_URL = "https://github.com/helix-editor/helix/releases/download/25.07.1/helix-25.07.1-x86_64-windows.zip"
    APP_NAME = "helix"

    # create tmp dir
    TMP_WORKSPACE_PATH = INSTALLER_ROOT_PATH / "tmp"
    shutil.rmtree(TMP_WORKSPACE_PATH, ignore_errors=True)
    TMP_WORKSPACE_PATH.mkdir(parents=True)

    # download file
    response = requests.get(SOURCE_URL)

    # validate request
    if not response.ok or response.status_code != 200:
        raise Exception(f"Request failed {response.status_code}")

    # save response file
    ZIP_FILE_NAME = APP_NAME + ".zip"
    ZIP_FILE_PATH = TMP_WORKSPACE_PATH / ZIP_FILE_NAME
    with open(ZIP_FILE_PATH, "wb") as file:
        file.write(response.content)

    # unzip
    EXTRACTED_FOLDER_NAME = APP_NAME
    EXTRACTED_FOLDER_PATH = TMP_WORKSPACE_PATH / EXTRACTED_FOLDER_NAME
    shutil.unpack_archive(ZIP_FILE_PATH, EXTRACTED_FOLDER_PATH)

    # delete if it already exists in install location
    INSTALLED_PATH = APPS_DIR / APP_NAME
    shutil.rmtree(INSTALLED_PATH, ignore_errors=True)

    # move to app location
    shutil.move(EXTRACTED_FOLDER_PATH, APPS_DIR)

    # find executable
    APP_INSTALL_PATH = APPS_DIR / APP_NAME
    children = APP_INSTALL_PATH.rglob("*")
    for child in children:
        if child.suffix == ".exe":
            EXECUTABLE_PATH = child
            break
    else:
        raise Exception("Executable not found")

    # create shim
    SHIM_EXE_ORIGINAL_PATH = THIS_DIR / "shim.exe"
    SHIM_EXE_TARGET_PATH = BIN_DIR / (APP_NAME + ".exe")
    SHIM_EXE_TARGET_PATH.unlink(missing_ok=True)  # remove if it already exists
    shutil.copy(SHIM_EXE_ORIGINAL_PATH, SHIM_EXE_TARGET_PATH)

    # write shim text
    SHIM_TEXT_PATH = BIN_DIR / (APP_NAME + ".shim")
    SHIM_TEXT_PATH.unlink(missing_ok=True)  # remove if it already exists
    with open(SHIM_TEXT_PATH, "w") as file:
        file.write(f"path = {EXECUTABLE_PATH}")
    # remove tmp dir
    shutil.rmtree(TMP_WORKSPACE_PATH)


if __name__ == "__main__":
    main()
