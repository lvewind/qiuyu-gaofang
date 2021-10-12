import PyInstaller.__main__
import sys
import re
import time

version_str = """
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2020,6,17,1747),
    prodvers=(2020,6,17,1747),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Microsoft Corporation'),
        StringStruct(u'FileDescription', u'Kiki'),
        StringStruct(u'FileVersion', u'2021.4.28.1747'),
        StringStruct(u'InternalName', u'HiWorker'),
        StringStruct(u'LegalCopyright', u'\xa9 lvewind'),
        StringStruct(u'OriginalFilename', u'Kiki.exe'),
        StringStruct(u'ProductName', u'Kiki'),
        StringStruct(u'ProductVersion', u'1.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""


def upgrade_version_file(version_code: str):

    data_time = time.localtime(time.time())
    filevers = str(data_time[0]) + "," + str(data_time[1]) + "," + str(data_time[2]) + "," + "2020" + str(data_time[3]) + str(data_time[4])
    file_version = str(data_time[0]) + "." + str(data_time[1]) + "." + str(data_time[2]) + "." + str(data_time[3]) + str(data_time[4])
    old_filevers = re.search(r"\d*[,]\d*[,]\d*[,]\d*", version_code).group(0)    # 找第一个匹配字符串
    version_code = version_code.replace(old_filevers, filevers)

    old_file_version = re.search(r"\d*[.]\d*[.]\d*[.]\d*", version_code).group(0)    # 找第一个匹配字符串
    version_code = version_code.replace(old_file_version, file_version)
    print(version_code)
    with open("version.txt", "w+", encoding="utf-8") as fw:
        fw.writelines(version_code)
        # fw.write(version_code)
        
        
if __name__ == '__main__':
    sys.setrecursionlimit(10240)
    package_name = "Kiki"
    scriptname = "launch.py"
    upgrade_version_file(version_str)
    version_file = "version.txt",

    PyInstaller.__main__.run([
        '--name=%s' % package_name,
        '--onefile',
        '--key=15rMJf3kqTFtyPiw',
        '--version-file=%s' % version_file,
        '--uac-admin',
        # '--windowed',
        # '--add-binary=%s' % os.path.join('resource', 'path', '*.png'),
        # '--add-data=%s' % os.path.join('resource', 'path', '*.txt'),
        # '--icon=%s' % os.path.join('resource', 'path', 'icon.ico'),
        # os.path.join('my_package', '__main__.py'),
        scriptname
    ])
