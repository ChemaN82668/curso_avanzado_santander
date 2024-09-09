"""
Clases abstractas en Python.
"""

import abc

class Figura(abc.ABC):

    def __init__(self, etiqueta="", color=0):
        self.color = color
        self.etiqueta = etiqueta

    def __str__(self):
        return self.etiqueta + " " + str(self.color)
    
    @abc.abstractmethod
    def area(self):
        pass

if __name__ == '__main__':
    try:
        fig = Figura("F1")
    except Exception as e:
        print(e)

    