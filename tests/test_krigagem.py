import numpy as np  # noqa: F401
import pytest

from interpoladores.config import KrigagemConfig
from interpoladores.krigagem import Krigagem


def gerar_grid(nx=5, ny=5, xmin=0, xmax=20, ymin=0, ymax=20):
    """Gera uma grade regular para testes."""
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    return x, y


def gerar_amostras(n_pontos=None):
    """Gera pontos de amostra para testes."""
    if n_pontos is None:
        # Pontos padrão
        x = [0, 10, 20]
        y = [0, 10, 20]
        z = [1.0, 2.0, 3.0]
    else:
        # Gera pontos aleatórios
        np.random.seed(42)  # Para reprodutibilidade
        x = np.random.rand(n_pontos) * 20
        y = np.random.rand(n_pontos) * 20
        # Função simples para gerar valores: z = x/10 + y/20
        z = x / 10 + y / 20

    return x, y, z


def test_krigagem_simples():
    """Testa a Krigagem com configuração padrão."""
    # Pontos amostrados
    x, y, z = gerar_amostras()
    # Grade de teste
    gridx, gridy = gerar_grid()

    # Usar KrigagemConfig em vez de passar modelo_variograma diretamente
    config = KrigagemConfig(modelo_variograma="linear")
    krig = Krigagem(x, y, z, config=config)
    zi = krig.interpolar(gridx, gridy)

    assert zi.shape == (5, 5)
    assert not np.any(np.isnan(zi))


@pytest.mark.parametrize("modelo", ["linear", "exponential", "gaussian", "spherical"])
def test_krigagem_varios_modelos(modelo):
    """Testa a Krigagem com diferentes modelos de variograma."""
    x, y, z = gerar_amostras()
    gridx, gridy = gerar_grid()

    # Usar KrigagemConfig em vez de passar modelo_variograma diretamente
    config = KrigagemConfig(modelo_variograma=modelo)
    krig = Krigagem(x, y, z, config=config)
    zi = krig.interpolar(gridx, gridy)

    assert zi.shape == (5, 5)
    assert not np.any(np.isnan(zi))


def test_krigagem_grade_densa():
    """Testa a Krigagem com uma grade mais densa."""
    x, y, z = gerar_amostras()
    gridx, gridy = gerar_grid(nx=10, ny=10)

    krig = Krigagem(x, y, z)
    zi = krig.interpolar(gridx, gridy)

    assert zi.shape == (10, 10)
    assert not np.any(np.isnan(zi))


def test_krigagem_pontos_colineares():
    """Testa a Krigagem com pontos colineares."""
    x = [0, 5, 10]
    y = [0, 0, 0]  # linha reta
    z = [1.0, 2.0, 1.5]
    gridx, gridy = gerar_grid(xmin=-5, xmax=15, ymin=-5, ymax=5)

    krig = Krigagem(x, y, z)
    zi = krig.interpolar(gridx, gridy)

    assert zi.shape == (5, 5)
    assert not np.any(np.isnan(zi))


def test_krigagem_com_config():
    """Testa a Krigagem usando a classe KrigagemConfig."""
    x, y, z = gerar_amostras()
    gridx, gridy = gerar_grid()

    config = KrigagemConfig(
        modelo_variograma="exponential", anisotropy_angle=45.0, anisotropy_ratio=2.0
    )

    krig = Krigagem(x, y, z, config=config)
    zi = krig.interpolar(gridx, gridy)

    assert zi.shape == (5, 5)
    assert not np.any(np.isnan(zi))


def test_krigagem_com_estatisticas():
    """Testa a Krigagem com retorno de estatísticas."""
    x, y, z = gerar_amostras()
    gridx, gridy = gerar_grid()

    config = KrigagemConfig(enable_statistics=True)
    krig = Krigagem(x, y, z, config=config)

    resultado = krig.interpolar(gridx, gridy)

    # Verifica se o resultado é uma tupla com dois elementos
    assert isinstance(resultado, tuple)
    assert len(resultado) == 2

    zi, ss = resultado

    # Verifica as dimensões
    assert zi.shape == (5, 5)
    assert ss.shape == (5, 5)

    # Verifica que a variância é não-negativa (com tolerância para erros numéricos)
    assert np.all(
        ss >= -1e-10
    )  # Tolerância para pequenos valores negativos devido a erros numéricos


def test_krigagem_validacao_entrada():
    """Testa a validação de entrada da Krigagem."""
    # Teste com dimensões incompatíveis
    x = [0, 10, 20]
    y = [0, 10]  # Um valor a menos
    z = [1.0, 2.0, 3.0]

    with pytest.raises(ValueError) as excinfo:
        Krigagem(x, y, z)
    assert "Dimensões incompatíveis" in str(excinfo.value)

    # Teste com poucos pontos
    x = [0, 10]
    y = [0, 10]
    z = [1.0, 2.0]

    with pytest.raises(ValueError) as excinfo:
        Krigagem(x, y, z)
    assert "Krigagem requer pelo menos 3 pontos" in str(excinfo.value)

    # Teste com grades de dimensões diferentes
    x, y, z = gerar_amostras()
    gridx, _ = gerar_grid(nx=5, ny=5)
    _, gridy = gerar_grid(nx=6, ny=6)  # Dimensão diferente

    krig = Krigagem(x, y, z)

    with pytest.raises(ValueError) as excinfo:
        krig.interpolar(gridx, gridy)
    assert "Grades X e Y devem ter o mesmo formato" in str(excinfo.value)


def test_krigagem_muitos_pontos():
    """Testa a Krigagem com muitos pontos para verificar desempenho."""
    x, y, z = gerar_amostras(n_pontos=20)
    gridx, gridy = gerar_grid()

    krig = Krigagem(x, y, z)
    zi = krig.interpolar(gridx, gridy)

    assert zi.shape == (5, 5)
    assert not np.any(np.isnan(zi))


def test_krigagem_reproducibilidade():
    """Testa se a Krigagem produz resultados consistentes para as mesmas entradas."""
    x, y, z = gerar_amostras()
    gridx, gridy = gerar_grid()

    # Usar KrigagemConfig em vez de passar modelo_variograma diretamente
    config = KrigagemConfig(modelo_variograma="linear")
    krig1 = Krigagem(x, y, z, config=config)
    krig2 = Krigagem(x, y, z, config=config)

    zi1 = krig1.interpolar(gridx, gridy)
    zi2 = krig2.interpolar(gridx, gridy)

    np.testing.assert_allclose(zi1, zi2)
