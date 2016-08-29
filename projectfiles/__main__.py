#!/usr/bin/env python3

# sys is used for the sys.exit function and to check python version
import sys, os

# Check the python version
if sys.version_info[0] != 3 or sys.version_info[1] < 2:
    print("Sorry, your python version is not compatable")
    print("This program requires python 3.2 or later")
    print("Program exiting")
    sys.exit(1)

# argparse is used to pass the port and check value
import argparse

# used to run the python wsgi server
from wsgiref.simple_server import make_server

# the skipoles package contains your own code plus
# the skipole framework code
import skipoles 

# Sets up a parser to get port and check value
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='Robotics Telescope Raspberry Pi 01 web service',
                                 epilog='Stop the server with ctrl-c')

parser.add_argument("-p", "--port", type=int, dest="port", default=8000,
                  help="The port the web server will listen at, default 8000")


# If option is not used, delete this bit 
parser.add_argument("-o", "--option", dest="option",
                  help="A value passed to your check_session function")

parser.add_argument('--version', action='version', version=('%(prog)s 0.0'))

args = parser.parse_args()

print("Loading site")

# The skipoles.load_project() function requires the project name,
# and the location of the 'projectfiles' directory, normally in the same
# directory as this script

projectfiles = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'projectfiles')

site = skipoles.load_project("pi01", projectfiles)

if site is None:
    print("Project not found")
    sys.exit(1)


# If option is not used, delete this bit 
site.check = args.option

# if it is required to set any subproject option value, use
# site.set_subproject_check(projectname, optionvalue)

# This 'site' object can now be used in a wsgi app function
# by calling its 'respond' method, with the environ as argument.
# The method returns status, headers and the page data
# so call it using:
# status, headers, data = site.respond(environ)


def the_app(environ, start_response):
    "Defines the wsgi application"
    # uses the 'site' object created previously
    status, headers, data = site.respond(environ)
    start_response(status, headers)
    return data

# serve the site, using the python wsgi web server

httpd = make_server('', args.port, the_app)
print("Serving on port " + str(args.port) + "...")
print("Press ctrl-c to stop")

# Serve until process is killed
httpd.serve_forever()