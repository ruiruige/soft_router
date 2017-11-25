#!/usr/bin/env python
# coding=utf-8

import subprocess

import dns.resolver
import psutil


pid_list = psutil.pids()
cmdline_list = [" ".join(psutil.Process(pid).cmdline()) for pid in pid_list]


def check_process(name=None):
    for cmdline in cmdline_list:
        if name in cmdline:
            return True
    return False


def check_listen_port(port=None):
    pass


def native_shell(cmd=None):
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = pipe.communicate()
    return stdout, stderr


def get_proc_max_fd(pid=None):
    cmd = "cat /proc/%d/limits | grep 'Max open files' | awk '{print $5}'" % pid
    # Max open files 65535 65535 files
    # $1   $2   $3     $4    $5    $6~
    stdout, stderr = native_shell(cmd=cmd)
    if stderr:
        print("get_proc_max_fd of %d failed, errmsg is %s" % (pid, stderr))
        return stderr
    return int(stdout.strip())


def get_pid_by_cmdline(name=None):
    for pid in pid_list:
        cmdline = " ".join(psutil.Process(pid).cmdline())
        if name in cmdline:
            return pid


def check_dns():
    def check_dns_resolve():
        print("checking DNS resolve")
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = ['127.0.0.1']
        my_resolver.port = 54

        try:
            answer = my_resolver.query('google.com')
            for i in answer.response.answer:
                print i
        except dns.resolver.NXDOMAIN:
            print("DNS resolve check failed")
        else:
            print("DNS resolve check OK")
        finally:
            print(" ")

    def check_dnsmasq():
        print("checking dnsmasq")
        rst = check_process(
            name="/usr/sbin/dnsmasq -x /var/run/dnsmasq/dnsmasq.pid -u dnsmasq")
        if not rst:
            print("process dnsmasq does not exist")
        else:
            print("process dnsmasq OK")
        print(" ")

    def check_overture():
        print("checking overture")
        rst = check_process(
            name="/root/install/overture/overture-linux-amd64")
        if not rst:
            print("process overture does not exist")
        else:
            print("process overture OK")
        print(" ")

    check_dnsmasq()
    check_overture()
    check_dns_resolve()


def check_TcpRoute():
    print("checking TcpRoute process")
    rst = check_process(
        name="/root/install/TcpRoute2/TcpRoute2-linux-amd64")
    if not rst:
        print("process TcpRoute does not exist")
        return
    else:
        print("process TcpRoute OK")
    print(" ")

    print("checking TcpRoute max fd limit")
    pid = get_pid_by_cmdline(
        name="/root/install/TcpRoute2/TcpRoute2-linux-amd64")
    max_fd_num = get_proc_max_fd(pid=pid)
    if max_fd_num < 1100:
        print("max_fd_num is %d ,error !" % max_fd_num)
    else:
        print("checking TcpRoute max fd OK")


def check_redsocks():
    print("checking redsocks process")
    rst = check_process(
        name="/usr/local/bin/redsocks -c /etc/redsocks.conf")
    if not rst:
        print("process redsocks does not exist")
        return
    else:
        print("process redsocks OK")
    print(" ")

    print("checking redsocks max fd limit")
    pid = get_pid_by_cmdline(
        name="/usr/local/bin/redsocks -c /etc/redsocks.conf")
    max_fd_num = get_proc_max_fd(pid=pid)
    if max_fd_num < 1100:
        print("max_fd_num is %d ,error !" % max_fd_num)
    else:
        print("checking redsocks max fd OK")


def check_internal_ip():
    pass


def check_all():
    check_dns()
    check_TcpRoute()
    check_redsocks()


if __name__ == '__main__':
    check_all()
