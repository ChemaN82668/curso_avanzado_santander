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
    def createDetalle(self, L, etiqueta=None):
        pass

    @abc.abstractmethod
    def crearFichero(self, texto, path):
        pass


class BuilderXML(Builder):

    def __init__(self):
        self.cabs = None
        self.etiqueta = ""

    def createCab(self, L):
        self.cabs = L
        return ""

    def createDetalle(self, L, etiqueta=None):
        linea = ""
        self.etiqueta = etiqueta
        for pos, i in enumerate(L):
            linea += f"<{self.cabs[pos]}>" + str(i).strip() + f"</{self.cabs[pos]}>"

        return f"<{etiqueta}>" + linea + f"</{etiqueta}>"

    def crearFichero(self, texto, path):
        pathFinal = path + ".xml"
        xml = f"<{self.etiqueta+'s'}>" + texto + f"</{self.etiqueta+'s'}>"
        xml = "<?xml version='1.0' encoding='UTF-8'?>" + xml
        fout = None
        try:
            fout = open(pathFinal, "w")
            fout.write(xml)
            print(f"se ha generado el fichero: {pathFinal}")

        except Exception as e:
            raise e

        finally:
            if fout:
                fout.close()


class BuilderHTML(Builder):

    def createCab(self, L):
        """
        El formato: <tr><th>col1</th><th> ... </th></tr>
        """
        cabeceras = "".join(["<th>" + col + "</th>" for col in L])
        return "<tr>" + cabeceras + "</tr>"

    def createDetalle(self, L, etiqueta=None):
        """
        El formato: <tr><td>col1</td><td> ... </td></tr>
        """
        detalle = "".join(["<td>" + col + "</td>" for col in L])
        return "<tr>" + detalle + "</tr>"

    def crearFichero(self, texto, path):
        pathFinal = path + ".html"
        print(pathFinal)


class Director:

    def __init__(self, builder):
        self.builder = builder
        self.nombre = ""
        self.directorios = ""

    def __analizarPath(self, path):
        if "/" not in path:
            self.nombre = path.partition(".")[0].lower()
            self.directorios = "."
        else:
            L = path.split("/")
            fichero = L[-1]
            self.directorios = L[:-1]
            self.nombre = fichero.partition(".")[0]

    def __getPathDestino(self):
        return "/".join(self.directorios) + "/" + self.nombre

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
                    tabla += self.builder.createDetalle(L, self.nombre[:-1])

            self.builder.crearFichero(tabla, self.__getPathDestino())

        except Exception as e:
            print(e)

        finally:
            if f:
                f.close()


if __name__ == "__main__":

    builder = BuilderXML()
    director = Director(builder)
    director.convertirFichero("patron_builder/Pedidos.txt")
