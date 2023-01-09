from bs4 import BeautifulSoup

import os
import sys
import shutil
import json

LIBRARY_JSON_FILE = 'libraries.json'
GITHUB_URL = 'https://github.com'

def _get_app_name():
    app_name = sys.argv[1]
    allowed_app_names = []
    for item in os.listdir("."):
        if os.path.isdir(item) and not item.startswith("."):
            allowed_app_names.append(item)

    if app_name not in allowed_app_names:
        _init_package_page(app_name)

    return app_name

def _init_package_page(app_name):
    os.mkdir(app_name)
    shutil.copyfile("package-page-template.html", f"{app_name}/index.html")
    with open(f"{app_name}/index.html", "r+") as html:
        package_page = BeautifulSoup(html, 'html.parser')
        package_page.find("title").string = app_name

    with open(f"{app_name}/index.html", "w") as html:
        html.write(str(package_page.prettify()))

def _get_version_number():
    version_number = sys.argv[2]
    return version_number


def _get_protocol():
    protocol = sys.argv[3]

    allowed_protocols = ["https", "ssh"]
    if protocol not in allowed_protocols:
        print(f"This protocol is not supported. Please choose one in '{allowed_protocols}'.")
        exit(1)

    return protocol

def _get_organization():
    org_name = sys.argv[4]
    return org_name

def _get_repository():
    repo_name = sys.argv[5]
    return repo_name

def _set_lib_main_page(org, repo, app):
    with open(LIBRARY_JSON_FILE, 'r') as json_file:
        json_data = json.load(json_file)
        if not any(data_entry['lib_name'] == app for data_entry in json_data):
            new_lib = {
                "repo_name": repo,
                "repo_url": f'{GITHUB_URL}/{org}/{repo}',
                "lib_name": app
            }
            json_data.append(new_lib)
            with open(LIBRARY_JSON_FILE, 'w+') as new_json_file:
                json.dump(json_data, new_json_file)

if __name__ == "__main__":
    app = _get_app_name()
    version = _get_version_number()
    protocol = _get_protocol()
    git_org = _get_organization()
    git_repo = _get_repository()
    _set_lib_main_page(git_org, git_repo, app)

    with open("commit_message.txt", "w") as f:
        commit_message = f"Publish {app} - {version} in GitHub {git_org}/{git_repo}"
        f.write(commit_message)

    with open(f"{app}/index.html", "r+") as html:
        soup = BeautifulSoup(html, 'html.parser')
        new_a = soup.new_tag("a")
        if protocol == 'https':
            new_a["href"] = f"git+https://github.com/{git_org}/{git_repo}.git@{version}#egg={app}-{version}"
        else: # ssh
            new_a["href"] = f"git+ssh://git@github.com/{git_org}/{git_repo}.git@{version}#egg={app}-{version}"
        new_a.string = f"{app}-{version}"
        soup.html.body.insert(0, new_a)

    with open(f"{app}/index.html", "w") as html:
        html.write(str(soup.prettify()))

    sys.stdout.write(commit_message)
