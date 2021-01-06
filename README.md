# roblox-status-notifier
A small program I've built in Python to notify you of when a user on
roblox comes online, or goes offline.

# How to use
To use this, you must first launch the program. This requires Python to
be installed on this machine.

Once you launch the program, it will create an IDs text file in the same
directory as the program. Put the ID of every user you wish to monitor on
individual lines, save it, then relaunch the program, and you should be
set to go.

# Alerts & Notifications.
This program alerts the user via notifications. If you don't want them,
then set the allow_notifications variable in the script to False.

If you do want notifications however, don't touch that variable. On
Windows, this uses the win10toast module, so you will need to install
that on both Linux and Windows (even though you don't need it on Linux.)

For notifications on Linux, you will need a notification daemon installed,
(most Desktop Environments come with their own notification daemon, but you
can install your own if you're using something like a plain Window Manager
like i3, or dwm) as well as the notify-send package.

Otherwise, if all else fails, i.e a lack of a notification daemon, or the
notify-send package for example, it will simply print to the console.

# Further Configuration.
You can modify how long it takes between each check of users being online,
by modifying the PING_DURATION variable (it's measured in seconds), and
the lifetime of the notification (Windows only), with the NOTIF_LIFETIME
variable.
