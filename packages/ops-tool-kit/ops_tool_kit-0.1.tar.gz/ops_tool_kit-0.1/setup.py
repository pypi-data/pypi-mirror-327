from setuptools import setup, find_packages

setup(
    name='ops_tool_kit',  # 包名
    version='0.1',  # 版本号
    packages=find_packages(),  # 自动查找包
    install_requires=[  # 依赖项，例如：'requests>=2.25.0'
        # 'some-dependency>=x.y.z'
    ],
    author='Coder_lz',
    author_email='229165631@qq.com',
    description='Personal tool kit',
    long_description=open('README.md').read(),  # 长描述，可以从README读取
    long_description_content_type='text/markdown',
    url='https://github.com/zlz2013',  # 项目URL
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)