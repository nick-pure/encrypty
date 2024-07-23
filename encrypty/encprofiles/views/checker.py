from .responses import Er

def print_arr(arr):
    string = str()
    for el in arr:
        string = string + ', ' + el
    return string[1:]

def print_or_arr(arrarr):
    string = str()
    for i in range(len(arrarr) - 1):
        string = string + arrarr[i][0]
        for j in range(1 ,len(arrarr[i]) - 1):
            string = string + ', ' + arrarr[i][j]
        string = string + ' or '
    string = string + arrarr[len(arrarr) - 1][0]
    for j in range(1, len(arrarr[i]) - 1):
        string = string + ', ' + arrarr[i][j]
    return string
    
def single_way_check(*required):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method == 'GET':
                data = request.GET
                missed = list()
                for r in required:
                    if r not in data:
                        missed.append(r)
                if len(missed) == 0:
                    return func(request, *args, **kwargs)
                return Er(f'Missing arguments : {print_arr(missed)}', 405)
            elif request.method == 'POST':
                data = request.POST
                for r in required:
                    if r not in data:
                        return Er(f'Missing arguments : {r}', 405)
                return func(request, *args, **kwargs)
            else:
                return Er('Invalid HTTP method', 405)
        return wrapper
    return decorator

def few_ways_checker(*required):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method == 'GET':
                data = request.GET
                flag = False
                missed_arr = list()
                for req in required:
                    missed = list()
                    for r in req:
                        if r not in data:
                            missed.append(r)
                    if len(missed) == 0:
                        flag = True
                    else:
                        missed_arr.append(missed)
                if flag:
                    return func(request, *args, **kwargs)
                return Er(f'Missing arguments : {print_or_arr(missed_arr)}', 405)
            elif request.method == 'POST':
                data = request.POST
                flag = False
                missed_arr = list()
                for req in required:
                    missed = list()
                    for r in req:
                        if r not in data:
                            missed.append(r)
                    if len(missed) == 0:
                        flag = True
                    else:
                        missed_arr.append(missed)
                if flag:
                    return func(request, *args, **kwargs)
                return Er(f'Missing arguments : {print_or_arr(missed_arr)}', 405)
            else:
                return Er('Invalid HTTP method', 405)
        return wrapper
    return decorator

def method_checker(method):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method == method:
                return func(request, *args, **kwargs)
            return Er('Invalid HTTP method', 405)
        return wrapper
    return decorator