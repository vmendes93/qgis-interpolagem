# Interpolação por Inverso da Distância Ponderada (IDW)

## Fundamentos Teóricos

A interpolação IDW (Inverse Distance Weighting) é um método determinístico que estima valores em pontos desconhecidos usando uma média ponderada dos valores de pontos conhecidos, onde o peso diminui com a distância.

## Fórmula Matemática

O valor interpolado em um ponto desconhecido é calculado como:

![Fórmula IDW Principal](https://latex.codecogs.com/png.latex?Z%28s_0%29%20%3D%20%5Cfrac%7B%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%20w_i%20Z%28s_i%29%7D%7B%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%20w_i%7D )

onde:
- Z(s_0) é o valor a ser estimado no ponto s_0
- Z(s_i) são os valores conhecidos nos pontos s_i
- w_i são os pesos, calculados como:

![Fórmula dos Pesos](https://latex.codecogs.com/png.latex?w_i%20%3D%20%5Cfrac%7B1%7D%7Bd%28s_0%2C%20s_i%29%5Ep%7D )

onde:
- d(s_0, s_i) é a distância entre o ponto a ser estimado s_0 e o ponto conhecido s_i
- p é o expoente de potência (geralmente 2)

## Parâmetros Importantes

### Expoente de Potência (power)

O expoente controla a taxa de diminuição da influência com a distância:
- Valores maiores (p > 3) dão mais peso a pontos próximos, criando "ilhas" ao redor dos pontos conhecidos
- Valores menores (p < 2) distribuem a influência mais uniformemente, criando superfícies mais suaves
- p = 2 é o valor mais comum, representando o inverso do quadrado da distância

### Número de Vizinhos (n_neighbors)

Limita quantos pontos próximos são considerados na interpolação:
- Usar poucos vizinhos acelera o cálculo mas pode perder padrões importantes
- Usar muitos vizinhos pode suavizar demais a superfície e aumentar o tempo de processamento
- O valor ideal depende da densidade e distribuição dos pontos conhecidos

### Distância Máxima (max_distance)

Define um raio máximo de busca para considerar pontos na interpolação:
- Útil para evitar que pontos muito distantes influenciem a estimativa
- Ajuda a preservar descontinuidades naturais nos dados
- Pode resultar em áreas sem valores (NaN) quando não há pontos dentro da distância máxima

## Vantagens e Limitações

### Vantagens
- Algoritmo simples e intuitivo
- Computacionalmente eficiente
- Funciona bem com distribuição regular de pontos
- Preserva os valores exatos nos pontos conhecidos

### Limitações
- Não considera a estrutura espacial dos dados
- Tende a criar "olhos de boi" (bull's eyes) ao redor dos pontos conhecidos
- Não fornece estimativa de erro
- Sensível a outliers e agrupamentos de pontos

## Implementação no Kit de Interpolação

Nossa implementação do IDW oferece:
- Configuração flexível de todos os parâmetros importantes
- Uso eficiente de KD-Trees para busca rápida de vizinhos
- Tratamento adequado de casos extremos
- Opção de valor padrão para células sem vizinhos válidos
