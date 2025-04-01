import os
import getpass
import rsa
import shutil
import sys
import subprocess

os.system('pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org" --trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org')
print('*'*50, ' PIP config set! ', '*'*50)
print('')

print('Installing required packages')
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
print('Package installation complete')

from distutils.dir_util import copy_tree

def create_folder_structure():
    base_path = os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI')
    keys_dir = os.path.join(base_path, 'Keys')
    try:
        os.makedirs(keys_dir)
    except:
        pass

    # shutil.copy('QV_Download_v2.py', os.path.join(base_path, 'QV_Download_v2.py'))
    # shutil.copy('chromedriver.exe', os.path.join(base_path, 'chromedriver.exe'))
    src_path = os.path.join(os.path.dirname(__file__), "login_generator.py")
    shutil.copy(src_path, os.path.join(base_path, 'login_generator.py'))
    copy_tree(os.path.join(os.getcwd(), 'Keys'), keys_dir)

    base_path = os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI')
    os.chdir(base_path)
    if not os.path.exists(os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI', 'ipynb_metadata.xml')):
        with open(os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI', 'ipynb_metadata.xml'), mode='w+') as f:
            f.write('')
    if not os.path.exists(os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI', 'API.log')):
        with open(os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI', 'API.log'), mode='w+') as f:
            f.write('')

    
def gen_login():

    keys_path = os.path.join('C:', os.sep, 'Users', getpass.getuser(), 'OneDrive - Landmark Group', 'Work', 'Automations', 'GUI', 'Keys')
    with open(os.path.join(keys_path, 'pub_key.PEM'), mode='rb') as pub_key:
        publicKey = pub_key.read()
        publicKey = rsa.PublicKey.load_pkcs1(publicKey)

    qv_usrname = str(input('Please enter QV username:'))
    qv_pswd = getpass.getpass('Enter QV password')
    qv = qv_usrname + '###' + qv_pswd
    er_usrname = str(input('Please enter ER username:'))
    er_pswd = getpass.getpass('Enter ER password')
    er = er_usrname+ '###' + er_pswd

    qv = rsa.encrypt(qv.encode('utf-8'), publicKey)
    er = rsa.encrypt(er.encode('utf-8'), publicKey)

    with open(os.path.join(keys_path, 'qv_login.txt'), mode='wb') as f:
        f.write(qv)
    with open(os.path.join(keys_path, 'er_login.txt'), mode='wb') as f:
        f.write(er)

def post_install():
    create_folder_structure()
    gen_login()

if __name__ == "__main__":
    post_install()