import numpy as np # noqa: F401
import pytest

from interpoladores.config import IDWConfig
from interpoladores.idw import IDW


def gerar_grid(nx=10, ny=10, xmin=0, xmax=50, ymin=0, ymax=50):
    """Gera uma grade regular para testes."""
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    return np.meshgrid(x, y)


def gerar_amostras(n_pontos=4):
    """Gera pontos de amostra para testes."""
    if n_pontos == 4:
        pontos = np.array([[10, 10], [20, 15], [30, 35], [40, 40]])
        valores = np.array([1.0, 2.0, 3.0, 3.0])
    else:
        # Gera pontos aleatórios
        np.random.seed(42)  # Para reprodutibilidade
        pontos = np.random.rand(n_pontos, 2) * 50
        # Função simples para gerar valores: z = x/10 + y/20
        valores = pontos[:, 0] / 10 + pontos[:, 1] / 20

    return pontos, valores


def test_idw_padrao():
    """Testa o IDW com configuração padrão."""
    pontos, valores = gerar_amostras()
    grid_x, grid_y = gerar_grid()

    idw = IDW()
    z = idw.interpolar(pontos, valores, grid_x, grid_y)

    assert z.shape == grid_x.shape
    assert not np.any(np.isnan(z))


def test_idw_com_n_neighbors():
    """Testa o IDW com número limitado de vizinhos."""
    pontos, valores = gerar_amostras()
    grid_x, grid_y = gerar_grid()

    config = IDWConfig(n_neighbors=2)
    idw = IDW(config)
    z = idw.interpolar(pontos, valores, grid_x, grid_y)

    assert z.shape == grid_x.shape
    assert not np.any(np.isnan(z))


def test_idw_com_max_distance():
    """Testa o IDW com distância máxima configurada."""
    pontos, valores = gerar_amostras()
    grid_x, grid_y = gerar_grid()

    config = IDWConfig(max_distance=10.0)
    idw = IDW(config)
    z = idw.interpolar(pontos, valores, grid_x, grid_y)

    # Verifica se o shape está correto
    assert z.shape == grid_x.shape

    # Verifica que existem NaNs (porque com max_distance alguns pontos podem não ter vizinhos)
    assert np.isnan(z).any()

    # Verifica que os valores não NaN são válidos (ou seja, interpolação ocorreu onde possível)
    assert np.isfinite(z[~np.isnan(z)]).all()


def test_idw_com_default_value():
    """Testa o IDW com valor padrão para pontos sem vizinhos."""
    pontos, valores = gerar_amostras()
    grid_x, grid_y = gerar_grid()

    default_value = -999.0
    config = IDWConfig(max_distance=10.0, default_value=default_value)
    idw = IDW(config)
    z = idw.interpolar(pontos, valores, grid_x, grid_y)

    # Verifica se o shape está correto
    assert z.shape == grid_x.shape

    # Verifica que não existem NaNs (porque usamos default_value)
    assert not np.isnan(z).any()

    # Verifica que os pontos sem vizinhos têm o valor padrão
    mask = np.abs(z - default_value) < 1e-10
    assert mask.any()  # Deve haver pelo menos um ponto com valor padrão


def test_idw_com_power_diferente():
    """Testa o IDW com diferentes valores de power."""
    pontos, valores = gerar_amostras()
    grid_x, grid_y = gerar_grid()

    config1 = IDWConfig(power=1.0)
    config2 = IDWConfig(power=4.0)

    idw1 = IDW(config1)
    idw2 = IDW(config2)

    z1 = idw1.interpolar(pontos, valores, grid_x, grid_y)
    z2 = idw2.interpolar(pontos, valores, grid_x, grid_y)

    assert not np.allclose(z1, z2)


def test_idw_validacao_entrada():
    """Testa a validação de entrada do IDW."""
    pontos = np.array([[10, 10], [20, 15], [30, 35]])
    valores = np.array([1.0, 2.0])  # Número incorreto de valores
    grid_x, grid_y = gerar_grid()

    idw = IDW()

    # Testa erro quando número de pontos não corresponde ao número de valores
    with pytest.raises(ValueError) as excinfo:
        idw.interpolar(pontos, valores, grid_x, grid_y)
    assert "não corresponde ao número de valores" in str(excinfo.value)

    # Testa erro quando pontos não têm formato (N, 2)
    pontos_invalidos = np.array([[10, 10, 5], [20, 15, 10]])  # Formato (N, 3)
    valores_validos = np.array([1.0, 2.0])

    with pytest.raises(ValueError) as excinfo:
        idw.interpolar(pontos_invalidos, valores_validos, grid_x, grid_y)
    assert "Pontos devem ter formato (N, 2)" in str(excinfo.value)

    # Testa erro quando grades X e Y têm formatos diferentes
    grid_y_invalido = np.zeros((5, 15))  # Formato diferente de grid_x

    with pytest.raises(ValueError) as excinfo:
        idw.interpolar(pontos, np.array([1.0, 2.0, 3.0]), grid_x, grid_y_invalido)
    assert "Grades X e Y devem ter o mesmo formato" in str(excinfo.value)


def test_idw_sem_vizinhos_validos():
    """Testa o comportamento do IDW quando não há vizinhos válidos."""
    pontos = np.array([[10, 10], [20, 15]])
    valores = np.array([1.0, 2.0])
    grid_x, grid_y = gerar_grid(xmin=100, xmax=150)  # Grade longe dos pontos

    config = IDWConfig(max_distance=5.0)  # Distância máxima pequena
    idw = IDW(config)

    # Deve lançar ValueError porque nenhum ponto da grade tem vizinhos válidos
    with pytest.raises(ValueError) as excinfo:
        idw.interpolar(pontos, valores, grid_x, grid_y)
    assert "Nenhum ponto tem vizinhos dentro da distância máxima" in str(excinfo.value)


def test_idw_grade_grande():
    """Testa o IDW com uma grade grande para verificar desempenho."""
    pontos, valores = gerar_amostras(n_pontos=20)
    grid_x, grid_y = gerar_grid(nx=50, ny=50)  # Grade 50x50

    idw = IDW()
    z = idw.interpolar(pontos, valores, grid_x, grid_y)

    assert z.shape == grid_x.shape
    assert not np.any(np.isnan(z))


def test_idw_reproducibilidade():
    """Testa se o IDW produz resultados consistentes para as mesmas entradas."""
    pontos, valores = gerar_amostras()
    grid_x, grid_y = gerar_grid()

    idw = IDW()
    z1 = idw.interpolar(pontos, valores, grid_x, grid_y)
    z2 = idw.interpolar(pontos, valores, grid_x, grid_y)

    np.testing.assert_allclose(z1, z2)
