from setuptools import setup

exec(open('version.py').read())

setup(
    name = 'BulkVolumeCreate',
    version = __version__,
    author = 'Kshithij Iyer',
    author_email = 'kshithij.ki@gmail.com',
    url='https://github.com/kshithijiyer/gluster-BulkVolumeCreate/',
    license = 'BSD',
    description = ("A tool to generate a large number of glusterfs volumes."),
    py_modules = ['BulkVolumeCreate','version'],
    entry_points = """
    [console_scripts]
    BulkVolumeCreate = BulkVolumeCreate:main
    """
)
