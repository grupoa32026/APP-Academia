import decimal
import json

def calculariva(importe):
    return importe * 0.21

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)


