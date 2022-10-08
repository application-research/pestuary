from setuptools import setup

setup(
        name="pestuary",
        version="1.0",
        package_dir={'':'src'},
        install_requires=[
                'Click',
                "estuary_client",
                "requests",
            ],
        entry_points='''
            [console_scripts]
            pestuary=pestuary_cli:main
        '''
)
        
