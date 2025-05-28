"""
Módulo base para interpoladores.

Define uma interface genérica que deve ser implementada por qualquer
classe de interpolação (ex.: IDW, Krigagem).

Classes:
    - InterpoladorBase: Classe abstrata para interpoladores.

"""

class InterpoladorBase:
    """
    Classe base abstrata para interpoladores espaciais.

    Qualquer interpolador que herde desta classe deve implementar o método `interpolar`.

    Methods:
        interpolar(*args, **kwargs): Método que executa a interpolação.
    """

    def interpolar(self, *args, **kwargs):
        """
        Método abstrato para realizar interpolação.

        Este método deve ser sobrescrito nas subclasses.

        Raises:
            NotImplementedError: Se a subclasse não implementar este método.
        """
        raise NotImplementedError("Implemente esse método na subclasse.")

