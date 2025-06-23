# 🎯 Otimizador de Cortes de Mantas PRI

## 📋 Descrição

Sistema inteligente para otimização de cortes de mantas, desenvolvido em Python com interface gráfica Tkinter. O algoritmo utiliza força-bruta inteligente para maximizar o aproveitamento do material, gerando planos de corte detalhados e visuais.

## ✨ Funcionalidades

- **🎯 Otimização Inteligente**: Algoritmo de força-bruta que testa todas as combinações possíveis
- **📐 Dimensões Flexíveis**: Suporte a rolos de diferentes tamanhos
- **🔄 Rotação Automática**: Peças podem ser rotacionadas para melhor aproveitamento
- **📊 Visualização Clara**: Output detalhado com desenhos e instruções passo a passo
- **📤 Múltiplas Exportações**: TXT, PDF, impressão e área de transferência
- **📏 Medidas Intuitivas**: Resultados em metros quadrados para fácil compreensão

## 🛠️ Tecnologias

- **Python 3.10+**
- **Tkinter** - Interface gráfica
- **itertools** - Combinações e otimizações
- **datetime** - Timestamps nos relatórios

## 📦 Instalação

### Pré-requisitos
```bash
# Python 3.10 ou superior
python --version

# Tkinter (geralmente já vem com Python)
# No macOS, se necessário:
brew install python-tk
```

### Clone e Execute
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/cut_optimizer_project.git

# Entre no diretório
cd cut_optimizer_project

# Execute o programa
python cut_optimizer.py
```

## 🎮 Como Usar

### 1. Configurar Dimensões do Rolo
- **Largura do rolo**: Defina a largura da manta (padrão: 1050mm)
- **Altura máxima**: Defina o comprimento máximo (padrão: 50000mm)

### 2. Inserir Peças
- **Largura**: Dimensão da peça em mm
- **Altura**: Dimensão da peça em mm  
- **Quantidade**: Número de peças necessárias

### 3. Calcular e Visualizar
- Clique em "🚀 CALCULAR PLANO DE CORTE OTIMIZADO"
- Visualize o resultado detalhado
- Use os botões de exportação conforme necessário

## 📊 Exemplo de Output

```
🎯 FAIXA NÚMERO 1 - CORTE ÚNICO
================================================================================

📋 RESUMO EXECUTIVO:
   • Quantidade de peças nesta faixa: 2
   • Altura do corte: 800 mm
   • Largura total utilizada: 1000 mm
   • Aproveitamento: 95.2%

📐 DESENHO DO CORTE:
   ┌────────────────────────────────────────────────────────────────────────────┐
   │                                ROL                                         │
   │                            DE MANTA 1.050mm                               │
   └────────────────────────────────────────────────────────────────────────────┘
   ┌─────────────┐┌─────────────┐
   │      1      ││      2      │
   └─────────────┘└─────────────┘

✂️  INSTRUÇÕES DE CORTE:
1. Corte uma faixa de 800mm de altura do rolo
2. Na faixa cortada, faça os seguintes cortes verticais:

   Corte 1: na posição 800mm
   → Resultado: peça 800×500mm

   Corte 2: na posição 1000mm
   → Resultado: peça 500×400mm

   RESULTADO FINAL: 2 peças cortadas lado a lado
```

## 🔧 Algoritmo

O sistema utiliza um algoritmo de **força-bruta inteligente** que:

1. **Expande peças**: Cria todas as peças individuais com suas quantidades
2. **Gera orientações**: Testa rotações de 0° e 90° para cada peça
3. **Combinações**: Testa todas as combinações possíveis de até 6 peças por faixa
4. **Otimiza**: Escolhe a combinação que melhor preenche a largura do rolo
5. **Itera**: Repete o processo até usar todas as peças

## 📈 Vantagens

- **🎯 Máximo Aproveitamento**: Algoritmo otimizado para minimizar desperdício
- **👁️ Visualização Clara**: Output intuitivo com desenhos e instruções
- **📱 Interface Amigável**: GUI simples e funcional
- **📤 Exportação Flexível**: Múltiplos formatos de saída
- **🔧 Configurável**: Dimensões de rolo personalizáveis
- **📏 Medidas Práticas**: Resultados em m² para fácil compreensão

## 🚀 Roadmap

- [ ] **Correção de erros de linting** (285 erros → 0)
- [ ] **Interface web** com React/Flask
- [ ] **API REST** para integração com outros sistemas
- [ ] **Banco de dados** para histórico de projetos
- [ ] **Relatórios avançados** com gráficos
- [ ] **Múltiplos algoritmos** de otimização

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Rogério Maestri**
- Desenvolvedor Python
- Especialista em otimização e automação
- Contato: [seu-email@exemplo.com]

## 🙏 Agradecimentos

- Comunidade Python
- Biblioteca Tkinter
- Algoritmos de empacotamento 2D
- Usuários que testaram e forneceram feedback

---

**⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!** 