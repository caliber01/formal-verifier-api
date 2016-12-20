from setuptools import setup, find_packages

setup(
    name="formal_verifier",
    version="1.0.0",
    author="Maksym Semikin",
    author_email="maksym.semikin@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-bcrypt',
        'flask-cors',
        'flask-jwt-extended',
        'flask-restful',
        'mongoengine',
    ]
)
