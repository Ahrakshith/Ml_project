from setuptools import find_packages,setup
from typing import List


HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this line return a list of requirement for the packages to the installed
    :param file_path:
    :return:
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()  # FIX: read all lines
        requirements=[requirement.replace("\n","") for requirement in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements



setup(
    name="MlProject",
    version="0.0.1",
    author="Rakshith",
    author_email="ahrakshith122@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
