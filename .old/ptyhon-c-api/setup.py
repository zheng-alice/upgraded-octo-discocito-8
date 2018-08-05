from setuptools import setup, find_packages, Extension

module1 = Extension("chips",
                    language='c++',
                    sources = ["chipmodule.cpp"])

def do_setup():
    setup(name = "PEAnuts",
          version = "0.0",
          author = "Team Sigma",
          description = "Does not work just yet",
          license = "Cog*Works",
          platforms = ["Windows", "Linux", "Mac OS-X", "Unix"],
          packages = find_packages(),
          install_requires = ["numpy>=1.12"],
          ext_modules = [module1])

if __name__ == "__main__":
    do_setup()
