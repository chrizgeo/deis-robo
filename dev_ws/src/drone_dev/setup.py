from setuptools import setup

package_name = 'drone_dev'

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
    maintainer='cg',
    maintainer_email='christogeorge@live.in',
    description='Package for dev on the drone',
    license='License not declared',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'drone = drone_dev.drone:main',
            'teleop_drone = drone_dev.teleop_drone:main'
        ],
    },
)
