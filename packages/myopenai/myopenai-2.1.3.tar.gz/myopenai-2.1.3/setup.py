from setuptools import setup, find_packages

setup(
    name='myopenai',
    version='2.1.3',
    packages=find_packages(),
    package_data={
        'myopenai': ['pricedata.json'],
    },
    install_requires=[
        'openai',
        'anthropic',
        'google-generativeai',
        'python-dotenv',
        'requests',
        'jsonschema',
        'pydantic',
        'pyaudio',
    ],
    url='https://github.com/lupin-oomura/myopenai.git',
    author='Shin Oomura',
    author_email='shin.oomura@gmail.com',
    description='A simple OpenAI function package',
)
