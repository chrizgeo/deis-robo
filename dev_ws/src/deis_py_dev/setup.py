from setuptools import setup

package_name = 'deis_py_dev'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='CG',
    maintainer_email='christogeorge@live.in',
    description='DEV - ROS2 nodes for DEIS Robo',
    license='Copyright NO one is fucking allowed to touch it',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            #these nodes are from the package deis_py_dev
            #you run these nodes
            'main_node = deis_py_dev.main:main',
            'sparkie_node = deis_py_dev.sparkie:main',
            'teleop_node = deis_py_dev.teleop:main',
            'gps_node = deis_py_dev.gps:main',
        ],
    },
)
