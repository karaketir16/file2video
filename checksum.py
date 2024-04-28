import hashlib

def checksum(large_file):
    """Calculate MD5 checksum for file."""
    md5_object = hashlib.md5()
    block_size = 128 * md5_object.block_size
    with open(large_file, 'rb') as a_file:
        chunk = a_file.read(block_size)
        while chunk:
            md5_object.update(chunk)
            chunk = a_file.read(block_size)
    return md5_object.hexdigest()