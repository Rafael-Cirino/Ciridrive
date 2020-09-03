from setuptools import setup, find_packages

setup(
    name="ciridrive_python",
    version="1.195",
    url="https://github.com/Rafael-Cirino/Ciridrive",
    license="MIT",
    author="Rafael Cirino",
    author_email="rafael.cirino@unicamperacing.com.br",
    description="This library simplifies the integration of python algorithms with Google drive | Essa biblioteca simplifica a integração de algoritmos em python, com o Google drive",
    packages=find_packages(exclude=["test", "credentials", "download", "pass_drive"]),
    long_description=open("README.md").read(),
    zip_safe=False,
)

