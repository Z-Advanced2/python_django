# class reqistration
# -*- cording: utf-8 -*-
import os
import re

class Curobject :
    # request html file path
    def request(selef, path = "/nouhin/home-wwwdevelopers/testweb"):
        files = []
        for file in Curobject.find_all_files(path):
            if re.findall('.*/index.html', str(file)):
                files.append(file.replace(path, ""))
#                files.append(file)
        return(files)

    # search files and directories path
    def find_all_files(directory):
        for root, dirs, files in os.walk(directory):
            yield root
            for file in files:
                yield os.path.join(root, file)
