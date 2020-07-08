import zipfile
import os
from os.path import expanduser, join, basename, exists
from shutil import copyfile

home = expanduser("~")

forge_cache = join(home, ".gradle/caches/forge_gradle/maven_downloader/de/oceanlabs/mcp/mcp_snapshot/unofficialtest-1.16.1")
mcpzip = join(forge_cache, "mcp_snapshot-unofficialtest-1.16.1.zip")
mappingsfolder = "merged"

# mcp_snapshot-20200706-unofficialtest-1.16.1.zip
def deleteFile(loc):
    if exists(loc):
        os.remove(loc)

deleteFile(mcpzip)

if not exists(forge_cache):
    os.mkdir(forge_cache)

if not exists(join(forge_cache, "mcp_snapshot-unofficialtest-1.16.1.pom")):
    copyfile('for gradle cache/mcp_snapshot-unofficialtest-1.16.1.pom',
             join(forge_cache, "mcp_snapshot-unofficialtest-1.16.1.pom"))

dir_path = os.path.dirname(os.path.realpath(__file__))

filenames = ['fields.csv', 'methods.csv', "params.csv"]

zf = zipfile.ZipFile(join(dir_path, mcpzip), "w")
print(f"Zip Location {mcpzip}")
for folderName, subfolders, files in os.walk(join(dir_path, mappingsfolder)):
    for filename in filenames:
        # create complete filepath of file in directory
        filePath = join(folderName, filename)
        # Add file to zip
        zf.write(filePath, basename(filePath))
        print(f"Written {filename}")
zf.close()

