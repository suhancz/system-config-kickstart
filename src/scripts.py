#!/usr/bin/python3
#
# Chris Lumens <clumens@redhat.com>
# Brent Fox <bfox@redhat.com>
# Tammy Fox <tfox@redhat.com>
#
# Copyright (C) 2000-2007 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2 or, at your option, any later version.  This
# program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc.

import gtk
import gtk.glade
import getopt
import string
from pykickstart.parser import Script
from pykickstart.constants import *

class scripts:
    def __init__(self, xml, ksHandler):
        self.ks = ksHandler
        self.chroot_checkbutton = xml.get_widget("chroot_checkbutton")
        self.interpreter_checkbutton = xml.get_widget("interpreter_checkbutton")
        self.interpreter_entry = xml.get_widget("interpreter_entry")
        self.pre_interpreter_checkbutton = xml.get_widget("pre_interpreter_checkbutton")
        self.pre_interpreter_entry = xml.get_widget("pre_interpreter_entry")
        self.pre_textview = xml.get_widget("pre_textview")
        self.post_textview = xml.get_widget("post_textview")

        self.interpreter_checkbutton.connect("toggled", self.interpreter_cb)
        self.pre_interpreter_checkbutton.connect("toggled", self.pre_interpreter_cb)

    def updateKS(self, ksHandler):
        self.ks = ksHandler

    def interpreter_cb(self, args):
        self.interpreter_entry.set_sensitive(self.interpreter_checkbutton.get_active())

    def pre_interpreter_cb(self, args):
        self.pre_interpreter_entry.set_sensitive(self.pre_interpreter_checkbutton.get_active())

    def formToKickstart(self):
        self.ks.scripts = []
        self.preData()
        self.postData()

    def preData(self):
        pre_buffer = self.pre_textview.get_buffer()
        data = pre_buffer.get_text(pre_buffer.get_start_iter(),pre_buffer.get_end_iter(),True)
        data = string.strip(data)

        if data == "":
            return

        preScripts = [s for s in self.ks.scripts if s.type == KS_SCRIPT_PRE]

        if len(preScripts) == 0:
            script = Script("", type=KS_SCRIPT_PRE)
        else:
            script = preScripts[0]

        if self.pre_interpreter_checkbutton.get_active():
            script.interp = self.pre_interpreter_entry.get_text()
        else:
            script.interp = ""

        script.script = data

        if len(preScripts) == 0:
            self.ks.scripts.append(script)

    def postData(self):
        post_buffer = self.post_textview.get_buffer()
        data = post_buffer.get_text(post_buffer.get_start_iter(),post_buffer.get_end_iter(),True)
        data = string.strip(data)

        if data == "":
            return

        postScripts = [s for s in self.ks.scripts if s.type == KS_SCRIPT_POST]

        if len(postScripts) == 0:
            script = Script("", type=KS_SCRIPT_POST)
        else:
            script = postScripts[0]

        if self.chroot_checkbutton.get_active():
            script.inChroot = False
        else:
            script.inChroot = True

        if self.interpreter_checkbutton.get_active():
            script.interp = self.interpreter_entry.get_text()
        else:
            script.interp = ""

        script.script = data

        if len(postScripts) == 0:
            self.ks.scripts.append(script)

    def applyKickstart(self):
        preScripts = [s for s in self.ks.scripts if s.type == KS_SCRIPT_PRE]
        postScripts = [s for s in self.ks.scripts if s.type == KS_SCRIPT_POST]

        # We're kind of a crappy UI and assume they only have one script.
        if len(preScripts) > 0:
            script = preScripts[0]

            if script.interp != "":
                self.pre_interpreter_checkbutton.set_active(True)
                self.pre_interpreter_entry.set_text(script.interp)

            self.pre_textview.get_buffer().set_text(script.script)

        if len(postScripts) > 0:
            script = postScripts[0]

            if script.interp != "":
                self.interpreter_checkbutton.set_active(True)
                self.interpreter_entry.set_text(script.interp)

            if script.inChroot == False:
                self.chroot_checkbutton.set_active(True)

            self.post_textview.get_buffer().set_text(script.script)
