from os import walk, path, sys
from datetime import datetime
from pkg_resources import resource_string


def afterlast(arr, offsetstr):
    return arr[len(arr) - arr[::-1].index(offsetstr[::-1]) :]


def get_resource_text(resource_path):
    resource_content = resource_string(__name__, resource_path)
    return resource_content.replace(b"\r\n", b"\n").decode("utf-8", errors="ignore")


def get_sorted_files(file_list, extensions):
    # sort based on extension
    sortedExts = sorted(extensions)
    sortedFiles = []
    for e in sortedExts:
        for f in file_list:
            if f in uncachableFiles:
                continue
            if afterlast(f, ".") == e:
                sortedFiles.append(f)
    return sortedFiles


def create_pwa_files(directoryPath):
    projectName = path.basename(directoryPath)

    # insertion
    extensions = []
    file_list = []

    for root, dirs, files in walk(directoryPath):
        if ".git" in root:
            continue
        for file in files:
            if afterlast(file, ".") not in extensions:
                extensions.append(afterlast(file, "."))
            file_list.append(
                afterlast(root, directoryPath).replace("\\", "/") + "/" + file
            )

            if file.endswith(".html"):
                file_path = root + "\\" + file
                with open(file_path, "r+") as f:
                    content = f.read()

                    # does root contain absolute path with \ at the end
                    manifestLinkHTML = manifestLink.replace(
                        "$currentChildPath",
                        afterlast(root + "\\", directoryPath).replace("\\", "/")[1:],
                    )
                    if manifestLinkHTML not in content:
                        content = content.replace(
                            "</head>", f"\t{manifestLinkHTML}\n\t</head>"
                        )

                    if file == "index.html" and SWregistrationScript not in content:
                        content = content.replace(
                            "</body>", f"\t{SWregistrationScript}\n\t</body>"
                        )

                    f.seek(0)
                    f.write(content)
                    f.truncate()

    if "/sw.js" not in file_list:
        file_list.append("/sw.js")

    # Access template files
    default_sw = get_resource_text("sw.js")
    default_registration = get_resource_text("register-sw.js")
    default_app_webmanifest = get_resource_text("app.webmanifest")

    # file creation
    if not path.exists(directoryPath + "/app.webmanifest"):
        with open(directoryPath + "/app.webmanifest", "w") as f:
            f.write(default_app_webmanifest.replace("$projectName", projectName))

    if not path.exists(directoryPath + "/register-sw.js"):
        with open(directoryPath + "/register-sw.js", "w") as f:
            f.write(default_registration)

    with open(directoryPath + "/sw.js", "w") as f:
        sortedDirectoryTree = get_sorted_files(file_list, extensions)
        sortedDirectoryTree_str = ""
        curExt = ""
        for filename in sortedDirectoryTree:
            if curExt and curExt != afterlast(filename, "."):
                sortedDirectoryTree_str += "\n"
            curExt = afterlast(filename, ".")
            sortedDirectoryTree_str += '\t"' + filename + '",\n'

        f.write(
            default_sw.replace("$currentDate", currentDate).replace(
                "$sortedDirectoryTree", sortedDirectoryTree_str
            )
        )


def main():  # The entry point for your script
    if len(sys.argv) < 2:
        print("Usage: pwa-enabler <path_to_web_app>")
        sys.exit(1)

    project_path = sys.argv[1]
    if not path.isdir(project_path):
        print(f"Error: {project_path} is not a valid directory")
        sys.exit(1)

    create_pwa_files(project_path)
    print(f"PWA files created for {project_path}")


manifestLink = '<link href="$currentChildPathapp.webmanifest" rel="manifest" />'
SWregistrationScript = '<script src="register-sw.js"></script>'

uncachableFiles = ["/README.md"]

# Get the current date
currentDate = datetime.now().strftime("%Y-%m-%d %H:%M")

if __name__ == "__main__":
    main()
