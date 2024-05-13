import random
import string
import subprocess
import pytest
from checkers import checkout_positive
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout_positive(
        "mkdir {} {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"], data["folder_badarx"],
                                      data["folder_home"]),
        "")


@pytest.fixture()
def clear_folders():
    return checkout_positive(
        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                            data["folder_badarx"]), "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(5):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout_positive(
                "cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], filename),
                ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout_positive("cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not checkout_positive(
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername,
                                                                                      testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_badarx():
    checkout_positive("cd {}; 7z a {}/badarx.7z".format(data["folder_in"], data["folder_badarx"]), "Everything is Ok")
    checkout_positive("truncate -s l {}/badarx.7z".format(data["folder_badarx"]), "Everything is Ok")
    yield "badarx"
    checkout_positive("rm -f {}/badarx.7z".format(data["folder_badarx"]), "")


'''
Задание 1.
Условие:
Дополнить проект фикстурой, которая после каждого шага теста дописывает в заранее созданный файл stat.txt строку вида:
время, кол-во файлов из конфига, размер файла из конфига, статистика загрузки процессора
из файла /proc/loadavg (можно писать просто всё содержимое этого файла).
'''


@pytest.fixture()
def home_task1():
    yield "home_task1"
    checkout_positive("cat /proc/loadavg >> {}/{}".format(data["folder_home"], "stat.txt"), "")
    checkout_positive("echo {}>> {}/{}".format(datetime.now().strftime("%H:%M:%S.%f"), data["folder_home"], "stat.txt"),
                      "")
    checkout_positive("echo {} >> {}/{}".format(str(data["count_file"]), data["folder_home"], "stat.txt"), "")
    checkout_positive("echo  {} >> {}/{}".format(data["size_file"], data["folder_home"], "stat.txt"), "")
