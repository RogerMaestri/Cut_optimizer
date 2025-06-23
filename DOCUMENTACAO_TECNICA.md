# Documentação Técnica - Sistema de Otimização de Cortes de Mantas PRI

## 1. Visão Geral do Sistema

### 1.1 Propósito
O Sistema de Otimização de Cortes de Mantas PRI é uma aplicação desktop desenvolvida em Python com interface gráfica Tkinter, projetada para maximizar o aproveitamento de material durante o processo de corte de mantas industriais.

### 1.2 Objetivos Principais
- **Otimização de Aproveitamento**: Maximizar o uso da área disponível do rolo de manta
- **Facilidade de Uso**: Interface intuitiva para usuários com baixa alfabetização digital
- **Flexibilidade**: Suporte a múltiplas dimensões de peças e quantidades
- **Exportação**: Múltiplos formatos de saída para diferentes necessidades operacionais

### 1.3 Público-Alvo
- Operadores de máquinas de corte industrial
- Planejadores de produção
- Supervisores de fábrica
- Usuários com diferentes níveis de alfabetização digital

## 2. Arquitetura do Sistema

### 2.1 Estrutura Modular
```
cut_optimizer.py
├── Algoritmo de Otimização (pack_pieces)
├── Interface Gráfica (Tkinter)
├── Sistema de Exportação
├── Formatação e Visualização
└── Utilitários de Conversão
```

### 2.2 Componentes Principais

#### 2.2.1 Módulo de Otimização
- **Função Principal**: `pack_pieces()`
- **Algoritmo**: Força-bruta inteligente com otimizações
- **Complexidade**: O(n^k) onde k é limitado a 6 para performance
- **Estratégia**: Testa todas as combinações e orientações possíveis

#### 2.2.2 Interface Gráfica
- **Framework**: Tkinter (biblioteca padrão Python)
- **Layout**: Organizado em frames lógicos
- **Responsividade**: Adaptável a diferentes resoluções
- **Acessibilidade**: Cores contrastantes e fontes legíveis

#### 2.2.3 Sistema de Exportação
- **Formatos Suportados**: TXT, PDF (simulado), Clipboard, Impressão
- **Codificação**: UTF-8 para suporte a caracteres especiais
- **Metadados**: Data, hora e informações do projeto incluídos

## 3. Algoritmo de Otimização

### 3.1 Estratégia Geral
O algoritmo implementa uma abordagem de força-bruta inteligente que:

1. **Expansão de Peças**: Converte quantidades em peças individuais
2. **Geração de Orientações**: Cria todas as orientações possíveis (original + rotacionada)
3. **Combinação Inteligente**: Testa combinações de até 6 peças por faixa
4. **Seleção Ótima**: Escolhe a combinação com maior aproveitamento
5. **Iteração**: Repete o processo até esgotar todas as peças

### 3.2 Pseudocódigo Detalhado
```
FUNÇÃO pack_pieces(pieces, roll_width, roll_height):
    individual_pieces = expandir_quantidades(pieces)
    rows = []
    remaining = individual_pieces
    
    ENQUANTO remaining não estiver vazio:
        orientations = gerar_orientacoes(remaining)
        best_combo = encontrar_melhor_combinacao(orientations, roll_width)
        
        SE best_combo encontrado:
            row = criar_faixa(best_combo)
            rows.append(row)
            remaining = remover_pecas_usadas(remaining, best_combo)
        SENÃO:
            BREAK
    
    RETORNAR rows
```

### 3.3 Otimizações Implementadas

#### 3.3.1 Limitação de Combinações
- **Limite**: Máximo 6 peças por combinação
- **Justificativa**: Balanceamento entre qualidade e performance
- **Impacto**: Redução significativa do tempo de processamento

#### 3.3.2 Detecção de Preenchimento Perfeito
- **Condição**: `best_fill == roll_width`
- **Ação**: Interrupção imediata da busca
- **Benefício**: Evita processamento desnecessário

#### 3.3.3 Validação de Peças
- **Verificação**: Dimensões vs largura do rolo
- **Rotação**: Consideração automática de orientações alternativas
- **Rejeição**: Peças que não cabem em nenhuma orientação

## 4. Estruturas de Dados

### 4.1 Representação de Peças
```python
piece = {
    'w': int,      # Largura em mm
    'h': int,      # Altura em mm
    'qty': int     # Quantidade necessária
}
```

### 4.2 Representação de Faixas
```python
row = {
    'items': [     # Lista de peças na faixa
        {
            'w': int,       # Largura da peça
            'h': int,       # Altura da peça
            'orig_w': int,  # Largura original
            'orig_h': int   # Altura original
        }
    ],
    'used_width': int,  # Largura total utilizada
    'height': int       # Altura da faixa
}
```

### 4.3 Variáveis Globais
```python
ROLL_WIDTH = 1050  # Largura padrão do rolo em mm
current_result_text = ""  # Texto atual para exportação
current_pieces_data = []  # Dados das peças atuais
```

## 5. Interface Gráfica

### 5.1 Layout da Interface
```
┌─────────────────────────────────────────────────────────┐
│ 🎯 OTIMIZADOR DE CORTES DE MANTAS PRI (OTIMIZADO)      │
├─────────────────────────────────────────────────────────┤
│ 📏 DIMENSÕES DO ROLO                                    │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Largura: [1050] Altura Máxima: [50000]             │ │
│ └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ 📝 DADOS DAS PEÇAS                                      │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Largura │ Altura │ Quantidade                        │ │
│ │ [     ] │ [     ] │ [     ]                          │ │
│ │ [     ] │ [     ] │ [     ]                          │ │
│ └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ 🚀 CALCULAR PLANO DE CORTE OTIMIZADO                   │
├─────────────────────────────────────────────────────────┤
│ 📤 EXPORTAR RESULTADO                                   │
│ [📄 TXT] [📋 Copiar] [🖨️ Imprimir] [📊 PDF]           │
├─────────────────────────────────────────────────────────┤
│ 📊 RESULTADO                                            │
│ ┌─────────────────────────────────────────────────────┐ │
│ │                                                     │ │
│ │ Área de resultados com scroll                       │ │
│ │                                                     │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Componentes da Interface

#### 5.2.1 Frames Principais
- **roll_frame**: Configuração das dimensões do rolo
- **input_frame**: Entrada de dados das peças
- **buttons_frame**: Botão de cálculo
- **export_frame**: Botões de exportação
- **result_frame**: Área de resultados

#### 5.2.2 Campos de Entrada
- **roll_width_entry**: Largura do rolo (padrão: 1050mm)
- **roll_height_entry**: Altura máxima (padrão: 50000mm)
- **entries**: Lista de tuplas (width, height, quantity) para peças

#### 5.2.3 Botões de Ação
- **calc_button**: Executa o algoritmo de otimização
- **export_buttons**: Conjunto de botões para diferentes formatos de saída

### 5.3 Design de Usabilidade

#### 5.3.1 Princípios Aplicados
- **Consistência Visual**: Cores e fontes padronizadas
- **Hierarquia Clara**: Informações organizadas por importância
- **Feedback Imediato**: Mensagens de erro e sucesso claras
- **Acessibilidade**: Contraste adequado e fontes legíveis

#### 5.3.2 Elementos Visuais
- **Emojis**: Facilitam identificação rápida de seções
- **Cores**: Azul (#2E86AB) para elementos principais
- **Fontes**: Arial para legibilidade, Consolas para resultados
- **Espaçamento**: Padding adequado para conforto visual

## 6. Sistema de Processamento

### 6.1 Fluxo de Execução
```
1. Validação de Entrada
   ├── Verificação de dimensões do rolo
   ├── Validação de peças
   └── Verificação de compatibilidade

2. Execução do Algoritmo
   ├── Expansão de quantidades
   ├── Geração de orientações
   ├── Busca de combinações ótimas
   └── Criação de faixas

3. Cálculo de Métricas
   ├── Área total utilizada
   ├── Área desperdiçada
   ├── Percentual de aproveitamento
   └── Comprimento total necessário

4. Formatação de Saída
   ├── Resumo executivo
   ├── Visualização detalhada
   ├── Instruções de corte
   └── Métricas finais
```

### 6.2 Validações Implementadas

#### 6.2.1 Validação de Dimensões
```python
if roll_width <= 0 or roll_height <= 0:
    raise ValueError("Dimensões devem ser maiores que zero")
```

#### 6.2.2 Validação de Peças
```python
if piece['w'] > roll_width and piece['h'] > roll_width:
    raise ValueError("Peça não cabe no rolo")
```

#### 6.2.3 Validação de Quantidades
```python
if w > 0 and h > 0 and q > 0:
    pieces.append({'w': w, 'h': h, 'qty': q})
```

### 6.3 Tratamento de Erros
- **Try-Catch**: Captura de exceções em operações críticas
- **MessageBox**: Feedback visual para o usuário
- **Validação Preventiva**: Verificação antes da execução
- **Recuperação Graceful**: Continuação da execução quando possível

## 7. Sistema de Exportação

### 7.1 Formatos Suportados

#### 7.1.1 Arquivo TXT
- **Codificação**: UTF-8
- **Metadados**: Data, hora, dimensões do rolo
- **Conteúdo**: Resultado completo formatado
- **Vantagens**: Compatibilidade universal, fácil leitura

#### 7.1.2 Área de Transferência
- **Formato**: Texto simples
- **Uso**: Colagem em outros aplicativos
- **Vantagens**: Transferência rápida, sem arquivos

#### 7.1.3 Impressão
- **Método**: Comando do sistema (lpr)
- **Arquivo Temporário**: Criação automática
- **Limpeza**: Remoção automática após impressão
- **Vantagens**: Saída física imediata

#### 7.1.4 PDF (Simulado)
- **Implementação**: Arquivo TXT com extensão .pdf
- **Futuro**: Integração com biblioteca reportlab
- **Vantagens**: Formato profissional, preservação de layout

### 7.2 Estrutura de Exportação
```
PLANO DE CORTE OTIMIZADO
==================================================
Data: DD/MM/AAAA HH:MM
Largura do rolo: XXXX mm

🎯 PLANO DE CORTE DE MANTAS PRI (OTIMIZADO)
============================================================

📏 INFORMAÇÕES BÁSICAS:
   • Largura da manta: XXXX mm
   • Total de peças: XXX
   • Total de faixas: XX
   • Comprimento total: XXXX mm
   • Aproveitamento: XX.X%

📦 PEÇAS QUE SERÃO CORTADAS:
   [Detalhes das peças...]

📐 DETALHES DE CADA FAIXA:
   [Visualização detalhada...]

🎯 RESUMO COMPLETO DO CORTE:
   [Resumo final...]
```

## 8. Funções de Formatação

### 8.1 Conversão de Medidas
```python
def format_measurement(mm):
    """Converte milímetros para formato legível"""
    if mm >= 1000:
        return f"{mm/1000:.1f} m"
    else:
        return f"{mm} mm"

def format_area_m2(mm2):
    """Converte mm² para m² ou cm²"""
    m2 = mm2 / 1_000_000
    if m2 >= 1:
        return f"{m2:.2f} m²"
    else:
        return f"{m2*10000:.1f} cm²"
```

### 8.2 Visualização de Faixas
```python
def create_visual_row(row_num, row, roll_width):
    """Cria representação visual detalhada da faixa"""
    # Implementação detalhada com:
    # - Resumo executivo
    # - Desenho visual do rolo
    # - Posicionamento das peças
    # - Instruções de corte
```

### 8.3 Resumos e Sumários
```python
def create_pieces_summary(pieces):
    """Resumo das peças a serem cortadas"""

def create_visual_summary(rows, total_height, used_area, loss_area, util):
    """Resumo completo do corte"""
```

## 9. Testes e Validação

### 9.1 Cenários de Teste

#### 9.1.1 Casos Básicos
- **Peça Única**: Uma peça que cabe perfeitamente no rolo
- **Múltiplas Peças Iguais**: Várias peças do mesmo tamanho
- **Peças Diferentes**: Mistura de dimensões variadas

#### 9.1.2 Casos Extremos
- **Rolo Pequeno**: Largura mínima para testar limitações
- **Peças Grandes**: Dimensões próximas ao limite do rolo
- **Muitas Peças**: Grande quantidade de peças pequenas

#### 9.1.3 Casos de Erro
- **Dimensões Inválidas**: Valores negativos ou zero
- **Peças Incompatíveis**: Dimensões maiores que o rolo
- **Entrada Vazia**: Ausência de dados válidos

### 9.2 Métricas de Qualidade
- **Aproveitamento**: Percentual de área utilizada
- **Tempo de Processamento**: Performance do algoritmo
- **Precisão**: Acerto nas dimensões calculadas
- **Usabilidade**: Facilidade de uso da interface

## 10. Deployment e Distribuição

### 10.1 Requisitos do Sistema
- **Python**: Versão 3.6 ou superior
- **Tkinter**: Incluído na instalação padrão do Python
- **Sistema Operacional**: Windows, macOS, Linux
- **Memória**: Mínimo 512MB RAM
- **Armazenamento**: 10MB para aplicação

### 10.2 Dependências
```
tkinter (incluído no Python)
itertools (biblioteca padrão)
datetime (biblioteca padrão)
os (biblioteca padrão)
```

### 10.3 Processo de Build
```bash
# Instalação de dependências
pip install -r requirements.txt

# Criação do executável (PyInstaller)
pyinstaller --onefile --windowed cut_optimizer.py

# Distribuição
# - Executável gerado
# - README.txt com instruções
# - Arquivo ZIP para distribuição
```

### 10.4 Estrutura de Distribuição
```
cut_optimizer_distrib/
├── cut_optimizer.exe (Windows)
├── README.txt
└── cut_optimizer_project.zip
```

## 11. Manutenção e Evolução

### 11.1 Monitoramento
- **Logs de Erro**: Captura de exceções não tratadas
- **Métricas de Uso**: Tempo de processamento, tipos de entrada
- **Feedback do Usuário**: Coleta de sugestões e problemas

### 11.2 Atualizações Planejadas
- **Algoritmo Avançado**: Implementação de algoritmos mais sofisticados
- **Interface Melhorada**: Design mais moderno e responsivo
- **Exportação PDF**: Integração com biblioteca reportlab
- **Banco de Dados**: Persistência de projetos e configurações

### 11.3 Melhorias de Performance
- **Multithreading**: Processamento paralelo para grandes volumes
- **Cache**: Armazenamento de resultados intermediários
- **Otimização de Memória**: Redução do uso de recursos

## 12. Considerações de Segurança

### 12.1 Validação de Entrada
- **Sanitização**: Remoção de caracteres perigosos
- **Limites**: Validação de valores máximos e mínimos
- **Tipos**: Verificação de tipos de dados

### 12.2 Manipulação de Arquivos
- **Caminhos Seguros**: Validação de caminhos de arquivo
- **Permissões**: Verificação de permissões de escrita
- **Limpeza**: Remoção de arquivos temporários

### 12.3 Interface Segura
- **Escape de Caracteres**: Prevenção de injeção de código
- **Validação de Formulários**: Verificação de dados de entrada
- **Feedback Seguro**: Mensagens sem exposição de informações sensíveis

## 13. Documentação de API

### 13.1 Funções Principais

#### pack_pieces(pieces, roll_width, roll_height)
```python
"""
Algoritmo de otimização de cortes.

Args:
    pieces: Lista de dicionários com 'w', 'h', 'qty'
    roll_width: Largura do rolo em mm
    roll_height: Altura máxima do rolo em mm

Returns:
    Lista de faixas otimizadas
"""
```

#### calculate()
```python
"""
Função principal de cálculo.
Executa validação, otimização e formatação de resultados.
"""
```

#### export_to_txt()
```python
"""
Exporta resultado para arquivo TXT.
Permite seleção de local e nome do arquivo.
"""
```

### 13.2 Constantes e Configurações
```python
ROLL_WIDTH = 1050  # Largura padrão do rolo
MAX_COMBINATIONS = 6  # Limite de peças por combinação
DEFAULT_ROLL_HEIGHT = 50000  # Altura padrão (ilimitada)
```

## 14. Conclusão

O Sistema de Otimização de Cortes de Mantas PRI representa uma solução completa e eficiente para o problema de maximização de aproveitamento de material industrial. Sua arquitetura modular, interface intuitiva e algoritmo otimizado proporcionam uma ferramenta valiosa para operações de corte industrial.

### 14.1 Pontos Fortes
- **Algoritmo Eficiente**: Balanceamento entre qualidade e performance
- **Interface Intuitiva**: Design focado na usabilidade
- **Flexibilidade**: Suporte a múltiplos cenários de uso
- **Robustez**: Tratamento abrangente de erros

### 14.2 Áreas de Melhoria
- **Performance**: Implementação de algoritmos mais avançados
- **Interface**: Modernização do design visual
- **Funcionalidades**: Adição de recursos avançados
- **Integração**: Conectividade com sistemas externos

### 14.3 Impacto Esperado
- **Redução de Desperdício**: Aumento do aproveitamento de material
- **Economia**: Redução de custos operacionais
- **Eficiência**: Otimização do tempo de planejamento
- **Satisfação**: Melhoria na experiência do usuário

---

**Versão**: 1.0  
**Data**: Dezembro 2024  
**Autor**: Sistema de Otimização de Cortes de Mantas PRI  
**Licença**: MIT 