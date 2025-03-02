#!py -3
# -*- coding: utf-8 -*-

"""
Vincy SHI, partial-derivative (c) 2024-2025
date: 2024-03-21
update: 2025-03-02
本工具的功能是为 Windows 文件夹设置友好别名。
在资源管理器中，例如「用户」「桌面」「收藏夹」等文件夹将以中文显示，但不影响其原始路径 "Users", "Desktop" 和 "Favorites"。
在实践中，我们往往会遇到一些工具或项目不支持中文路径，但又希望在资源管理器中以中文显示，这时候就可以使用本工具为文件夹设置这样的友好别名。
请在本工具弹出的命令框中先输入需要更名的文件夹路径，敲击回车；再输入别名，敲击回车。
注意，1.具有别名的文件夹不能够在资源管理器中重命名真实路径，你将需要借助本工具来删除别名或修改路径名称。
      2.本工具会使文件夹及其子文件夹显示为只读属性，这是刷新文件夹别名导致的。除了右键-属性-只读中的方框被框选，并无其他副作用。
"""

import configparser
import ctypes
import os
import platform
import sys

try:
    # 操作系统识别和路径准备
    if platform.system() != "Windows":
        input("本工具仅支持 Windows。")
        exit(-1)
    SYS_VERSION = platform.version().split(".")[0]
    SYS_ENCODING = "utf-16" if SYS_VERSION in ["10", "11"] else "ANSI"
    print("Windows 内核版本：" + SYS_VERSION)
    full_dir, _ = os.path.split(__file__)
    print("当前路径：" + full_dir)

    # 管理员权限的检查与获取
    if not ctypes.windll.shell32.IsUserAnAdmin():
        SW_NORMAL = 0x1
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'-u "{__file__}"', None, SW_NORMAL
        )
        print("请在新窗口完成操作... ")
        exit(0)

    # 用户交互和准备配置内容
    print(__doc__)
    target_dir = input("请输入希望更名的文件夹路径: ")
    folder_dir, _, folder_name = target_dir.rpartition("/")
    ini_file_path = os.path.join(target_dir, "desktop.ini")
    config = configparser.ConfigParser()
    config.read(ini_file_path, SYS_ENCODING)
    if config.has_option(".ShellClassInfo", "LocalizedResourceName"):
        parent_dir, dir_name = os.path.split(target_dir)
        alias = config.get(".ShellClassInfo", "LocalizedResourceName")
        option = input(
            f'文件夹 "{dir_name}" 已定义别名 "{alias}"。\n'
            "您希望 修改本名(0) / 修改别名(1) / 清除别名(2) / 取消(-1): "
        )
        if option == "0":
            dir_name = input("请输入修改的文件夹本名: ")
            os.rename(target_dir, os.path.join(parent_dir, dir_name))
            input("已修改。不影响别名的显示。")
            exit(0)
        elif option == "1":
            alias = input("请输入修改的文件夹别名: ")
            config.set(".ShellClassInfo", "LocalizedResourceName", alias)
        elif option == "2":
            config.remove_option(".ShellClassInfo", "LocalizedResourceName")
        else:
            input("已取消。")
            exit(0)
    elif config.has_section(".ShellClassInfo"):
        alias = input("请输入添加的文件夹别名: ")
        config.set(".ShellClassInfo", "LocalizedResourceName", alias)
    else:
        alias = input("请输入添加的文件夹别名: ")
        config.add_section(".ShellClassInfo")
        config.set(".ShellClassInfo", "LocalizedResourceName", alias)

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
        full_dir,
        None,
    )
    folder_disk, _, folder_path = target_dir.rpartition(":")
    os.system(''.join(["attrib +r ",folder_disk,":\\",folder_path]))
    input("已提交。Windows 将在几分钟内同步。")

except Exception as e:
    print(e)
    input("出现错误。")
