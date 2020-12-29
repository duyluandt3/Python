#!"d:\data\electronic\electronic study\python\0.new_couse\30.web_base_financial_grap\web_1\virtual\scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'bokeh==2.0.2','console_scripts','bokeh'
__requires__ = 'bokeh==2.0.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('bokeh==2.0.2', 'console_scripts', 'bokeh')()
    )
