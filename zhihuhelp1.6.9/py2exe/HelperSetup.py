from distutils.core import setup
import py2exe
options = {"py2exe":
    {"compressed": 1, 
     "optimize": 1,
     "bundle_files": 1,
    }
    }
setup(
    console=[{"script":"ZhihuHelp.py",
              "icon_resources":[(1, "helper.ico")]}],
    options=options,
    zipfile=None,  
    )

