# Krigagem

## Fundamentos Teóricos

A Krigagem é um método geoestatístico de interpolação espacial que estima valores em locais não amostrados considerando a estrutura espacial de correlação dos dados. Diferentemente de métodos determinísticos como o IDW, a Krigagem fornece não apenas estimativas dos valores, mas também a variância associada, permitindo quantificar a incerteza.

## Conceitos Fundamentais

### Variograma

O variograma é a ferramenta central da geoestatística, que descreve como a variabilidade espacial muda com a distância e direção. Matematicamente, o semivariograma γ(h) é definido como:

![Fórmula do Semivariograma](https://latex.codecogs.com/png.latex?%5Cgamma%28h%29%20%3D%20%5Cfrac%7B1%7D%7B2N%28h%29%7D%20%5Csum_%7Bi%3D1%7D%5E%7BN%28h%29%7D%20%5BZ%28s_i%29%20-%20Z%28s_i%20%2B%20h%29%5D%5E2 )

onde:
- γ(h) é o semivariograma para a distância h
- N(h) é o número de pares de pontos separados pela distância h
- Z(s_i) é o valor no ponto s_i
- Z(s_i + h) é o valor no ponto s_i + h

### Modelos de Variograma

Após calcular o variograma experimental, ajusta-se um modelo teórico. Os modelos mais comuns são:

- **Esférico**: Atinge o patamar a uma distância finita (alcance)
- **Exponencial**: Aproxima-se assintoticamente do patamar
- **Gaussiano**: Aproxima-se suavemente do patamar, com comportamento parabólico na origem
- **Linear**: Aumenta linearmente com a distância

### Parâmetros do Variograma

- **Efeito Pepita (Nugget)**: Variabilidade em distância zero, representando erro de medição ou variabilidade em escala menor que a amostragem
- **Patamar (Sill)**: Valor máximo do variograma, representando a variância total dos dados
- **Alcance (Range)**: Distância além da qual não há mais correlação espacial

### Anisotropia

A anisotropia ocorre quando a correlação espacial varia com a direção. Pode ser:
- **Geométrica**: O alcance varia com a direção
- **Zonal**: O patamar varia com a direção

## Krigagem Ordinária

A Krigagem Ordinária é a forma mais comum de Krigagem, que estima valores como uma combinação linear ponderada dos valores conhecidos:

![Fórmula da Krigagem](https://latex.codecogs.com/png.latex?Z%5E*%28s_0%29%20%3D%20%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%20%5Clambda_i%20Z%28s_i%29 )


- Z*(s_0) é o valor estimado no ponto s_0

- Z(s_i) são os valores conhecidos nos pontos s_i

- λ_i são os pesos, determinados pela solução de um sistema de equações que minimiza a variância de estimação

Os pesos λ_i são calculados para que:

1. A estimativa seja não-enviesada: ![Soma dos pesos](https://latex.codecogs.com/png.latex?%5Csum_%7Bi%3D1%7D%5E%7Bn%7D%20%5Clambda_i%20%3D%201 )

2. A variância de estimação seja minimizada

## Vantagens e Limitações

### Vantagens
- Considera a estrutura espacial dos dados
- Fornece medida de incerteza (variância de estimação)
- Produz superfícies mais suaves e realistas
- É um estimador BLUE (Best Linear Unbiased Estimator)

### Limitações
- Mais complexo e computacionalmente intensivo
- Requer conhecimento geoestatístico para parametrização adequada
- Sensível à escolha do modelo de variograma
- Assume estacionaridade (média e variância constantes na área de estudo)

## Implementação no Kit de Interpolação

Nossa implementação da Krigagem oferece:
- Suporte a diferentes modelos de variograma
- Configuração de anisotropia
- Cálculo de variância de estimativa
- Personalização avançada de parâmetros
