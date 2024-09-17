"""
Patrón builder:
Conversor de formato CSV a HTML o XML
"""

import abc


class Builder(abc.ABC):

    @abc.abstractmethod
    def createCab(self, L):
        pass

    @abc.abstractmethod
    def createDetalle(self, L):
        pass

    @abc.abstractmethod
    def crearFichero(self, texto, path):
        pass


class BuilderXML(Builder):

    def __init__(self):
        self.cabs = None

    def createCab(self, L):
        self.cabs = L
        return ""

    def createDetalle(self, L):
        linea = ""
        for pos, i in enumerate(L):
            linea += f"<{self.cabs[pos]}>"+ str(i) + f"</{self.cabs[pos]}>"        
        return linea

    def crearFichero(self, texto, path):
        pass


class BuilderHTML(Builder):

    def createCab(self, L):
        """
        El formato: <tr><th>col1</th><th> ... </th></tr>
        """
        cabeceras = "".join(["<th>"+col+"</th>" for col in L])
        return "<tr>"+ cabeceras +"</tr>"

    def createDetalle(self, L):
        """
        El formato: <tr><td>col1</td><td> ... </td></tr>
        """
        detalle = "".join(["<td>"+col+"</td>" for col in L])
        return "<tr>"+ detalle +"</tr>"

    def crearFichero(self, texto, path):
        pass


class Director:

    def __init__(self, builder):
        self.builder = builder
        self.nombre=""
        self.directorios=""

    def __analizarPath(self, path):
        if "/" not in path:
            self.nombre = path.partition(".")[0]
            self.directorios = "./"
        else:
            L = path.split("/")
            fichero = L[-1]
            self.directorios = L[:-1]
            self.nombre = fichero.partition(".")[0]


    def convertirFichero(self, path, sep=";"):
        f = None
        self.__analizarPath(path)
        cabs = True
        tabla = ""
        try:
            f = open(path)
            for linea in f:
                linea = linea.rstrip()
                L = linea.split(sep)
                if cabs:
                    tabla += self.builder.createCab(L)
                    cabs = False                    
                else:
                    tabla += self.builder.createDetalle(L)
            print(tabla)
                
        except Exception as e:
            print(e)

        finally:
            if f:
                f.close()


if __name__ == "__main__":

    builder = BuilderXML()
    director = Director(builder)
    director.convertirFichero("patron_builder/Empleados.txt")
