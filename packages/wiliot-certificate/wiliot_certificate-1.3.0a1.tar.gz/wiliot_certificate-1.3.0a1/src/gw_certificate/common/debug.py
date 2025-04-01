import datetime
import logging
import os
import colorama
import tabulate
import pprint


# Debugging & Printing
def debug_print(txt, pretty=False, center=False, tab=False, color=None, enable=True):
    """
    :type txt: string
    :param txt: text to print
    :type pretty: bool
    :param pretty: pretty print
    :type center: bool
    :param center: print with stars (*)
    :type tab: bool
    :param tab: tabulate input
    :type color: str
    :param color: colorama color code
    """
    if enable:
        if tab:
            txt = '\n' + tabulate.tabulate(txt, tablefmt='rst')
        if type(txt) != str:
            try:
                txt = str(txt)
            except TypeError:
                debug_print('Could not Print!')
        if center:
            txt = txt.center(94, '-')
        if color is not None:
            txt = eval(f'colorama.Fore.{color}') + txt + colorama.Style.RESET_ALL
        if pretty:
            txt = pprint.pformat(txt, sort_dicts=False)

        # Print Text
        if logging.getLogger().hasHandlers():
            log = logging.getLogger()
            log.info(txt)
        else:
            print(datetime.datetime.now().strftime("[%d/%m/%Y, %H:%M:%S]: ") + txt)

def is_databricks():
    """returns if running in databricks"""
    try:
        get_ipython().__class__.__name__
        return True
    except NameError:
        return False


def is_databricks():
    try:
        from IPython import get_ipython
        if "IPKernelApp" not in get_ipython().config:
            return False
        if "VSCODE_PID" in os.environ:
            return False
        return True
    except Exception as e:
        return False
