# -*- coding: utf-8 -*-
# @Date    : 2017-06-12
# @Author  : lileilei 
import os, time, platform, time
import re

from adb.checkpath import getsystemsta
from ulit.log import logger, LOG

find = getsystemsta()


# 获取当前连接设备列表
@logger('获取当前连接设备列表')
def get_devices():
    cmd = 'adb devices'
    # os.popen(cmd) 从命令cmd打开一个管道，返回值是连接管道的文件对象，通过该对象可以进行读或写。
    content = os.popen(cmd)

    devices_info = content.readlines()

    devices = []

    for i in devices_info:
        if i.endswith('device\n'):
            devices.append(i.replace('\tdevice\n', ''))

    return devices


@logger('获取启动耗时')
def starttime_app(packagename, packagenameactivicy):  # 启动耗时
    cmd = 'adb shell am start -W -n %s' % packagenameactivicy
    me = os.popen(cmd).read().split('\n')[-7].split(':')  # 获取启动时间
    cmd2 = 'adb shell am force-stop %s' % packagename
    os.system(cmd2)
    return me


@logger('获取流量')
def liulang(packagename):
    cmd = 'adb shell ps  | %s %s' % (find, packagename)
    cm = os.popen(cmd).read().split()[1]
    cmd1 = "adb shell cat /proc/" + cm + "/net/dev | findstr wlan0"
    liul = os.popen(cmd1).read().split()
    me1_shou = liul[1]  # 接受
    me2_shou = liul[9]  # 上传
    time.sleep(2)
    cmd2 = "adb shell cat /proc/" + cm + "/net/dev | findstr wlan0"
    liul1 = os.popen(cmd2).read().split()
    me1_xia = liul1[1]  # 接受
    me2_xia = liul1[9]  # 上传
    me1 = int(int(me1_xia) - int(me1_shou)) / 1024
    me2 = int(int(me2_xia) - int(me2_shou)) / 1024
    liulang_sum = me1 + me2
    return me1, me2, liulang_sum


@logger('获取cpu信息')
def caijicpu(packagename):  # 这里采集的cpu时候可以是执行操作采集 就是-n  -d  刷新间隔
    # cpu = 'adb shell top -n 1| %s %s' % (find, packagename)
    # re_cpu = os.popen(cpu).read().split()[2]
    # return re_cpu
    cmd = 'adb -s {0} shell dumpsys cpuinfo {1}'.format(get_devices()[0], packagename)
    content = os.popen(cmd)
    cpuinfo = content.readlines()

    # 获取进程使用CPU
    for line in cpuinfo:
        if re.findall(packagename, line):
            cpulist = line.split(" ")
            while '' in cpulist:
                cpulist.remove('')  # 将list中的空元素删除
            print(cpulist)
            return cpulist[0].strip('%')  # 去掉百分号，返回一个float


@logger('获取内存')
def getnencun(packagename):  # Total 的实际使用过物理内存
    # cpu = 'adb shell top -n 1| %s %s' % (find, packagename)
    # print(cpu)
    # re_cpu = int(os.popen(cpu).read().split()[8][:-1]) / 1024
    # return re_cpu
    """
    PSS – Proportional Set Size 实际使用的物理内存（比例分配共享库占用的内存）
    USS – Unique Set Size 进程独自占用的物理内存（不包含共享库占用的内存）
    如果没有root权限的Android手机可能获取不到uss；
    """

    # cmd = 'adb shell "dumpsys meminfo |grep {}"'.format(check_app_pid()[0])
    cmd = 'adb shell dumpsys meminfo {0}'.format(packagename)

    content = os.popen(cmd)

    meminfo = content.readlines()

    total = "TOTAL"

    # 获取pss内存值
    for line in meminfo:
        if re.findall(total, line):  # 找到TOTAL 这一行
            pssnums = line.split(" ")  # 将这一行，按空格分割成一个list
            while '' in pssnums:  # 将list中的空元素删除
                pssnums.remove('')
            return int(pssnums[1]) / 1024  # 返回总共内存使用


@logger('执行monkey测试')
def adb_monkey(packagename, s_num, throttle, pct_touch, pct_motion, pct_trackball, pct_nav, pct_syskeys, pct_appswitch, num, logfilepath):
    cmden = 'adb shell monkey -p %s -s %s --throttle %s --pct-touch %s --pct-motion %s  --pct-trackball  %s  --pct-trackball %s  --pct-syskeys  %s  --pct-appswitch  %s   -v -v -v %s >%s' % (
        packagename, s_num, throttle, pct_touch, pct_motion, pct_trackball, pct_nav, pct_syskeys, pct_appswitch, num, logfilepath)
    os.popen(cmden)


@logger('获取设备状态')
def huoqushebeizhuangtai():  # 获取设备状态
    cmd1 = 'adb get-state'
    devices_status = os.popen(cmd1).read().split()[0]
    return devices_status
