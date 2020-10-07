import hashlib
import os

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


print(md5(r"/Users/petterboussard/Documents/obl-2-redes/obligatoriocopy.pdf"))
print(os.path.getsize("/Users/petterboussard/Documents/obl-2-redes/obligatoriocopy.pdf"))