from setuptools import setup

setup(
        name="pestuary",
        version="1.0.6",
        package_dir={'':'src'},
        install_requires=[
                "estuary_client",
                "requests",
                "instantcli"
            ],
        entry_points='''
            [console_scripts]
            pestuary=pestuary_cli:main
        '''
)
        
