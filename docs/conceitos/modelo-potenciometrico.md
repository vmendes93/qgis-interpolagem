# Modelo Potenciométrico

## Fundamentos Teóricos

O modelo potenciométrico é uma ferramenta para análise de fluxo a partir de superfícies interpoladas, especialmente útil em estudos hidrogeológicos. Ele permite calcular a direção e magnitude do fluxo com base no gradiente da superfície potenciométrica.

## Conceitos Fundamentais

### Superfície Potenciométrica

Uma superfície potenciométrica representa o nível de energia potencial em cada ponto de um campo escalar. Em hidrogeologia, esta superfície geralmente representa o nível da água subterrânea (nível freático ou nível piezométrico).

### Gradiente

O gradiente de uma superfície escalar é um vetor que aponta na direção de maior aumento da função, com magnitude proporcional à taxa de variação. Matematicamente, para uma superfície z(x,y), o gradiente é:

![Fórmula do Gradiente](https://latex.codecogs.com/png.latex?%5Cnabla%20z%20%3D%20%5Cleft%28%20%5Cfrac%7B%5Cpartial%20z%7D%7B%5Cpartial%20x%7D%2C%20%5Cfrac%7B%5Cpartial%20z%7D%7B%5Cpartial%20y%7D%20%5Cright%29 )

### Vetores de Fluxo

Em sistemas naturais, o fluxo ocorre na direção do gradiente negativo, ou seja, de regiões de maior potencial para regiões de menor potencial. Os vetores de fluxo são calculados como:

![Fórmula dos Vetores de Fluxo](https://latex.codecogs.com/png.latex?%5Cvec%7BF%7D%20%3D%20-%5Cnabla%20z%20%3D%20%5Cleft%28%20-%5Cfrac%7B%5Cpartial%20z%7D%7B%5Cpartial%20x%7D%2C%20-%5Cfrac%7B%5Cpartial%20z%7D%7B%5Cpartial%20y%7D%20%5Cright%29 )


## Aplicações

O modelo potenciométrico tem diversas aplicações:

### Hidrogeologia

- Determinação da direção do fluxo de água subterrânea
- Identificação de zonas de recarga e descarga
- Análise de captura de poços de bombeamento
- Delineação de áreas de proteção de mananciais

### Outras Áreas

- Análise de fluxo de calor em estudos geotérmicos
- Modelagem de dispersão de contaminantes
- Estudos de drenagem superficial
- Análise de campos gravitacionais ou magnéticos

## Propriedades Importantes

### Ortogonalidade

Os vetores de fluxo são sempre perpendiculares às linhas equipotenciais (linhas de igual valor na superfície potenciométrica).

### Conservação

Em um meio homogêneo e isotrópico, o fluxo segue o princípio de conservação, onde a divergência do campo de fluxo é zero em regiões sem fontes ou sumidouros.

### Magnitude

A magnitude do fluxo é proporcional ao gradiente da superfície, indicando a "força" do fluxo em cada ponto.

## Implementação no Kit de Interpolação

Nossa implementação do modelo potenciométrico oferece:

- Cálculo preciso do gradiente usando diferenças finitas centrais
- Cálculo dos vetores de fluxo (gradiente negativo)
- Visualização dos vetores de fluxo com opções de personalização
- Validação robusta dos dados de entrada
