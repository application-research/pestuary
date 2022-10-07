from setuptools import setup

setup(
        name="Pestuary",
        version="1.0",
        py_modules="pestuary",
        package_dir={'':'src'},
        install_requires=[
                'Click',
                "swagger_client @ git+https://github.com/snissn/estuary-swagger-clients.git#subdirectory=python",
                "requests",
            ],
        entry_points='''
            [console_scripts]
            pestuary=pestuary_cli:main
        '''
)
        
