"""
This package will be called by the Skipole framework to access your data.
"""


import sys, time

from .. import FailPage, GoTo, ValidateError, ServerError, use_submit_list

from . import control, login, database_ops, hardware


# any page not listed here requires basic authentication
_PUBLIC_PAGES = [1,  # index
                 2,  # sensors
                 4,  # information
                 6,  # controls.json
                 7,  # sensors.json
                 9,  # sernsors_refresh,
               540,  # no_javascript
              1002,  # css
              1004,  # css
              1006   # css
               ]


def start_project(project, projectfiles, path, option):
    """On a project being loaded, and before the wsgi service is started, this is called once,
       Note: it may be called multiple times if your web server starts multiple processes.
       This function should return a dictionary (typically an empty dictionary if this value is not used).
       Can be used to set any initial parameters, and the dictionary returned will be set in the
       'skicall.proj_data' attribute."""
    proj_data = {}

    # checks database exists, if not create it
    database_ops.start_database(project, projectfiles)


    # a time delay may be required here to give other services time to start
    # this has been found to be necessary in some situations if the service is
    # started on boot up and a network connection such as an mqtt client is needed
    # time.sleep(10)

    # setup hardware
    hardware.initial_setup_outputs()

    # get dictionary of initial start-up output values from database
    output_dict = database_ops.power_up_values()
    if not output_dict:
        print("Invalid read of database, delete setup directory to revert to defaults")
        sys.exit(1)

    # set the initial start-up values
    control.set_multi_outputs(output_dict)

    return proj_data


def start_call(called_ident, skicall):
    "When a call is initially received this function is called."
    if not called_ident:
        return
    if skicall.environ.get('HTTP_HOST'):
        # This is used in the information page to insert the host into a displayed url
        skicall.call_data['HTTP_HOST'] = skicall.environ['HTTP_HOST']
    else:
        skicall.call_data['HTTP_HOST'] = skicall.environ['SERVER_NAME']
    # password protected pages
    if called_ident[1] not in _PUBLIC_PAGES:
        # check login
        if not login.check_login(skicall.environ):
            # login failed, ask for a login
            return (skicall.project,2010)
    return called_ident


@use_submit_list
def submit_data(skicall):
    """This function is called when a Responder wishes to submit data for processing in some manner
       For two or more submit_list values, the decorator ensures the matching function is called instead"""

    raise FailPage("submit_list string not recognised")


def end_call(page_ident, page_type, skicall):
    """This function is called at the end of a call prior to filling the returned page with page_data,
       it can also return an optional ident_data string to embed into forms."""
    # in this example, status is the value on input02
    status = hardware.get_text_input('input02')
    if status:
        skicall.page_data['topnav','status', 'para_text'] = status
    else:
        skicall.page_data['topnav','status', 'para_text'] = "Status: input02 unavailable"
    return