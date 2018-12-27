# class registration
# -*- coding: utf-8 -*-
import sys
import subprocess

class Mvalidate :
    # initial method
    def __init__(self, path = "") :
        self.path = path

    # requset batch process
    def request(self, path) :
        if os.path.exists(path) :
            text = subprocess.getoutput(["env LANG='ja_JP.UTF8' /release/tools/validator/batch/bin/new_validator.sh " + path])
        else :
            text = "File not found"
        return(text)
