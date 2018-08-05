from setuptools import setup, find_packages
from Cython.Build import cythonize

def do_setup():
    setup(name = "PEAnuts",
          version = "0.0",
          author = "Team Sigma",
          description = "Does not work just yet",
          license = "Cog*Works",
          platforms = ["Windows", "Linux", "Mac OS-X", "Unix"],
          packages = find_packages(),
          install_requires = ["numpy>=1.12"],
          ext_modules = cythonize("test.pyx"))

if __name__ == "__main__":
    do_setup()
