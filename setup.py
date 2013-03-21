from setuptools import setup
setup(
    name = "fakebook",
    version = "0.2",
    package_dir = {'': 'src'},
    packages = [
        'fakebook',
    ],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = [
        'requests>=1.1.0',
    ],

    package_data = {},

    author = "Karol Majta",
    author_email = "karol@karolmajta.com",
    description = "Tool for managing facebook test users",
    license = "JSON License",
    keywords = "facebook test users",
    url = "https://github.com/lolek09/fakebook",
)
