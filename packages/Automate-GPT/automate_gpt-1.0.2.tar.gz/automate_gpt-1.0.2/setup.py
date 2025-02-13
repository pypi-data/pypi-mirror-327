from setuptools import find_packages, setup

setup(
    name='Automate_GPT',
    packages=find_packages(),
    version='1.0.2',
    description='Use Chat GPT Automation',
    author='Jenil sheth',
    author_email="shethjeniljigneshbhai@gmail.com",
    install_requires=["undetected_chromedriver","selenium","pyperclip"],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
)