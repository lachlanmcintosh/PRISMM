from setuptools import setup, find_packages

setup(
    name='prismm',
    version='0.1',
    description='Phylogenetic Reconstruction and Inference in Stochastic Models for Mutation in Cancer',
    author='Lachlan McIntosh',
    author_email='lmcintosh@wehi.edu.au',
    packages=find_packages(),
    install_requires=[
        # list of dependencies
    ],
    entry_points={
        'console_scripts': [
            #'rs=prismm.run_simulation.run_simulation:main',
            #'rsio=prismm.run_simulation.run_simulation_IO:main',
            #'do_all2=prismm.do_all2:main',
            'rsia=prismm.do_simulation_inference_analysis:main'
        ],
    },
)
