from setuptools import find_packages, setup


def get_install_requires():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f.readlines() if not line.startswith("-")]


setup(
    name="gdsfactory",
    url="https://github.com/PsiQ/gdsfactory",
    version="1.1.3",
    author="PsiQ",
    scripts=["pp/pf.py"],
    description="python libraries to generate GDS layouts",
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_install_requires(),
    python_requires=">=3.6",
    entry_points='''
        [console_scripts]
        pf=pp.pf:cli
    ''',
)
