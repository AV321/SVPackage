from setuptools import setup 

setup(
        name = 'SVassembly',
        packages = ['SVassembly'],
        version = '0.431',
        description = 'SV phasing pipeline',
        author = 'Hanlee Ji lab',
        author_email = 'avitko@stanford.edu',
        url = 'https://github.com/AV321/SVassembly',
        dowload_url = 'https://github.com/AV321/SVassembly/archive/0.431.tar.gz',
        license = 'MIT',
        package_data = {'SVassembly': ['*.R']},#'*.Rscript']}, #added bc of R file
        #include_package_data=True  #added bc of R file
        #install_requires = ['pandas']  #need to fill this out
        #keywords
        #classifiers
)
