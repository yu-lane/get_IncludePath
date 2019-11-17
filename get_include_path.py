# _*_ coding:utf-8 _*_

"""
this module could generate the folder path that contain .h file
and make these path could use in:
vscode c_cpp_propertied.json setting
and iar include path setting
default platform is vscode
if you want other platform, input agrv after file
such as: python3 get_include_path.py iar
"""
import os
import sys

c_cpp_property_str_head = """{
    "configurations": [
        {
            "name": "Win32",
            "includePath": [
"""
c_cpp_property_str_tail = """            ],
            "intelliSenseMode": "${default}",
            "defines": [
                "STM32F072",
                "GASSAN_UPS",
                "USE_STDPERIPH_DRIVER",
                "USE_STM32072B_EVAL",
                "HSI48_USE"
            ],
            "browse": {
                "path": [


                ],
                "limitSymbolsToIncludedHeaders": true,
                "databaseFilename": ""
            }
           
            
        }
    ],
    "version": 4
}"""


def get_son_path_list():
    """
    获取工作目录下含有.h文件的文件夹路径
    获取的路径是绝对路径
    """
    path = os.path.abspath('.') #获取当前工作目录路径
    include_path = []              #初始化一个list
    for home, dirs, files in os.walk(path):
        for file_name in files:
            f_name, f_extend = os.path.splitext(file_name)
            if f_extend == '.h':
                include_path.append(home)
                break

    return include_path

def mkdir(folder_name):
    """
    在当前目录下创建一个文件夹, 参数为文件夹名称
    """
    path = os.path.abspath('.') #获取当前工作目录路径
    path = path +"\\"+ folder_name
    print(path)
    if os.path.exists(path):
       print("folder exists\n")
    else:
        os.makedirs(path)
        print("folder created\n")

def relative_path(roott_path, path_list, platform="vscode"):
    r"""
    将绝对路径中的工作目录路径换成${workspaceRoot}: vscode
    如果是IAR，则替换成$PROJ_DIR$\..
    """
    path_return = []
    if platform is "vscode":
        root_symble = "${workspaceRoot}"
    if platform is "iar":
        root_symble = "$PROJ_DIR$\\.."
    print("platform work root folder symble is %s" %(root_symble))

    for _path in path_list:
        path_return.append(_path.replace(roott_path, root_symble))
    return path_return

def gen_include_string(dir_list, platform="vscode"):
    """
    #生成一个包含引号/换行/.h文件路径的人可读的文件
    """
    dst_string = ""
    
    for _path in dir_list:
        if platform is "vscode":
            dst_string += "\t\t\t\t\""
            dst_string += _path.replace("\\", "/")
            dst_string += "\""
            if _path != dir_list[-1]:
                dst_string += ","
            dst_string += "\n"
            #dst_file.write("\"")
            #_path.replace("\\\\","/")
        else:
            dst_string += _path
            #dst_file.write(_path)
            dst_string += "\n"
    
    return dst_string

def write_h_to_file(w_string, file_name="include_path.txt"):
    """
    generate a file contain path that have .h files
    """
    dst_file = open(file_name, "w")
    dst_file.write(w_string)
    dst_file.close()

def write_property_file(w_string, file_name="c_cpp_properties.txt"):
    """
    generate a c_cpp_properties config file
    """
    mkdir(".vscode")

    dst_string = ""
    dst_string += c_cpp_property_str_head
    dst_string += w_string
    dst_string += c_cpp_property_str_tail

    dst_file = open(r".\.vscode\\"+file_name, "w")
    dst_file.write(dst_string)
    dst_file.close()

if __name__ == '__main__':
    PLATFORM = 'vscode'
    print("default platform is %s" %(PLATFORM))
    print("if you want other platform, input agrv after file")
    print("support platform is vscode and iar")

    print(sys.argv[-1])
    if (sys.argv[-1]) == "iar":
        PLATFORM = "iar"
    print("platform is %s" %(PLATFORM))

    INCLIDE_PATH = get_son_path_list()
    ROOT_PATH = os.path.abspath(".")
    REAL_PATH = relative_path(ROOT_PATH, INCLIDE_PATH, PLATFORM)
    if PLATFORM is "vscode":
        write_property_file(gen_include_string(REAL_PATH, PLATFORM), "c_cpp_properties.json")
    else:
        write_h_to_file(gen_include_string(REAL_PATH, PLATFORM), "include_path.txt")
    print('Done')
    