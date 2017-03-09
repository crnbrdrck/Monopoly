from setuptools import setup

setup(
    name="Monopoly.Client",
    version="1.0",
    description="Super Confused's Monopoly Client",
    author="Super Confused",
    packages=['Client', 'pygame'],
    entry_points={
        'setuptools.installation': [
            'eggsecutable = Client.__main__:main',
        ]
    }
)