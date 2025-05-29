#!/usr/bin/env python3
"""
Script para atualizar docstrings nos arquivos do projeto.
"""

import os
import re
import sys

# Dicionário com as novas docstrings para cada arquivo e classe/método
DOCSTRINGS = {
    "interpoladores/idw.py": {
        "module": '''"""
Módulo de interpolação IDW (Inverse Distance Weighting).

Este módulo implementa o método de interpolação IDW, que estima valores em pontos
desconhecidos usando uma média ponderada dos valores de pontos conhecidos, onde
o peso diminui com a distância.

Características principais:
- Configuração flexível do expoente de distância
- Controle do número de vizinhos considerados
- Definição de distância máxima de influência
- Tratamento de casos extremos com valores padrão

Classes:
    - IDW: Classe responsável pela interpolação IDW.

Dependências:
    - numpy: Para operações numéricas eficientes
    - scipy.spatial.cKDTree: Para busca eficiente de vizinhos próximos
"""''',

        "IDW": '''"""
    Interpolador baseado no método de Inverso da Distância (IDW).

    O IDW estima valores em pontos desconhecidos calculando uma média ponderada
    dos valores em pontos conhecidos, onde o peso é inversamente proporcional à
    distância elevada a uma potência. Pontos mais próximos têm maior influência
    que pontos mais distantes.

    Permite configurar:
    - Expoente da distância (`power`): Controla a taxa de diminuição da influência com a distância
    - Número de vizinhos (`n_neighbors`): Limita quantos pontos próximos são considerados
    - Distância máxima de influência (`max_distance`): Define um raio máximo de busca
    - Valor padrão (`default_value`): Valor a usar quando não há vizinhos válidos

    Args:
        config (IDWConfig): Configuração do IDW. Default usa parâmetros padrões.
        verbose (bool, optional): Se True, exibe logs detalhados. Default é False.
        arquivo_log (str, optional): Caminho para arquivo de log. Se None, não salva logs.
            Default é None.

    Example:
        >>> from interpoladores.idw import IDW
        >>> from interpoladores.config import IDWConfig
        >>> import numpy as np
        >>>
        >>> # Pontos conhecidos
        >>> pontos = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        >>> valores = np.array([10, 20, 30, 40])
        >>>
        >>> # Grade para interpolação
        >>> x = np.linspace(0, 1, 10)
        >>> y = np.linspace(0, 1, 10)
        >>> grid_x, grid_y = np.meshgrid(x, y)
        >>>
        >>> # Configuração personalizada
        >>> config = IDWConfig(power=2.0, n_neighbors=3)
        >>>
        >>> # Interpolação
        >>> idw = IDW(config)
        >>> z = idw.interpolar(pontos, valores, grid_x, grid_y)
    """''',

        "interpolar": '''"""
        Realiza interpolação IDW sobre uma grade regular.

        O algoritmo:
        1. Valida as dimensões dos dados de entrada
        2. Constrói uma árvore KD para busca eficiente de vizinhos
        3. Para cada ponto da grade, encontra os vizinhos mais próximos
        4. Aplica a distância máxima se configurada
        5. Calcula os pesos baseados no inverso da distância elevada à potência
        6. Calcula a média ponderada dos valores dos vizinhos

        Args:
            pontos (np.ndarray): Array de shape (N, 2) com coordenadas XY dos pontos amostrados.
            valores (np.ndarray): Array de shape (N,) com os valores correspondentes aos pontos.
            grid_x (np.ndarray): Meshgrid com coordenadas X da grade.
            grid_y (np.ndarray): Meshgrid com coordenadas Y da grade.

        Returns:
            np.ndarray: Array 2D (mesmo shape de grid_x) com os valores interpolados.
                Se não houver vizinhos válidos para alguns pontos e default_value
                não estiver configurado, esses pontos terão valor NaN.

        Raises:
            ValueError: Se o número de pontos não for compatível com os valores.
            ValueError: Se os pontos não tiverem formato (N, 2).
            ValueError: Se as grades X e Y tiverem formatos diferentes.
            ValueError: Se não houver pontos válidos para interpolação.
        """'''
    },

    "interpoladores/krigagem.py": {
        "module": '''"""
Módulo de interpolação por Krigagem Ordinária utilizando PyKrige.

Este módulo implementa o método de interpolação geoestatística conhecido como
Krigagem Ordinária, que estima valores em pontos desconhecidos considerando
a estrutura espacial de correlação dos dados através de variogramas.

Características principais:
- Suporte a diferentes modelos de variograma
- Configuração de anisotropia
- Cálculo de variância de estimativa
- Personalização avançada de parâmetros

Classes:
    - Krigagem: Interpolador por Krigagem Ordinária.

Dependências:
    - numpy: Para operações numéricas eficientes
    - pykrige: Implementação de algoritmos de Krigagem
"""''',

        "Krigagem": '''"""
    Interpolador via Krigagem Ordinária utilizando PyKrige.

    A Krigagem Ordinária é um método geoestatístico que interpola valores
    desconhecidos com base na correlação espacial entre pontos conhecidos,
    modelada através de variogramas. Este método fornece não apenas estimativas
    dos valores, mas também a variância associada a cada estimativa.

    Permite interpolação geoestatística configurando:
    - Modelo de variograma
    - Parâmetros de anisotropia
    - Configurações avançadas do variograma
    - Opção de retornar estatísticas de erro

    Args:
        x (list or np.ndarray): Coordenadas X dos pontos amostrados.
        y (list or np.ndarray): Coordenadas Y dos pontos amostrados.
        z (list or np.ndarray): Valores associados aos pontos.
        config (KrigagemConfig, optional): Configuração da Krigagem.
            Default usa parâmetros padrões.
        verbose (bool, optional): Se True, exibe logs detalhados. Default é False.
        arquivo_log (str, optional): Caminho para arquivo de log. Se None, não salva logs.
            Default é None.

    Example:
        >>> from interpoladores.krigagem import Krigagem
        >>> from interpoladores.config import KrigagemConfig
        >>> import numpy as np
        >>>
        >>> # Pontos conhecidos
        >>> x = [0, 5, 10, 8, 3, 5]
        >>> y = [0, 5, 10, 8, 3, 10]
        >>> z = [10, 15, 20, 18, 12, 16]
        >>>
        >>> # Grade para interpolação
        >>> gridx = np.linspace(0, 10, 20)
        >>> gridy = np.linspace(0, 10, 20)
        >>>
        >>> # Configuração personalizada
        >>> config = KrigagemConfig(
        ...     modelo_variograma='exponential',
        ...     anisotropy_angle=45.0,
        ...     enable_statistics=True
        ... )
        >>>
        >>> # Interpolação
        >>> krig = Krigagem(x, y, z, config=config)
        >>> z_interp, variancia = krig.interpolar(gridx, gridy)
    """''',

        "interpolar": '''"""
        Executa a Krigagem Ordinária sobre a grade fornecida.

        O algoritmo:
        1. Valida as dimensões dos dados de entrada
        2. Configura os parâmetros do variograma
        3. Executa a Krigagem Ordinária usando PyKrige
        4. Retorna os valores interpolados e, opcionalmente, a variância

        Args:
            gridx (np.ndarray): Meshgrid das coordenadas X da grade.
            gridy (np.ndarray): Meshgrid das coordenadas Y da grade.

        Returns:
            Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
                Se enable_statistics=False (padrão): Grade 2D com os valores interpolados.
                Se enable_statistics=True: Tupla com (grade interpolada, variância de estimativa).

        Raises:
            ValueError: Se as grades X e Y tiverem formatos diferentes.
            ValueError: Se houver problema na execução da Krigagem (e.g. pontos insuficientes).
        """'''
    },

    "interpoladores/modelo_potenciometrico.py": {
        "module": '''"""
Módulo para cálculo de vetores de fluxo (modelo potenciométrico)
a partir de uma superfície interpolada.

Este módulo implementa funcionalidades para análise de fluxo em superfícies
potenciométricas, como aquelas encontradas em estudos hidrogeológicos.
Permite calcular gradientes, vetores de fluxo e visualizar os resultados.

Características principais:
- Cálculo de gradiente da superfície
- Cálculo de vetores de fluxo (gradiente negativo)
- Visualização de vetores de fluxo com opções de personalização
- Validação de dados de entrada

Classes:
    - ModeloPotenciometrico: Modelo que calcula os vetores de fluxo.

Funções:
    - plotar_vetores_fluxo: Plota os vetores de fluxo sobre a grade.

Dependências:
    - numpy: Para operações numéricas eficientes
    - matplotlib: Para visualização dos vetores de fluxo
"""''',

        "ModeloPotenciometrico": '''"""
    Classe para cálculo de vetores de fluxo (modelo potenciométrico)
    a partir de uma superfície interpolada.

    Em hidrogeologia e outras áreas, o fluxo ocorre na direção do gradiente
    negativo da superfície potenciométrica. Esta classe calcula esse gradiente
    e os vetores de fluxo resultantes para análise e visualização.

    A direção dos vetores de fluxo é baseada no gradiente da superfície,
    apontando de valores altos para valores baixos (gradiente negativo).

    Args:
        grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
        grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).
        z (np.ndarray): Superfície interpolada.
        verbose (bool, optional): Se True, exibe logs detalhados. Default é False.
        arquivo_log (str, optional): Caminho para arquivo de log. Se None, não salva logs.
            Default é None.

    Methods:
        calcular_fluxo: Calcula os vetores de fluxo (gradiente negativo da superfície).
        calcular_gradiente: Calcula o gradiente da superfície.

    Example:
        >>> import numpy as np
        >>> from interpoladores.modelo_potenciometrico import ModeloPotenciometrico, plotar_vetores_fluxo
        >>>
        >>> # Criar uma grade
        >>> x = np.linspace(0, 10, 20)
        >>> y = np.linspace(0, 10, 20)
        >>> grid_x, grid_y = np.meshgrid(x, y)
        >>>
        >>> # Criar uma superfície com um ponto alto no centro
        >>> centro_x, centro_y = 5, 5
        >>> z = 10 - 0.5 * ((grid_x - centro_x)**2 + (grid_y - centro_y)**2)
        >>>
        >>> # Calcular vetores de fluxo
        >>> modelo = ModeloPotenciometrico(grid_x, grid_y, z)
        >>> flow_x, flow_y = modelo.calcular_fluxo()
        >>>
        >>> # Visualizar os vetores
        >>> plotar_vetores_fluxo(grid_x, grid_y, flow_x, flow_y, densidade=2)
    """''',

        "calcular_gradiente": '''"""
        Calcula o gradiente da superfície z.

        O gradiente é um vetor que aponta na direção de maior aumento da função,
        com magnitude proporcional à taxa de variação. É calculado usando
        diferenças finitas centrais.

        Returns:
            Tuple[np.ndarray, np.ndarray]:
                - grad_x (np.ndarray): Componente X do gradiente.
                - grad_y (np.ndarray): Componente Y do gradiente.
        """''',

        "calcular_fluxo": '''"""
        Calcula os vetores de fluxo (gradiente invertido) da superfície z.

        Os vetores de fluxo apontam na direção de maior diminuição da superfície
        (gradiente negativo), representando a direção natural do fluxo de um
        fluido sob a influência do campo potencial.

        Returns:
            Tuple[np.ndarray, np.ndarray]:
                - flow_x (np.ndarray): Componente X dos vetores de fluxo.
                - flow_y (np.ndarray): Componente Y dos vetores de fluxo.
        """'''
    },

    "interpoladores/config.py": {
        "module": '''"""
Configurações para os algoritmos de interpolação.

Este módulo contém classes de configuração para os diferentes
algoritmos de interpolação implementados, permitindo personalização
flexível dos parâmetros sem complicar as interfaces das classes principais.

Classes:
    - IDWConfig: Configuração para interpolação IDW
    - KrigagemConfig: Configuração para interpolação por Krigagem
"""''',

        "IDWConfig": '''"""
    Configuração para o algoritmo IDW (Inverse Distance Weighting).

    Esta classe encapsula todos os parâmetros configuráveis do algoritmo IDW,
    permitindo personalização flexível sem complicar a interface da classe IDW.

    Attributes:
        power (float): Expoente da distância. Valores maiores aumentam a
                      influência de pontos próximos e diminuem a de pontos distantes.
                      Valores típicos estão entre 1 e 3. Default é 2.0.
        n_neighbors (int, optional): Número de vizinhos a considerar na interpolação.
                                    Se None, usa todos os pontos disponíveis. Default é None.
        max_distance (float, optional): Distância máxima para considerar pontos na interpolação.
                                       Pontos além desta distância são ignorados.
                                       Se None, não há limite. Default é None.
        default_value (float, optional): Valor padrão para células sem vizinhos válidos.
                                        Se None, usa NaN. Default é None.
    """''',

        "KrigagemConfig": '''"""
    Configuração para o algoritmo de Krigagem Ordinária.

    Esta classe encapsula todos os parâmetros configuráveis do algoritmo de Krigagem,
    permitindo personalização avançada sem complicar a interface da classe Krigagem.

    Attributes:
        modelo_variograma (str): Modelo de variograma a ser usado.
            Opções: 'linear', 'power', 'gaussian', 'spherical', 'exponential'.
            Cada modelo representa uma forma diferente de correlação espacial.
            Default é 'spherical'.
        nlags (int, optional): Número de lags para cálculo do variograma experimental.
            Controla a resolução do variograma. Se None, usa o valor padrão do PyKrige.
            Default é None.
        variogram_model_parameters (dict, optional): Parâmetros específicos do modelo de variograma.
            Permite ajuste fino do comportamento do variograma.
            Se None, PyKrige estima automaticamente. Default é None.
        anisotropy_angle (float, optional): Ângulo de anisotropia em graus (0-180).
            Usado quando a correlação espacial varia com a direção.
            Se 0, assume isotropia. Default é 0.
        anisotropy_ratio (float, optional): Razão de anisotropia.
            Representa a proporção entre os eixos maior e menor da elipse de anisotropia.
            Deve ser >= 1.0. Default é 1.0 (isotropia).
        verbose (bool, optional): Se True, exibe informações durante o processamento.
            Útil para depuração. Default é False.
        enable_statistics (bool, optional): Se True, calcula e retorna estatísticas de erro.
            Permite avaliar a incerteza da interpolação. Default é False.
    """'''
    },

    "utils/logging_utils.py": {
        "module": '''"""
Utilitários de logging para monitoramento de progresso dos algoritmos.

Este módulo fornece funções e classes para facilitar o logging
consistente em todos os algoritmos de interpolação, permitindo
monitorar o progresso, registrar erros e medir o tempo de execução.

Classes:
    - InterpoladorLogger: Classe para logging de operações de interpolação.

Funções:
    - configurar_logger: Configura um logger com handlers para console e/ou arquivo.
"""''',

        "configurar_logger": '''"""
    Configura um logger com handlers para console e/ou arquivo.

    Esta função simplifica a criação e configuração de loggers,
    permitindo direcionar a saída para console, arquivo ou ambos,
    com formatação consistente.

    Args:
        nome (str): Nome do logger.
        nivel (int, optional): Nível de logging. Default é logging.INFO.
        formato (str, optional): Formato das mensagens de log.
        arquivo_log (str, optional): Caminho para o arquivo de log.
            Se None, não salva logs em arquivo. Default é None.
        console (bool, optional): Se True, exibe logs no console.
            Default é True.

    Returns:
        logging.Logger: Logger configurado.
    """''',

        "InterpoladorLogger": '''"""
    Classe para logging de operações de interpolação.

    Fornece métodos para registrar eventos comuns em algoritmos de interpolação,
    como início, progresso e conclusão, além de medir o tempo de execução.

    Args:
        nome (str): Nome do algoritmo ou módulo.
        nivel (int, optional): Nível de logging. Default é logging.INFO.
        arquivo_log (str, optional): Caminho para o arquivo de log.
            Se None, não salva logs em arquivo. Default é None.
        console (bool, optional): Se True, exibe logs no console.
            Default é True.
    """'''
    }
}

def update_docstrings(file_path, docstrings_dict):
    """
    Atualiza as docstrings em um arquivo Python.

    Args:
        file_path (str): Caminho para o arquivo Python
        docstrings_dict (dict): Dicionário com as novas docstrings
    """
    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Atualiza a docstring do módulo
    if 'module' in docstrings_dict:
        module_pattern = r'""".*?"""'
        module_match = re.search(module_pattern, content, re.DOTALL)
        if module_match:
            content = content.replace(module_match.group(0), docstrings_dict['module'], 1)

    # Atualiza as docstrings de classes e métodos
    for item_name, new_docstring in docstrings_dict.items():
        if item_name == 'module':
            continue

        # Padrão para encontrar a classe ou método e sua docstring
        pattern = rf'(class|def)\s+{item_name}.*?:\s*""".*?"""'
        match = re.search(pattern, content, re.DOTALL)

        if match:
            # Extrai a declaração da classe/método e a docstring atual
            declaration_and_docstring = match.group(0)

            # Separa a declaração da docstring
            declaration_pattern = rf'(class|def)\s+{item_name}.*?:\s*'
            declaration_match = re.search(declaration_pattern, declaration_and_docstring)

            if declaration_match:
                declaration = declaration_match.group(0)

                # Substitui a docstring mantendo a declaração
                old_docstring_pattern = r'""".*?"""'
                old_docstring_match = re.search(old_docstring_pattern, declaration_and_docstring, re.DOTALL)

                if old_docstring_match:
                    # Preserva a indentação da docstring original
                    indent_match = re.search(r'^(\s*)', declaration_and_docstring, re.MULTILINE)
                    indent = indent_match.group(1) if indent_match else ''

                    # Indenta a nova docstring
                    indented_docstring = new_docstring
                    if indent:
                        lines = new_docstring.split('\n')
                        # Primeira linha já tem indentação correta da declaração
                        indented_lines = [lines[0]]
                        # Adiciona indentação às linhas restantes
                        for line in lines[1:]:
                            indented_lines.append(indent + line if line.strip() else line)
                        indented_docstring = '\n'.join(indented_lines)

                    # Substitui a docstring antiga pela nova
                    new_declaration_and_docstring = declaration_and_docstring.replace(
                        old_docstring_match.group(0), indented_docstring
                    )
                    content = content.replace(declaration_and_docstring, new_declaration_and_docstring)

    # Salva o arquivo atualizado
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    """
    Função principal que atualiza as docstrings em todos os arquivos.
    """
    base_dir = os.getcwd()  # Diretório atual

    for file_path, docstrings in DOCSTRINGS.items():
        full_path = os.path.join(base_dir, file_path)
        print(f"Atualizando docstrings em {file_path}...")
        if update_docstrings(full_path, docstrings):
            print(f"✓ Docstrings atualizadas com sucesso em {file_path}")
        else:
            print(f"✗ Falha ao atualizar docstrings em {file_path}")

if __name__ == "__main__":
    main()
