from setuptools import setup, find_packages

setup(
  name="arnelify-server",
  version="0.6.5",
  author="Arnelify",
  description="Minimalistic dynamic library which is a powerful http-server written in C and C++.",
  url='https://github.com/arnelify/arnelify-server-python',
  keywords="arnelify arnelify-server-python arnelify-server",
  packages=find_packages(),
  package_data={
    'arnelify_server': [
      'arnelify_server/bin/arnelify_server_amd64.so',
      'arnelify_server/bin/arnelify_server_arm64.so',
    ],
  },
  install_requires=[],
  long_description=open("README.md", "r", encoding="utf-8").read(),
  long_description_content_type="text/markdown",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
  ]
)