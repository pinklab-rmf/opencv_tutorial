from setuptools import find_packages, setup
import os
import glob

package_name = 'opencv_tutorial'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob.glob(os.path.join('launch', '*.launch.py'))),
        ('share/' + package_name + '/param', glob.glob(os.path.join('param', '*.yaml')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mkh',
    maintainer_email='kyung133851@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'img_publisher = opencv_tutorial.img_publisher:main',
            'img_control = opencv_tutorial.img_control:main',
            'cartoon = opencv_tutorial.cartoon:main',
            'laplace = opencv_tutorial.laplace:main',
            'edge = opencv_tutorial.edge:main',
            'optical_flow = opencv_tutorial.optical_flow:main',
            
        ],
    },
)
