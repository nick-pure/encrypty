from django.http import JsonResponse

class Ok(JsonResponse):
    def __init__(self, description, status):
        super().__init__({'status' : 'ok', 'info' : {'description' : description}}, status=status)

class Er(JsonResponse):
    def __init__(self, error, status):
        super().__init__({'status' : 'error', 'info' : {'error' : error}}, status=status)

class Data(JsonResponse):
    def __init__(self, data, status):
        super().__init__({'status' : 'ok', 'data' : data}, status=status)