from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import subprocess
class BuildExeCommand(build_py):
    def run(self):
        # Run the PyInstaller command to build the .exe file
        subprocess.run(['pyinstaller', 'main.spec'])
        # Call the parent run() method to perform the regular build process
        build_py.run(self)
DEPENDENCIES = ['joblib', 'pandas', 'numpy']
setup(
    name='Final-Project',
    version='',
    packages=find_packages(),
    install_requires=DEPENDENCIES,
    author='gabilempert',
    description='Stock prediction UI',
    cmdclass = {'build_exe': BuildExeCommand},

)



