from setuptools import setup

setup(
    name='xml_sanitize',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=['xml_sanitize'],
    entry_points={
        'console_scripts': [
            'xml-sanitize = xml_sanitize:main'
        ]
    }
)
