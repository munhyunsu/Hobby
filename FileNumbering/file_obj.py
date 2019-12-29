import os
import hashlib
import shutil

BUF_SIZE = 64*1024


class File(object):
    def __init__(self, src):
        self.path = src
        self.sha256 = self._get_sha256()
    
    def _get_sha256(self):
        sha256 = hashlib.sha256()
        
        with open(self.path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha256.update(data)

        return sha256.hexdigest()

    def move(self, dst):
        if os.path.exists(dst):
            return False
        shutil.move(self.path, dst)
        return True

