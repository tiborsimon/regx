from termcolor import colored


yellow = lambda x: colored(x, 'yellow', attrs=['bold'])

if __name__ == '__main__':
    print(yellow('REGX command line python interface entry point.'))

