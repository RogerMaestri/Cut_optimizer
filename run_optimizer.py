#!/usr/bin/env python3
"""
Script launcher para o Otimizador de Cortes
Detecta automaticamente se pode usar GUI ou precisa usar CLI
"""

import subprocess
import sys
import os
from datetime import datetime
from itertools import combinations

ROLL_WIDTH = 1050  # largura fixa do rolo em mm

def pack_pieces(pieces):
    """
    Algoritmo otimizado de força-bruta inteligente para maximizar aproveitamento.
    """
    # Expande peças individuais
    individual_pieces = []
    for p in pieces:
        for _ in range(p['qty']):
            individual_pieces.append((p['w'], p['h'], p['w'], p['h']))

    rows = []
    remaining = individual_pieces[:]
    
    while remaining:
        # Gera orientações possíveis para peças restantes
        orientations = []
        for i, (w, h, orig_w, orig_h) in enumerate(remaining):
            orientations.append((i, w, h, orig_w, orig_h))      # original
            if w != h:  # rotacionada se diferente
                orientations.append((i, h, w, orig_w, orig_h))
        
        # Busca melhor combinação para esta faixa
        best_combo = []
        best_fill = -1
        
        # Testa combinações de até 6 orientações
        for r in range(1, min(6, len(orientations)) + 1):
            for combo in combinations(range(len(orientations)), r):
                # Verifica se usa peças diferentes
                used_pieces = set()
                valid = True
                total_width = 0
                
                for idx in combo:
                    piece_idx = orientations[idx][0]
                    if piece_idx in used_pieces:
                        valid = False
                        break
                    used_pieces.add(piece_idx)
                    total_width += orientations[idx][1]  # largura
                
                if valid and total_width <= ROLL_WIDTH and total_width > best_fill:
                    best_fill = total_width
                    best_combo = [orientations[idx] for idx in combo]
                    if best_fill == ROLL_WIDTH:  # preenchimento perfeito
                        break
            if best_fill == ROLL_WIDTH:
                break
        
        if not best_combo:
            break
            
        # Remove peças usadas
        used_indices = sorted([item[0] for item in best_combo], reverse=True)
        for idx in used_indices:
            remaining.pop(idx)
        
        # Cria faixa
        used_width = sum(item[1] for item in best_combo)
        max_height = max(item[2] for item in best_combo)
        
        row = {
            'items': [{'w': item[1], 'h': item[2], 'orig_w': item[3], 'orig_h': item[4]} 
                      for item in best_combo],
            'used_width': used_width,
            'height': max_height
        }
        rows.append(row)
    
    return rows

def format_measurement(mm):
    """Converte milímetros para formato mais legível"""
    if mm >= 1000:
        return f"{mm/1000:.1f} m"
    else:
        return f"{mm} mm"

def create_visual_row(row_num, row, roll_width):
    """Cria uma representação visual muito clara da faixa"""
    used_width = row['used_width']
    leftover = roll_width - used_width
    height = row['height']
    
    visual = f"\n{'='*60}\n🎯 FAIXA NÚMERO {row_num}\n{'='*60}\n\n"
    visual += "📏 COMO CORTAR ESTA FAIXA:\n" + "─" * 40 + "\n"
    
    current_pos = 0
    for i, item in enumerate(row['items'], 1):
        piece_width = item['w']
        piece_height = item['h']
        orig_width = item['orig_w']
        orig_height = item['orig_h']
        
        start_pos = current_pos
        end_pos = current_pos + piece_width
        
        visual += f"\n🔸 PEÇA {i} ({orig_width}×{orig_height}mm):\n"
        
        if piece_width == orig_width:
            visual += f"   ⬜ DEITADA | {piece_width}mm × {piece_height}mm\n"
        else:
            visual += f"   ⬜ EM PÉ | {piece_width}mm × {piece_height}mm\n"
        
        visual += f"   📍 Posição: {start_pos}mm a {end_pos}mm\n"
        current_pos += piece_width
    
    if leftover > 0:
        visual += f"\n⚠️  SOBRA: {leftover}mm (do {used_width}mm ao {roll_width}mm)\n"
    
    visual += f"\n📋 RESUMO: {len(row['items'])} peças | {used_width}mm usado | {(used_width/roll_width)*100:.1f}% aproveitamento\n"
    
    return visual

def create_pieces_summary(pieces):
    """Cria um resumo claro das peças"""
    summary = "\n📦 PEÇAS QUE SERÃO CORTADAS:\n\n"
    
    for i, piece in enumerate(pieces, 1):
        width = piece['w']
        height = piece['h']
        qty = piece['qty']
        area = width * height
        
        summary += f"🔸 PEÇA {i}: {width}×{height}mm | {qty} unidades | {area * qty} mm² total\n"
    
    return summary

def get_roll_dimensions():
    """Coleta as dimensões do rolo"""
    print("📏 DIMENSÕES DO ROLO:")
    print("─" * 30)
    
    while True:
        try:
            roll_width = input("   Largura do rolo (mm) [padrão: 1050]: ").strip()
            if not roll_width:
                roll_width = 1050
            else:
                roll_width = int(roll_width)
            
            if roll_width <= 0:
                print("   ⚠️ Largura deve ser maior que zero!")
                continue
            break
        except ValueError:
            print("   ⚠️ Digite apenas números!")
    
    while True:
        try:
            roll_height = input("   Altura máxima (mm) [padrão: 50000]: ").strip()
            if not roll_height:
                roll_height = 50000
            else:
                roll_height = int(roll_height)
            
            if roll_height <= 0:
                print("   ⚠️ Altura deve ser maior que zero!")
                continue
            break
        except ValueError:
            print("   ⚠️ Digite apenas números!")
    
    return roll_width, roll_height

def get_pieces_input():
    """Coleta as dimensões das peças do usuário"""
    print("🎯 OTIMIZADOR DE CORTES DE MANTAS PRI (ALGORITMO OTIMIZADO)")
    print("=" * 60)
    print("Algoritmo: Força-bruta inteligente para máximo aproveitamento")
    print("\nInsira as dimensões das peças (Enter vazio para finalizar):")
    
    pieces = []
    i = 1
    while True:
        print(f"\n📝 PEÇA {i}:")
        try:
            w_input = input("   Largura (mm): ").strip()
            if not w_input:
                break
            w = int(w_input)
            
            h = int(input("   Altura (mm): "))
            q = int(input("   Quantidade: "))
            
            if w > 0 and h > 0 and q > 0:
                pieces.append({'w': w, 'h': h, 'qty': q})
                print(f"   ✅ Adicionada: {w}×{h}mm ({q} unidades)")
                i += 1
            else:
                print("   ⚠️ Valores devem ser maiores que zero!")
        except ValueError:
            print("   ⚠️ Digite apenas números!")
        except KeyboardInterrupt:
            print("\n\nOperação cancelada.")
            sys.exit(0)
    
    return pieces

def run_cli():
    """Executa versão CLI otimizada"""
    # Coleta dimensões do rolo
    roll_width, roll_height = get_roll_dimensions()
    print(f"   ✅ Rolo configurado: {roll_width}×{roll_height}mm\n")
    
    # Coleta peças
    pieces = get_pieces_input()
    
    if not pieces:
        print("⚠️ Nenhuma peça foi informada!")
        return
    
    # Validação: verifica se todas as peças cabem no rolo
    for piece in pieces:
        if piece['w'] > roll_width and piece['h'] > roll_width:
            print(f"⚠️ ERRO: Peça {piece['w']}×{piece['h']}mm não cabe no rolo de {roll_width}mm de largura!")
            return
    
    print("\n🚀 CALCULANDO PLANO OTIMIZADO...")
    print("   Testando todas as combinações e orientações...")
    
    # Calcula otimização
    rows = pack_pieces(pieces, roll_width, roll_height)
    total_height = sum(r['height'] for r in rows)
    total_area = roll_width * total_height
    
    used_area = 0
    for r in rows:
        for item in r['items']:
            used_area += item['w'] * item['h']
    
    loss_area = total_area - used_area
    util = used_area / total_area * 100 if total_area else 0
    
    print(f"   ✅ Concluído! {util:.1f}% de aproveitamento")
    
    # Monta resultado
    result = "🎯 PLANO DE CORTE OTIMIZADO\n" + "=" * 60 + "\n\n"
    
    # Informações básicas
    result += "📏 INFORMAÇÕES BÁSICAS:\n" + "─" * 40 + "\n"
    result += f"   • Largura da manta: {format_measurement(roll_width)}\n"
    result += f"   • Total de peças: {sum(p['qty'] for p in pieces)}\n"
    result += f"   • Total de faixas: {len(rows)}\n"
    result += f"   • Comprimento total: {format_measurement(total_height)}\n"
    result += f"   • Aproveitamento: {util:.1f}%\n"
    
    # Resumo das peças
    result += create_pieces_summary(pieces)
    
    # Detalhes de cada faixa
    result += "\n📐 DETALHES DE CADA FAIXA:\n" + "=" * 60
    
    for i, r in enumerate(rows, 1):
        visual_row = create_visual_row(i, r, roll_width)
        result += visual_row
    
    # Resumo final
    result += f"\n\n🎯 RESUMO FINAL:\n"
    result += f"   • {sum(len(r['items']) for r in rows)} peças em {len(rows)} faixas\n"
    result += f"   • {used_area} mm² utilizados de {total_area} mm² totais\n"
    result += f"   • {util:.1f}% de aproveitamento do material\n"
    
    if util >= 90:
        result += "   ✅ EXCELENTE aproveitamento!\n"
    elif util >= 80:
        result += "   👍 BOM aproveitamento!\n"
    elif util >= 70:
        result += "   ⚠️ Aproveitamento regular.\n"
    else:
        result += "   ❌ Baixo aproveitamento.\n"
    
    # Exibe resultado
    print("\n" + result)
    
    # Pergunta se quer salvar
    try:
        save = input("\n💾 Salvar resultado em arquivo? (s/n): ").strip().lower()
        if save in ['s', 'sim', 'y', 'yes']:
            filename = f"plano_corte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"PLANO DE CORTE OTIMIZADO\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
                f.write(result)
            print(f"✅ Arquivo salvo: {filename}")
            
        again = input("\n🔄 Calcular outro plano? (s/n): ").strip().lower()
        if again in ['s', 'sim', 'y', 'yes']:
            print("\n" + "="*60)
            run_cli()
            
    except KeyboardInterrupt:
        print("\n\nFinalizado.")

def test_gui():
    """Testa se a GUI funciona"""
    try:
        # Tenta executar o arquivo GUI original
        result = subprocess.run([sys.executable, 'cut_optimizer.py'], 
                              capture_output=True, text=True, timeout=2)
        return result.returncode == 0
    except:
        return False

def main():
    """Função principal que decide entre GUI e CLI"""
    print("🎯 OTIMIZADOR DE CORTES DE MANTAS PRI")
    print("Testando disponibilidade da interface gráfica...")
    
    if test_gui():
        print("✅ Interface gráfica disponível! Abrindo GUI...")
        subprocess.run([sys.executable, 'cut_optimizer.py'])
    else:
        print("⚠️ Interface gráfica não disponível (macOS 12.6)")
        print("🚀 Executando em modo linha de comando otimizado...\n")
        run_cli()

if __name__ == "__main__":
    main()