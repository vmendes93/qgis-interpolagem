# Conceitos de Interpolação Espacial

Este documento explica os conceitos fundamentais por trás dos métodos de interpolação implementados neste projeto.

## Interpolação Espacial

A interpolação espacial é o processo de estimar valores desconhecidos em locais não amostrados com base em valores conhecidos em locais amostrados. É amplamente utilizada em geociências, hidrologia, meteorologia e outras áreas que lidam com dados espaciais.

## IDW (Inverse Distance Weighting)

O método IDW baseia-se no princípio de que pontos mais próximos têm maior influência no valor estimado do que pontos mais distantes.

### Fórmula

O valor interpolado em um ponto desconhecido é calculado como:

```
Z(s₀) = Σ[wᵢ × Z(sᵢ)] / Σwᵢ

onde:
wᵢ = 1 / d(s₀, sᵢ)ᵖ
```

- Z(s₀) é o valor estimado no ponto s₀
- Z(sᵢ) é o valor conhecido no ponto sᵢ
- wᵢ é o peso do ponto sᵢ
- d(s₀, sᵢ) é a distância entre s₀ e sᵢ
- p é o expoente de potência (geralmente 2)

### Características

- **Vantagens**: Simples, intuitivo, eficiente computacionalmente
- **Desvantagens**: Não estima incertezas, tende a criar "olhos de boi" ao redor dos pontos amostrais
- **Parâmetros importantes**: Expoente de potência, número de vizinhos, distância máxima

## Krigagem

A Krigagem é um método geoestatístico que utiliza a correlação espacial entre pontos para estimar valores desconhecidos, considerando não apenas a distância, mas também a configuração espacial dos pontos.

### Conceitos-chave

- **Variograma**: Descreve a correlação espacial entre pontos em função da distância
- **Modelos de variograma**: Esférico, exponencial, gaussiano, etc.
- **Anisotropia**: Variação da correlação espacial com a direção

### Características

- **Vantagens**: Fornece estimativa de erro, considera a estrutura espacial dos dados
- **Desvantagens**: Mais complexo, computacionalmente mais intensivo
- **Parâmetros importantes**: Modelo de variograma, parâmetros do variograma, anisotropia

## Modelo Potenciométrico

O modelo potenciométrico é utilizado para calcular gradientes e vetores de fluxo a partir de uma superfície interpolada, como níveis de água subterrânea.

### Conceitos-chave

- **Gradiente**: Taxa de variação da superfície em cada direção
- **Vetores de fluxo**: Direção e magnitude do fluxo, perpendicular às linhas equipotenciais
- **Lei de Darcy**: O fluxo ocorre do potencial maior para o menor

### Características

- **Aplicações**: Hidrogeologia, análise de fluxo de águas subterrâneas
- **Visualização**: Vetores de fluxo sobrepostos à superfície potenciométrica
