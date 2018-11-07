from setuptools import setup

exec(open('version.py').read())

setup(
    name = 'BulkVolumeCreate',
    version = __version__,
    author = 'Kshithij Iyer',
    author_email = 'kshithij.ki@gmail.com',
    url='https://github.com/vijaykumar-koppad/Crefi',
    license = 'BSD',
    description = ("A tool to generate large number of glusterfs volumes."),
    py_modules = ['BulkVolumeCreate','version'],
    install_requires = [""],
    requires = [""],
    entry_points = """
    [console_scripts]
    BulkVolumeCreate = BulkVolumeCreate:main
    """
)
