'''
Created on May 15, 2012

@author: hugosenari
'''
import os, dbus, gobject
from plugnplay import Plugin
from dtc.core.interfaces.module import Module
from dtc.core.interfaces.notifiable import Notifiable
from dtc.core.interfaces.runnable import Runnable
from dtc.core.interfaces.loggable import Loggable
from dbus.mainloop.glib import DBusGMainLoop
import gsmdecode


DBUS_SESSION_MAEMO_ADDRESS = "DBUS_SESSION_MAEMO_ADDRESS"
DBUS_SYSTEM_MAEMO_ADDRESS = "DBUS_SYSTEM_MAEMO_ADDRESS"

class NotifyMaemo(Plugin):
    implements = [Module, Runnable]

    def __init__(self, *arg, **vargs):
        self.running = False
        self.maemo_ses_bus_addr = os.environ.get(DBUS_SESSION_MAEMO_ADDRESS, False)
        self.maemo_sys_bus_addr = os.environ.get(DBUS_SYSTEM_MAEMO_ADDRESS, False)
        self.maemo_ses_bus = None
        self.maemo_sys_bus = None
        DBusGMainLoop(set_as_default=True)

    #methods for module
    @property
    def version(self, *arg, **vargs):
        return 1

    @property
    def require(self, *args, **vargs):
        return None

    @property
    def priority(self, *args, **vargs):
        return 1

    @property
    def title(self, *args, **vargs):
        return "Maemo Notifications"

    @property
    def description(self, *args, **vargs):
        return "Show notifications from maemo"

    @property
    def author(self, *args, **vargs):
        return "hugosenari <hugosenari@gmail.com>"

    #methods from runnable
    def rerun(self, *args, **vargs):
        self.kill()
        self.run()

    def kill(self, *args, **vargs):
        self.maemo_ses_bus = None
        self.maemo_ses_bus_addr = None
        self.maemo_sys_bus = None
        self.maemo_sys_bus_addr = None
        self.running = False

    def is_running(self, *args, **vargs):
        return self.running

    def run(self, *args, **vargs):
        Loggable.info("Run notify_maemo", "Your NotifyMaemo plugin are running")
        self.running = True
        if (self.maemo_ses_bus_addr):
            try:
                self.maemo_ses_bus = dbus.bus.BusConnection(self.maemo_ses_bus_addr)
                self.connet_to_ses_signals()
            except:
                Loggable.warn("No CON", "Can't connect to session bus address: %s" % self.maemo_ses_bus_addr)
        else:
            Loggable.warn("No ENV", "No env value for %s" % DBUS_SESSION_MAEMO_ADDRESS)

        if (self.maemo_sys_bus_addr):
            try:
                self.maemo_sys_bus = dbus.bus.BusConnection(self.maemo_sys_bus_addr)
                self.connet_to_sys_signals()
            except Exception as e:
                Loggable.warn("No CON", "Can't connect to sys bus address: %s" % self.maemo_sys_bus_addr)
                print e
        else:
            Loggable.warn("No ENV", "No env value for %s" % DBUS_SYSTEM_MAEMO_ADDRESS)

    def connet_to_ses_signals(self):
        pass

    def connet_to_sys_signals(self):
        def handle_message(msgpdu, from_number, msg_hash, to_number, *args, **argsv):
            Loggable.debug("MSGPU: ", msgpdu)
            pdu = gsmdecode.decode_pdu(msgpdu)
            Notifiable.info("SMS: %s" % (pdu.get('sender'),), pdu.get('user_data', ''))
            Loggable.info("SMS: %s" % (pdu.get('sender'),), pdu.get('user_data', ''))

        #receive new sms
        self.maemo_sys_bus\
            .add_signal_receiver(
                                 handle_message,
                                 path='/com/nokia/phone/SMS',
                                 dbus_interface='Phone.SMS',
                                 signal_name='IncomingSegment')

        def handle_call(objPath, number, *args, **argsv):
            print args, argsv
            Notifiable.info("NEW CALL", "Someone calling you")

        #receive new call
        self.maemo_sys_bus\
            .add_signal_receiver(
                                 handle_call,
                                 path='/com/nokia/csd/call',
                                 dbus_interface='com.nokia.csd.Call',
                                 signal_name='Coming')

        Notifiable.info("Maemo Notify", "Wainting for new messages")
