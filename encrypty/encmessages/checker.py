from .responses import Er

def print_arr(arr):
    string = str()
    for el in arr:
        string = string + ' ' + el
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
                return Er(f'Missing arguments :{print_arr(missed)}', 405)
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
                missed = list()
                for r in required:
                    if r not in data:
                        missed.append(r)
                if len(missed) == 0:
                    return func(request, *args, **kwargs)
                return Er(f'Missing arguments :{print_arr(missed)}', 405)
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