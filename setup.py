from setuptools import setup

setup(name='clean_folder',
      version='0.1.9',
      description='sorting current folder',
      author='Max Bondarenko',
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
      )