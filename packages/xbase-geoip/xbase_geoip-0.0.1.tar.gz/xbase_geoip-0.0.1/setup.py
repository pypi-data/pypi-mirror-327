from distutils.core import setup

from setuptools import find_packages

setup(name="xbase_geoip",
      version="0.0.1",
      description="ip位置查询工具",
      long_description="ip位置查询工具",
      author="xyt",
      author_email="2506564278@qq.com",
      license="<MIT License>",
      packages=find_packages(),
      url="https://gitee.com/jimonik/xbase_util.git",
      install_requires=[

      ],
      zip_safe=False,
      package_data={
            'xbase_geoip': ['../xbase_geoip_assets/*']
      },
      include_package_data=True)
