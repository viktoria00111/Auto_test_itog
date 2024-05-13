import yaml
from sshcheckers import ssh_checkout_negative
from sshcheckers import upload_files

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def test_step1(clear_folders, make_files, make_badarx):
    assert ssh_checkout_negative(data["host"], data["user"], "12345",
                                 "cd {}; 7z e badarx.7z -o{} -y".format(data["folder_out"], data["folder_ext"]),
                                 "ERROR"), "Test 4 Fail"


def test_step2():
    assert ssh_checkout_negative(data["host"], data["user"], "12345",
                                 "cd {}; 7z t badarx.7z".format(data["folder_out"]),
                                 "ERROR"), "Test 5 Fail"
