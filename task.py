import configparser
import ctypes
import os
import platform
import sys
import subprocess

target_dir = " "
folder_dir = " "
folder_name = " "
alias = " "
ini_file_path = " "
SYS_VERSION = platform.version().split(".")[0]
SYS_ENCODING = "utf-16" if SYS_VERSION in ["10", "11"] else "ANSI"
config = configparser.ConfigParser()
check = False
def nick_name(target_folder: str, nickname: str, option):

    global target_dir, folder_dir, folder_name, ini_file_path, alias
    target_dir = target_folder
    folder_dir, _, folder_name = target_dir.rpartition("/")
    ini_file_path = os.path.join(target_dir, "desktop.ini")
    alias = nickname

    if target_dir.strip():
        #target_dir.strip():target_dir!=null
        if option == 0 and alias.strip():
            create()
        elif option == 1:
            delete()
        else:
            pass #err
    else:
        pass #err
    return check
def create():
     config.read(ini_file_path, SYS_ENCODING)
     if config.has_option(".ShellClassInfo", "LocalizedResourceName") or config.has_section(".ShellClassInfo"):
         #若有配置文件，则更改别名
         config.set(".ShellClassInfo", "LocalizedResourceName", alias)
         change_ini()
     else:
        config.add_section(".ShellClassInfo")
        config.set(".ShellClassInfo", "LocalizedResourceName", alias)
        change_ini()

def delete():
    config.read(ini_file_path, SYS_ENCODING)
    if config.has_option(".ShellClassInfo", "LocalizedResourceName") or config.has_section(".ShellClassInfo"):
        # 若有配置文件，则删除别名，否则退出
        config.remove_option(".ShellClassInfo", "LocalizedResourceName")
        change_ini()
    else:
        pass
        # del
def change_ini():
    global check
    try:
        # 写入配置并提交系统更改请求
        FILE_ATTRIBUTE_HIDDEN = 0x00000002
        FILE_ATTRIBUTE_SYSTEM = 0x00000004
        FILE_ATTRIBUTE_ARCHIVE = 0x00000020
        SHCNE_ATTRIBUTES = 0x00000002
        SHCNE_UPDATEDIR = 0x00001000
        SHCNE_UPDATEITEM = 0x00002000
        SHCNF_PATHW = 0x0005
        SHCNF_FLUSH = 0x1000
        ctypes.windll.kernel32.SetFileAttributesW(ini_file_path, FILE_ATTRIBUTE_ARCHIVE)
        with open(ini_file_path, "w", encoding=SYS_ENCODING) as configfile:
            config.write(configfile, space_around_delimiters=False)
        ctypes.windll.kernel32.SetFileAttributesW(
            ini_file_path,
            FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM | FILE_ATTRIBUTE_ARCHIVE,
        )
        ctypes.windll.shell32.SHChangeNotify(
            SHCNE_ATTRIBUTES | SHCNE_UPDATEITEM,
            SHCNF_PATHW | SHCNF_FLUSH,
            ini_file_path,
            None,
        )
        ctypes.windll.shell32.SHChangeNotify(
            SHCNE_ATTRIBUTES | SHCNE_UPDATEDIR | SHCNE_UPDATEITEM,
            SHCNF_PATHW | SHCNF_FLUSH,
            target_dir,
            None,
        )
        folder_disk, _, folder_path = target_dir.rpartition(":")
        run_cmd(''.join(["attrib +r ",folder_disk,":\\",folder_path]))
    except Exception as e:
        check = False
        print("出现错误。")
        return False
    check = True
    return True
# command ：需要执行的cmd命令
# 0x08000000: 屏蔽命令
def run_cmd(command):
    subprocess.call(command, creationflags=0x08000000)

if __name__ == '__main__':
    pass  # result: 3