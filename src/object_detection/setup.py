from setuptools import setup

package_name = 'object_detection'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='copc',
    maintainer_email='copc@todo.todo',
    description='Object detection for the project',
    license='GPL3',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'node = object_detection.node:main',
        ],
    },
)
