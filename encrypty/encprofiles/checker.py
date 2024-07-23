from .responses import Er
def single_way_check(func):
    def wrapper(request, requiered, *args, **kwargs):
        if request.method == 'GET':
            data = request.GET
            for r in requiered:
                if r not in data:
                    return Er(f'Missing arguments : {r}', 405)
            return func(request, *args, **kwargs)
        elif request.method == 'POST':
            data = request.POST
            for r in requiered:
                if r not in data:
                    return Er(f'Missing arguments : {r}', 405)
            return func(request, *args, **kwargs)
        else:
            return Er('Invalid HTTP method', 405)
    return wrapper