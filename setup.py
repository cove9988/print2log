from distutils.core import setup
setup(
  name = 'print2log',
  packages = ['print2log'], # this must be the same as the name above
  version = '0.1',
  description = 'using decorator, minimal change required from replace any print statement. ',
  author = 'Paul Guo',
  author_email = 'cove9988@gmail.com',
  url = 'https://github.com/cove9988/print2log', # use the URL to the github repo
  download_url = 'https://github.com/cove9988/print2log/archive/print2log.0.1.tar.gz', 
  keywords = ['print', 'logging', 'recursive print'], # arbitrary keywords
  classifiers = [],
  python_requires='>=3',
)
