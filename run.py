import os
import shutil
import time
from pathlib import Path

import yaml

import pytest

if __name__ == '__main__':
    pytest.main()
    time.sleep(1)
    os.system('allure generate ./temp -o ./report --clean')
    shutil.move('logs/frame.log', 'logs/frame_' + time.strftime("%Y%m%d-%H%M%S") + '.log')



