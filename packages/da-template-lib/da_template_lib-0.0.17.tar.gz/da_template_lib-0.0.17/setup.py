from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='da-template-lib',
    version='0.0.17',
    license='MIT License',
    author='Kaue Matheus Santana',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='kaue.santana@equifax.com',
    keywords='Template Inovação em Dados',
    description='Template squad Inovação em Dados',
    packages=find_packages(),  # Isso inclui automaticamente todos os pacotes
    # packages=['da_lib'],
    install_requires=[
        'google-cloud-storage',
        'google-cloud-bigquery',
        'unicode',
        'pandas'
        ]
    )