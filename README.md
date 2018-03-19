# print2log #
Using decorator, minimal change required from replace any print statement. 

Simple and fast use this lib to add log file from your print statement with minimal change,
and more. 
1. better formating for the print and log, configurable 
2. additional log file with customized log_level, configurable 
3. catch function exception with raise error stop or continue running, configurable
4. catch function running time, configurable
5. display a colorful print based on log_level, configurable

# example #

```python
from  print2log import print_log, log_initial, print_recursion_tree
################ testing ############################
class testingA():
    @print_log
    def my_testing(self, t):
        print(t)
        print('info ', 'String 1', ' String 2 ', t)
        print('info ', t, {'  Dictionary': 'value'})
        print('warning ', t, {'My test ': 'My test result'})
        print('debug ', t, {' Debug': 'Good line'})
        print('error ', t, ('Error line', 'stop it here.'))
        print('critical: this is must print')

    @print_log
    def my_area(e):
        print('critical: this is must print')
        y = 1 / 0


@print_recursion_tree
def fib(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    return fib(n - 1) + fib(n - 2)

if __name__ == '__main__':
    
    log_initial('inital', 'c:\\paulwork\\testing\deploy\\log', 
        disable_color = False, function_run_time =False, exception_stop =False)
    a = testingA()
    a.my_testing('This is the first test string')

    a.my_area('Second test string')

    fib(5)
```
