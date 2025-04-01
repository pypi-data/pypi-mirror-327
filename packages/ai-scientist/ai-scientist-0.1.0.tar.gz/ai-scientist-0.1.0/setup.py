from setuptools import setup, find_packages

setup(
    name="ai-scientist",  # This is the package name on PyPI
    version="0.1.0",
    description="A CLI tool for running AI-powered research tasks.",
    author="Core Francisco Park",
    author_email="cfpark00@gmail.com",
    packages=find_packages(),  # This finds the ai_scientist package.
    install_requires=[
        "openai",   # For interacting with OpenAI's API
    ],
    include_package_data=True,  # Tells setuptools to include package data specified in MANIFEST.in
    package_data={
        "ai_scientist": ["prompts/assets/*.txt"],
    },
    entry_points={
        'console_scripts': [
            'ai-scientist=ai_scientist.run_research:main',
        ],
    },
)


