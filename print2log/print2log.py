'''
using decorator, minimal change required from replace any print statement. 

Simple and fast use this lib to add log file from your print statement with minimal change,
and more. 
1. better formating for the print and log, configurable 
2. additional log file with customized log_level, configurable 
3. catch function exception with raise error stop or continue running, configurable
4. catch function running time, configurable
5. display a colorful print based on log_level, configurable
'''

from functools import wraps
import logging
import time
import traceback
import sys
import os
import builtins
import re

class Bcolors:
    '''
    define the fonts and color to print display. only test and work on win os.
    '''
    """Sets color codes for text printing"""
    OKBLUE = '\033[36m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
    def disable(self):
        self.OKBLUE = ''
        self.FAIL = ''
        self.ENDC = ''        


    def color_msg(self, msg, level):
        if level == 'ERROR':
            #msg = self.BOLD + self.FAILRED + str(msg).rstrip() + self.ENDC
            msg = '%s ERROR: %s%s' % (self.FAIL, msg, self.ENDC)
        elif level == 'CRITICAL':
            msg = '%s CRITICAL: %s%s' % (self.FAIL, msg, self.ENDC)
        elif level == 'WARNING':
            msg = '%s WARNING:  %s%s' % (self.OKBLUE, msg, self.ENDC)
        elif level == 'INFO':
            msg = '%s INFO: %s%s' % (self.OKBLUE, msg, self.ENDC)
        elif level == 'DEBUG':
            msg = '%s DEBUG:  %s%s' % (self.OKBLUE, msg, self.ENDC)
        else:
            msg = '%s DEBUG:  %s%s' % (self.OKBLUE, msg, self.ENDC)

        return msg.rstrip()


def print2log(fn):
    _print = builtins.print
    bc = Bcolors()

    def log(name):
        @wraps(print)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(name)
            msg = level = ''
            if args and kwargs:
                msg = '{}({}, {}):'.format(', '.join(args), kwargs)
            else:
                msg = '{}'.format(''.join(map(str, args))
                                  if args else '', kwargs if kwargs else '')

            # #CRITICAL,ERROR, WARNING,INFO, DEBUG, NOTSET
            if 'CRITICAL' in msg.upper():
                level = 'CRITICAL'
                redata = re.compile(re.escape(level), re.IGNORECASE)
                msg = redata.sub('', msg, 1)
                logger.critical(msg)
            elif 'ERROR' in msg.upper():
                level = 'ERROR'
                redata = re.compile(re.escape(level), re.IGNORECASE)
                msg = redata.sub('', msg, 1)
                logger.error(msg)
            elif 'WARNING' in msg.upper():
                level = 'WARNING'
                redata = re.compile(re.escape(level), re.IGNORECASE)
                msg = redata.sub('', msg, 1)
                logger.warning(msg)
            elif 'INFO' in msg.upper():
                level = 'INFO'
                redata = re.compile(re.escape(level), re.IGNORECASE)
                msg = redata.sub('', msg, 1)
                logger.info(msg)
            elif 'DEBUG' in msg.upper():
                level = 'DEBUG'
                redata = re.compile(re.escape(level), re.IGNORECASE)
                msg = redata.sub('', msg, 1)
                logger.debug(msg)
            else:
                level = '   '
                logger.debug(msg)
            msg = msg.lstrip()

            global gdisable_color
            if gdisable_color:
                bc.disable()
            
            msg = bc.color_msg(msg, level)
            #_print(msg)
            #_print('{0:10} : {1:8} => {2}'.format(name, level, msg))
            sys.stderr.write('{0:10} : {1:8} => {2}\n'.format(name, level, msg))
        return wrapper

    @wraps(fn)
    def wrapper(*args, **kwargs):
        # global print
        retval = None
        builtins.print, backup = log(fn.__name__), builtins.print
        t1 = time.time()
        global gfunction_run_time
        global gexception_stop
        #print('info', 'start: {1} -- at : {0:%Y-%m-%d %H:%M}'.format(t1, fn.__name__))
        if gfunction_run_time: 
            print('info', ' start : {0}'.format(fn.__name__))
        try:
            retval = fn(*args, **kwargs)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(
                exc_type, exc_value, exc_traceback)
            print(
                'Error', 'func name:  {0} -- params: args: {1}  kwargs: {2}'.format(fn.__name__, args, kwargs))
            print('Error', lines)
            if gexception_stop:
                raise
        if gfunction_run_time: 
            t2 = time.time()
            delta = t2 - t1
            print('info', 'end {0}  total run time : {1:.2f} sec '.format(
                fn.__name__, delta))
        builtins.print = backup
        return retval
    return wrapper


def print_recursion_tree(func):
    global _recursion_depth
    _print = builtins.print
    _recursion_depth = 0
    logger = logging.getLogger(func.__name__)
    def getpads():
        if _recursion_depth == 0:
            str_fn = '{} *'.format(' |  ' * (_recursion_depth - 1))
            str_other = '{}  __'.format(' |  ' * (_recursion_depth - 1))
            str_ret = '{}    '.format(' |  ' * (_recursion_depth - 1))
        else:
            str_fn = '    {} +  '.format(' |  ' * (_recursion_depth - 1))
            str_other = '    {} |  '.format(' |  ' * (_recursion_depth - 1))
            str_ret = '    {} |  '.format(' |  ' * (_recursion_depth - 1))

        return str_fn, str_ret, str_other

    def indentedprint():
        @wraps(print)
        def wrapper(*args, **kwargs):
            str_fn, str_ret, str_other = getpads()
            _print(str_other, end=' ')
            _print(*args, **kwargs)
        return wrapper

    @wraps(func)
    def wrapper(*args, **kwargs):
        global _recursion_depth
        global print

        str_fn, str_ret, str_other = getpads()

        if args and kwargs:
            _print(str_fn, '({}, {}):'.format(
               ', '.join(args), kwargs))
        else:
            _print(str_fn, '({}):'.format(', '.join(
                map(str, args)) if args else '', kwargs if kwargs else ''))
        line =str_fn + '({}):'.format(', '.join(map(str, args)) if args else '', kwargs if kwargs else '')                
        logger.critical(line)
        _recursion_depth += 1
        print, backup = indentedprint(), print
        retval = func(*args, **kwargs)
        print = backup
        _recursion_depth -= 1
        _print(str_ret, '--', retval)
        line = str_ret + '--' + str(retval)
        #logger.critical(line)
        
        if _recursion_depth == 0:
            _print()
        return retval

    return wrapper

def log_initial(file_name, path, 
                log_level='ERROR', 
                log_formatter = '%(asctime)s : %(name)-12s - %(levelname)-8s => %(message)s',
                print_formatter =  '%(name)-12s - %(levelname)-8s => %(message)s',
                exception_stop = False, 
                disable_color = False,
                function_run_time = True):
    '''
    file_name: log file name without extension (.log)
    path: log path
    log_level: define the level and above write into log file. no effect on print on screen
    exception_stop = True if catch exception than raise error and stop the script. False, log/print error, but continue.
    log_formatter = print format
    disable_color = True not print in color.
    function_run_time = True, display each decorated function runtime
    '''
    log_file = os.path.join(path, file_name + '.log')
    logging.basicConfig(filename=log_file,
                        format=log_formatter, level=log_level)
    logger = logging.getLogger(file_name)
    print('Log File Location : {0}'.format(log_file))
    global gprint_formatter , gexception_stop,gdisable_color,gfunction_run_time
    gprint_formatter = print_formatter
    gexception_stop= exception_stop
    gdisable_color = disable_color
    gfunction_run_time = function_run_time    


glog_formatter= '%(asctime)s : %(name)-12s - %(levelname)-8s => %(message)s'
gprint_formatter = '%(name)-12s - %(levelname)-8s => %(message)s'
gexception_stop= False
gdisable_color = False
gfunction_run_time = True

print_log = print2log

if __name__ == '__main__':
    pass
    
