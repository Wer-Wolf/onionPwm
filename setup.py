# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='onionPwm',  # Required
    version='2.1',  # Required
    description='Python 3 library for interfacing with the onboard PWM of the Omega2',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional
    url='https://github.com/Wer-Wolf/onionPwm',  # Optional
    author='Wer-Wolf',  # Optional
    author_email='W_Armin@gmx.de',  # Optional
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='development',  # Optional
    package_dir={'': 'src'},  # Optional
    py_modules=["onionPwm"],  # Required
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.5, <4',
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=['peppercorn'],  # Optional
    # extras_require={  # Optional
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },
    # entry_points={  # Optional
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/Wer-Wolf/onionPwm/issues',
        'Source': 'https://github.com/Wer-Wolf/onionPwm',
    },
)