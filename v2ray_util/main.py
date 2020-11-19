#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import pkg_resources

from .util_core.v2ray import V2ray
from .util_core.utils import ColorStr, open_port, loop_input_choice_number
from .global_setting import stats_ctr, iptables_ctr, ban_bt, update_timer
from .config_modify import base, multiple, ss, stream, tls, cdn


def help():
    exec_name = sys.argv[0]
    from .util_core.config import Config
    lang = Config().get_data('lang')
    print("""
{0} [-h|--help] [options]
    -h, --help           get help
    -v, --version        get version
    start                start V2Ray
    stop                 stop V2Ray
    restart              restart V2Ray
    status               check V2Ray status
    new                  create new json profile
    update               update v2ray to latest
    update.sh            update multi-v2ray to latest
    add                  random create mkcp + (srtp|wechat-video|utp|dtls|wireguard) fake header group
    add [wechat|utp|srtp|dtls|wireguard|socks|mtproto|ss]     create special protocol, random new port
    del                  delete port group
    info                 check v2ray profile
    port                 modify port
    tls                  modify tls
    tfo                  modify tcpFastOpen
    stream               modify protocol
    cdn                  cdn mode
    stats                v2ray traffic statistics
    iptables             iptables traffic statistics
    clean                clean v2ray log
    log                  check v2ray log
        """.format(exec_name[exec_name.rfind("/") + 1:]))


def updateSh():
    if os.path.exists("/.dockerenv"):
        subprocess.Popen("wget https://github.com/egrojlive/v2ray/archive/$(curl -s https://api.github.com/repos/egrojlive/v2ray/tags |grep name|grep -o '[0-9].*[0-9]'|head -n 1).zip -O /tmp/v2ray-util.zip >/dev/null 2>&1")
        subprocess.Popen("pip install -U /tmp/v2ray-util.zip >/dev/null 2>&1", shell=True).wait()
        subprocess.Popen("rm -r /tmp/v2ray-util.zip >/dev/null 2>&1", shell=True).wait()
        # subprocess.Popen("pip install -U v2ray_util", shell=True).wait()
    else:
        subprocess.Popen("curl -Ls https://raw.githubusercontent.com/egrojlive/v2ray/main/v2ray.sh -o temp.sh", shell=True).wait()
        subprocess.Popen("bash temp.sh -k && rm -f temp.sh", shell=True).wait()


def parse_arg():
    if len(sys.argv) == 1:
        return
    elif len(sys.argv) == 2:
        if sys.argv[1] == "start":
            V2ray.start()
        elif sys.argv[1] == "stop":
            V2ray.stop()
        elif sys.argv[1] == "restart":
            V2ray.restart()
        elif sys.argv[1] in ("-h", "--help"):
            help()
        elif sys.argv[1] in ("-v", "--version"):
            V2ray.version()
        elif sys.argv[1] == "status":
            V2ray.status()
        elif sys.argv[1] == "info":
            V2ray.info()
        elif sys.argv[1] == "port":
            base.port()
        elif sys.argv[1] == "tls":
            tls.modify()
        elif sys.argv[1] == "tfo":
            base.tfo()
        elif sys.argv[1] == "stream":
            stream.modify()
        elif sys.argv[1] == "stats":
            stats_ctr.manage()
        elif sys.argv[1] == "iptables":
            iptables_ctr.manage()
        elif sys.argv[1] == "clean":
            V2ray.cleanLog()
        elif sys.argv[1] == "del":
            multiple.del_port()
        elif sys.argv[1] == "add":
            multiple.new_port()
        elif sys.argv[1] == "update":
            V2ray.update()
        elif sys.argv[1] == "update.sh":
            updateSh()
        elif sys.argv[1] == "new":
            V2ray.new()
        elif sys.argv[1] == "convert":
            V2ray.convert()
        elif sys.argv[1] == "log":
            V2ray.log()
        elif sys.argv[1] == "cdn":
            cdn.modify()
    elif len(sys.argv) == 3:
        if sys.argv[1] == "stream":
            stream.modify(sys.argv[2])
        elif sys.argv[1] == "tls":
            tls.modify(sys.argv[2])
    else:
        if sys.argv[1] == "add":
            multiple.new_port(sys.argv[2])
    sys.exit(0)


def service_manage():
    show_text = (_("start v2ray"), _("stop v2ray"), _(
        "restart v2ray"), _("v2ray status"), _("v2ray log"))
    print("")
    for index, text in enumerate(show_text):
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number(_("please select: "), len(show_text))
    if choice == 1:
        V2ray.start()
    elif choice == 2:
        V2ray.stop()
    elif choice == 3:
        V2ray.restart()
    elif choice == 4:
        V2ray.status()
    elif choice == 5:
        V2ray.log()


def user_manage():
    show_text = (_("add user"), _("add port"), _("del user"), _("del port"))
    print("")
    for index, text in enumerate(show_text):
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number(_("please select: "), len(show_text))
    if not choice:
        return
    elif choice == 1:
        multiple.new_user()
    elif choice == 2:
        multiple.new_port()
        open_port()
    elif choice == 3:
        multiple.del_user()
    elif choice == 4:
        multiple.del_port()


def profile_alter():
    show_text = (_("modify email"), _("modify UUID"), _("modify alterID"), _("modify port"), _("modify stream"), _("modify tls"),
                 _("modify tcpFastOpen"), _("modify dyn_port"), _("modify shadowsocks method"), _("modify shadowsocks password"), _("CDN mode(need domain)"))
    print("")
    for index, text in enumerate(show_text):
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number(_("please select: "), len(show_text))
    if not choice:
        return
    elif choice == 1:
        base.new_email()
    elif choice == 2:
        base.new_uuid()
    elif choice == 3:
        base.alterid()
    elif choice == 4:
        base.port()
    elif choice == 5:
        stream.modify()
    elif choice == 6:
        tls.modify()
    elif choice == 7:
        base.tfo()
    elif choice == 8:
        base.dyn_port()
    elif choice == 9:
        ss.modify('method')
    elif choice == 10:
        ss.modify('password')
    elif choice == 11:
        cdn.modify()


def global_setting():
    show_text = (_("V2ray Traffic Statistics"), _("Iptables Traffic Statistics"), _(
        "Ban Bittorrent"), _("Schedule Update V2ray"), _("Clean Log"), _("Change Language"))
    print("")
    for index, text in enumerate(show_text):
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number(_("please select: "), len(show_text))
    if choice == 1:
        stats_ctr.manage()
    elif choice == 2:
        iptables_ctr.manage()
    elif choice == 3:
        ban_bt.manage()
    elif choice == 4:
        update_timer.manage()
    elif choice == 5:
        V2ray.cleanLog()
    elif choice == 6:
        from .util_core.config import Config
        config = Config()
        lang = config.get_data("lang")
        config.set_data("lang", "zh" if lang == "en" else "en")
        print(ColorStr.yellow(_("please run again to become effective!")))
        sys.exit(0)


def menu():
    V2ray.check()
    parse_arg()
    while True:
        print("")
        print(ColorStr.cyan(_("Welcome to v2ray-util")))
        print("")
        show_text = (_("1.V2ray Manage"), _("2.Group Manage"), _("3.Modify Config"), _(
            "4.Check Config"), _("5.Global Setting"), _("6.Update V2Ray"), _("7.Generate Client Json"))
        for index, text in enumerate(show_text):
            if index % 2 == 0:
                print('{:<20}'.format(text), end="")
            else:
                print(text)
                print("")
        print("")
        choice = loop_input_choice_number(_("please select: "), len(show_text))
        if choice == 1:
            service_manage()
        elif choice == 2:
            user_manage()
        elif choice == 3:
            profile_alter()
        elif choice == 4:
            V2ray.info()
        elif choice == 5:
            global_setting()
        elif choice == 6:
            V2ray.update()
        elif choice == 7:
            from .util_core import client
            client.generate()
        else:
            break


if __name__ == "__main__":
    menu()