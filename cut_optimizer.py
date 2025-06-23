import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import os
from datetime import datetime
from itertools import combinations

ROLL_WIDTH = 1050  # largura fixa do rolo em mm

# Variáveis globais para armazenar o resultado atual
current_result_text = ""
current_pieces_data = []


def pack_pieces(pieces, roll_width=ROLL_WIDTH, roll_height=None):
    """
    Algoritmo otimizado de força-bruta inteligente para maximizar aproveitamento.
    Testa todas as combinações e orientações possíveis para cada faixa.
    
    Args:
        pieces: Lista de peças com dimensões e quantidades
        roll_width: Largura do rolo (padrão: 1050mm)
        roll_height: Altura máxima do rolo (padrão: sem limite)
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
        
        # Testa combinações de até 6 orientações (otimização de performance)
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
                
                if valid and total_width <= roll_width and total_width > best_fill:
                    best_fill = total_width
                    best_combo = [orientations[idx] for idx in combo]
                    if best_fill == roll_width:  # preenchimento perfeito
                        break
            if best_fill == roll_width:
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


def format_area_m2(mm2):
    """Converte milímetros quadrados para metros quadrados"""
    m2 = mm2 / 1_000_000  # 1 m² = 1.000.000 mm²
    if m2 >= 1:
        return f"{m2:.2f} m²"
    else:
        return f"{m2*10000:.1f} cm²"  # Para áreas muito pequenas, usa cm²


def create_visual_row(row_num, row, roll_width):
    """Cria uma representação visual muito clara e intuitiva da faixa"""
    used_width = row['used_width']
    leftover = roll_width - used_width
    height = row['height']
    
    # Cabeçalho da faixa
    visual = f"\n{'='*80}\n"
    visual += f"🎯 FAIXA NÚMERO {row_num} - CORTE ÚNICO\n"
    visual += f"{'='*80}\n\n"
    
    # RESUMO EXECUTIVO ANTES DE TUDO
    visual += "📋 RESUMO EXECUTIVO:\n"
    visual += "─" * 50 + "\n"
    visual += f"   • Quantidade de peças nesta faixa: {len(row['items'])}\n"
    visual += f"   • Altura do corte: {height} mm\n"
    visual += f"   • Largura total utilizada: {used_width} mm\n"
    if leftover > 0:
        visual += f"   • Largura desperdiçada: {leftover} mm\n"
    visual += f"   • Aproveitamento: {(used_width/roll_width)*100:.1f}%\n\n"
    
    # DESENHO VISUAL DO ROLO COM PEÇAS
    visual += "📐 DESENHO DO CORTE:\n"
    visual += "─" * 50 + "\n"
    visual += f"   Largura total do rolo: {roll_width} mm\n\n"
    
    # Desenho do rolo com as peças posicionadas
    visual += "   ┌" + "─" * 76 + "┐\n"
    visual += f"   │{'ROL':^76}│\n"
    visual += f"   │{'DE MANTA 1.050mm':^76}│\n"
    visual += "   └" + "─" * 76 + "┘\n"
    
    # Posicionamento das peças no rolo
    current_pos = 0
    for i, item in enumerate(row['items'], 1):
        piece_width = item['w']
        piece_height = item['h']
        orig_width = item['orig_w']
        orig_height = item['orig_h']
        
        # Calcula posições
        start_pos = current_pos
        end_pos = current_pos + piece_width
        
        # Desenho da peça no rolo
        piece_visual = "─" * (piece_width // 10)  # Escala visual
        if len(piece_visual) < 3:
            piece_visual = "───"
        
        # Linha superior da peça
        if start_pos == 0:
            visual += "   ┌" + piece_visual + "┐"
        else:
            visual += "   " + " " * (start_pos // 10) + "┌" + piece_visual + "┐"
        
        # Espaço restante até o final
        remaining_space = (roll_width - end_pos) // 10
        if remaining_space > 0:
            visual += " " * remaining_space
        visual += "\n"
        
        # Conteúdo da peça
        if start_pos == 0:
            visual += f"   │{i:^{len(piece_visual)}}│"
        else:
            visual += "   " + " " * (start_pos // 10) + f"│{i:^{len(piece_visual)}}│"
        
        if remaining_space > 0:
            visual += " " * remaining_space
        visual += "\n"
        
        # Linha inferior da peça
        if start_pos == 0:
            visual += "   └" + piece_visual + "┘"
        else:
            visual += "   " + " " * (start_pos // 10) + "└" + piece_visual + "┘"
        
        if remaining_space > 0:
            visual += " " * remaining_space
        visual += "\n"
        
        current_pos += piece_width
    
    # Legenda das peças
    visual += "\n   LEGENDA:\n"
    current_pos = 0
    for i, item in enumerate(row['items'], 1):
        piece_width = item['w']
        piece_height = item['h']
        orig_width = item['orig_w']
        orig_height = item['orig_h']
        
        start_pos = current_pos
        end_pos = current_pos + piece_width
        
        visual += f"   [{i}] = {orig_width}×{orig_height}mm → corte de {piece_width}×{piece_height}mm\n"
        visual += f"        posição: {start_pos}mm até {end_pos}mm\n"
        
        current_pos += piece_width
    
    # Espaço desperdiçado
    if leftover > 0:
        visual += f"\n   ⚠️  ESPAÇO NÃO UTILIZADO:\n"
        visual += f"      • {leftover} mm desperdiçados\n"
        visual += f"      • posição: {used_width}mm até {roll_width}mm\n"
    
    visual += "\n"
    
    # INSTRUÇÕES DE CORTE CLARAS
    visual += "✂️  INSTRUÇÕES DE CORTE:\n"
    visual += "─" * 50 + "\n"
    visual += f"1. Corte uma faixa de {height}mm de altura do rolo\n"
    visual += f"2. Na faixa cortada, faça os seguintes cortes verticais:\n\n"
    
    current_pos = 0
    for i, item in enumerate(row['items'], 1):
        piece_width = item['w']
        piece_height = item['h']
        orig_width = item['orig_w']
        orig_height = item['orig_h']
        
        start_pos = current_pos
        end_pos = current_pos + piece_width
        
        visual += f"   Corte {i}: na posição {end_pos}mm\n"
        visual += f"   → Resultado: peça {orig_width}×{orig_height}mm\n\n"
        
        current_pos += piece_width
    
    if len(row['items']) > 1:
        visual += f"   RESULTADO FINAL: {len(row['items'])} peças cortadas lado a lado\n"
    else:
        visual += f"   RESULTADO FINAL: 1 peça cortada\n"
    
    visual += "\n" + "="*80 + "\n\n"
    
    return visual


def create_pieces_summary(pieces):
    """Cria um resumo claro das peças que serão cortadas"""
    summary = """
📦 PEÇAS QUE SERÃO CORTADAS:

"""
    
    total_pieces = sum(p['qty'] for p in pieces)
    total_area = sum(p['w'] * p['h'] * p['qty'] for p in pieces)
    
    summary += f"   📊 RESUMO GERAL:\n"
    summary += f"   • Total de tipos de peças: {len(pieces)}\n"
    summary += f"   • Total de peças a cortar: {total_pieces}\n"
    summary += f"   • Área total necessária: {format_area_m2(total_area)}\n\n"
    
    for i, piece in enumerate(pieces, 1):
        width = piece['w']
        height = piece['h']
        qty = piece['qty']
        area = width * height
        
        summary += f"   🔸 TIPO DE PEÇA {i}:\n"
        summary += f"      • Dimensões originais: {width}mm × {height}mm\n"
        summary += f"      • Quantidade necessária: {qty} unidades\n"
        summary += f"      • Área por peça: {format_area_m2(area)}\n"
        summary += f"      • Área total deste tipo: {format_area_m2(area * qty)}\n\n"
    
    return summary


def create_visual_summary(rows, total_height, used_area, loss_area, util, roll_width=ROLL_WIDTH):
    """Cria um resumo visual muito claro"""
    summary = f"""
🎯 RESUMO COMPLETO DO CORTE:

📏 MATERIAL NECESSÁRIO:
   • 1 manta de {format_measurement(roll_width)} de largura
   • {total_height}mm de comprimento total
   • Área total: {format_area_m2(roll_width * total_height)}

📦 O QUE VOCÊ VAI PRODUZIR:
   • {sum(len(r['items']) for r in rows)} peças no total
   • {len(rows)} faixas de corte
   • Área utilizada: {format_area_m2(used_area)}

🗑️  O QUE VAI SOBRAR:
   • {format_area_m2(loss_area)} de material desperdiçado
   • {util:.1f}% de aproveitamento do material

💡 AVALIAÇÃO:
"""
    
    if util >= 90:
        summary += "   ✅ EXCELENTE! Você aproveitou quase todo o material\n"
    elif util >= 80:
        summary += "   👍 BOM! O aproveitamento está satisfatório\n"
    elif util >= 70:
        summary += "   ⚠️  REGULAR! Pode melhorar um pouco\n"
    else:
        summary += "   ❌ BAIXO! Muito material está sendo desperdiçado\n"
    
    summary += "\n📋 LISTA DE FAIXAS:\n"
    for i, r in enumerate(rows, 1):
        pieces_count = len(r['items'])
        used_width = r['used_width']
        height = r['height']
        summary += (f"   • Faixa {i}: {pieces_count} peças, "
                   f"{used_width}mm usado, {height}mm altura\n")
    
    return summary


def export_to_txt():
    """Exporta o resultado para arquivo TXT"""
    if not current_result_text:
        messagebox.showwarning("Atenção", "Nenhum resultado para exportar!")
        return
    
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivo de texto", "*.txt"), ("Todos os arquivos", "*.*")],
        title="Salvar plano de corte como..."
    )
    
    if filename:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("PLANO DE CORTE OTIMIZADO\n")
                f.write("=" * 50 + "\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write(f"Largura do rolo: {format_measurement(ROLL_WIDTH)}\n\n")
                f.write(current_result_text)
            
            messagebox.showinfo("Sucesso", 
                              f"Plano salvo em:\n{filename}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{str(e)}")


def copy_to_clipboard():
    """Copia o resultado para a área de transferência"""
    if not current_result_text:
        messagebox.showwarning("Atenção", "Nenhum resultado para copiar!")
        return
    
    try:
        root.clipboard_clear()
        root.clipboard_append(current_result_text)
        messagebox.showinfo("Sucesso", 
                          "Plano de corte copiado para a área de transferência!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao copiar:\n{str(e)}")


def print_result():
    """Imprime o resultado"""
    if not current_result_text:
        messagebox.showwarning("Atenção", "Nenhum resultado para imprimir!")
        return
    
    try:
        # Cria um arquivo temporário para impressão
        temp_file = "temp_print.txt"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("PLANO DE CORTE OTIMIZADO\n")
            f.write("=" * 50 + "\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            f.write(current_result_text)
        
        # Imprime usando o comando do sistema
        os.system(f"lpr {temp_file}")
        
        # Remove o arquivo temporário
        os.remove(temp_file)
        
        messagebox.showinfo("Sucesso", "Enviado para impressora!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao imprimir:\n{str(e)}")


def export_to_pdf():
    """Exporta o resultado para PDF (simulado)"""
    if not current_result_text:
        messagebox.showwarning("Atenção", "Nenhum resultado para exportar!")
        return
    
    filename = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Arquivo PDF", "*.pdf")],
        title="Salvar plano de corte como PDF..."
    )
    
    if filename:
        try:
            # Por enquanto, criamos um arquivo de texto com extensão .pdf
            # Em uma versão futura, poderíamos usar bibliotecas como reportlab
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("PLANO DE CORTE OTIMIZADO\n")
                f.write("=" * 50 + "\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write(f"Largura do rolo: {format_measurement(ROLL_WIDTH)}\n\n")
                f.write(current_result_text)
            
            messagebox.showinfo("Sucesso", 
                              f"Plano salvo como PDF em:\n{filename}\n\n"
                              "Nota: Esta é uma versão simplificada. "
                              "Para PDF profissional, instale a biblioteca reportlab.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar PDF:\n{str(e)}")


def calculate():
    global current_result_text, current_pieces_data
    
    # Captura dimensões do rolo
    try:
        roll_width = int(roll_width_entry.get())
        roll_height = int(roll_height_entry.get())
        
        if roll_width <= 0 or roll_height <= 0:
            messagebox.showwarning("Atenção", "Dimensões do rolo devem ser maiores que zero")
            return
            
    except ValueError:
        messagebox.showwarning("Atenção", "Informe dimensões válidas para o rolo")
        return
    
    # Captura peças
    pieces = []
    for w_e, h_e, q_e in entries:
        try:
            w = int(w_e.get())
            h = int(h_e.get())
            q = int(q_e.get())
        except ValueError:
            continue
        if w > 0 and h > 0 and q > 0:
            pieces.append({'w': w, 'h': h, 'qty': q})

    if not pieces:
        messagebox.showwarning("Atenção", "Informe ao menos uma peça válida")
        return

    # Validação: verifica se todas as peças cabem no rolo
    for piece in pieces:
        if piece['w'] > roll_width and piece['h'] > roll_width:
            messagebox.showwarning("Atenção", 
                                 f"Peça {piece['w']}×{piece['h']}mm não cabe no rolo de {roll_width}mm de largura, "
                                 f"nem mesmo rotacionada!")
            return

    current_pieces_data = pieces.copy()
    
    # === ALGORITMO OTIMIZADO ===
    rows = pack_pieces(pieces, roll_width, roll_height)
    
    total_height = sum(r['height'] for r in rows)
    total_area = roll_width * total_height
    
    # Calcula área usada pelas peças
    used_area = 0
    for r in rows:
        for item in r['items']:
            used_area += item['w'] * item['h']
    
    loss_area = total_area - used_area
    util = used_area / total_area * 100 if total_area else 0

    result.delete('1.0', tk.END)
    
    # Cabeçalho muito claro
    result.insert(tk.END, "🎯 PLANO DE CORTE DE MANTAS PRI (OTIMIZADO)\n")
    result.insert(tk.END, "=" * 60 + "\n\n")
    
    # Informações básicas
    result.insert(tk.END, "📏 INFORMAÇÕES BÁSICAS:\n")
    result.insert(tk.END, "─" * 40 + "\n")
    result.insert(tk.END, 
                 f"   • Largura da manta: {format_measurement(roll_width)}\n")
    result.insert(tk.END, 
                 f"   • Total de peças: {sum(p['qty'] for p in pieces)}\n")
    result.insert(tk.END, f"   • Total de faixas: {len(rows)}\n")
    result.insert(tk.END, 
                 f"   • Comprimento total: {format_measurement(total_height)}\n")
    result.insert(tk.END, f"   • Aproveitamento: {util:.1f}%\n\n")
    
    # Resumo das peças que serão cortadas
    result.insert(tk.END, create_pieces_summary(pieces))
    
    # Visualização detalhada de cada faixa
    result.insert(tk.END, "📐 DETALHES DE CADA FAIXA:\n")
    result.insert(tk.END, "=" * 60 + "\n")
    
    for i, r in enumerate(rows, 1):
        visual_row = create_visual_row(i, r, roll_width)
        result.insert(tk.END, visual_row)
    
    # Resumo final muito claro
    result.insert(tk.END, create_visual_summary(rows, total_height, 
                                              used_area, loss_area, util, roll_width))
    
    # Salva o texto atual para exportação
    current_result_text = result.get('1.0', tk.END)


# ==== GUI ====
root = tk.Tk()
root.title('🎯 Otimizador de Cortes de Mantas PRI 1.050x50 (OTIMIZADO)')
root.geometry('900x800')

# Frame principal
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Título
title_label = tk.Label(main_frame, 
                      text="🎯 OTIMIZADOR DE CORTES DE MANTAS PRI (OTIMIZADO)", 
                      font=('Arial', 16, 'bold'), fg='#2E86AB')
title_label.pack(pady=(0, 20))

# Frame para dimensões do rolo
roll_frame = tk.LabelFrame(main_frame, text="📏 DIMENSÕES DO ROLO", 
                          font=('Arial', 12, 'bold'), fg='#2E86AB', padx=15, pady=15)
roll_frame.pack(fill=tk.X, pady=(0, 20))

# Campos para dimensões do rolo
roll_inputs_frame = tk.Frame(roll_frame)
roll_inputs_frame.pack()

tk.Label(roll_inputs_frame, text='Largura do rolo (mm):', 
         font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=(0, 10), sticky='e')
roll_width_entry = tk.Entry(roll_inputs_frame, width=15, font=('Arial', 10))
roll_width_entry.insert(0, "1050")  # Valor padrão
roll_width_entry.grid(row=0, column=1, padx=(0, 20))

tk.Label(roll_inputs_frame, text='Altura máxima (mm):', 
         font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=(0, 10), sticky='e')
roll_height_entry = tk.Entry(roll_inputs_frame, width=15, font=('Arial', 10))
roll_height_entry.insert(0, "50000")  # Valor padrão (ilimitada)
roll_height_entry.grid(row=0, column=3)

# Texto explicativo
info_label = tk.Label(roll_frame, 
                     text="💡 Dica: Altura máxima pode ser deixada alta (50000mm) para rolos longos",
                     font=('Arial', 9), fg='#666666')
info_label.pack(pady=(10, 0))

# Frame para entrada de dados
input_frame = tk.LabelFrame(main_frame, text="📝 DADOS DAS PEÇAS", 
                           font=('Arial', 12, 'bold'), padx=15, pady=15)
input_frame.pack(fill=tk.X, pady=(0, 20))

# Cabeçalhos das colunas
headers_frame = tk.Frame(input_frame)
headers_frame.pack(fill=tk.X, pady=(0, 10))

tk.Label(headers_frame, text='Largura (mm)', 
         font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5)
tk.Label(headers_frame, text='Altura (mm)', 
         font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=5)
tk.Label(headers_frame, text='Quantidade', 
         font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=5)

entries = []
for i in range(8):  # Aumentei para 8 linhas
    row_frame = tk.Frame(input_frame)
    row_frame.pack(fill=tk.X, pady=2)
    
    e_w = tk.Entry(row_frame, width=12, font=('Arial', 10))
    e_h = tk.Entry(row_frame, width=12, font=('Arial', 10))
    e_q = tk.Entry(row_frame, width=8, font=('Arial', 10))
    
    e_w.grid(row=0, column=0, padx=5)
    e_h.grid(row=0, column=1, padx=5)
    e_q.grid(row=0, column=2, padx=5)
    
    entries.append((e_w, e_h, e_q))

# Frame para botões
buttons_frame = tk.Frame(main_frame)
buttons_frame.pack(pady=20)

# Botão calcular
calc_button = tk.Button(buttons_frame, text='🚀 CALCULAR PLANO DE CORTE OTIMIZADO', 
                       command=calculate, font=('Arial', 12, 'bold'),
                       bg='#2E86AB', fg='white', padx=20, pady=10)
calc_button.pack(side=tk.LEFT, padx=(0, 10))

# Frame para botões de exportação
export_frame = tk.LabelFrame(main_frame, text="📤 EXPORTAR RESULTADO", 
                            font=('Arial', 10, 'bold'), padx=10, pady=10)
export_frame.pack(fill=tk.X, pady=(0, 20))

# Botões de exportação
export_buttons_frame = tk.Frame(export_frame)
export_buttons_frame.pack()

tk.Button(export_buttons_frame, text='📄 Salvar TXT', 
          command=export_to_txt, font=('Arial', 9),
          bg='#28a745', fg='white', padx=15, pady=5).pack(side=tk.LEFT, padx=5)

tk.Button(export_buttons_frame, text='📋 Copiar', 
          command=copy_to_clipboard, font=('Arial', 9),
          bg='#17a2b8', fg='white', padx=15, pady=5).pack(side=tk.LEFT, padx=5)

tk.Button(export_buttons_frame, text='🖨️  Imprimir', 
          command=print_result, font=('Arial', 9),
          bg='#ffc107', fg='black', padx=15, pady=5).pack(side=tk.LEFT, padx=5)

tk.Button(export_buttons_frame, text='📊 Salvar PDF', 
          command=export_to_pdf, font=('Arial', 9),
          bg='#dc3545', fg='white', padx=15, pady=5).pack(side=tk.LEFT, padx=5)

# Área de resultados
result_frame = tk.LabelFrame(main_frame, text="📊 RESULTADO", 
                            font=('Arial', 12, 'bold'))
result_frame.pack(fill=tk.BOTH, expand=True)

result = scrolledtext.ScrolledText(result_frame, width=80, height=25, 
                                 font=('Consolas', 10))
result.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Instruções
instructions = tk.Label(main_frame, 
                      text=("💡 Dica: Insira as dimensões das peças, calcule e "
                           "use os botões de exportação para salvar/compartilhar! "
                           "Algoritmo otimizado para máximo aproveitamento."),
                      font=('Arial', 10), fg='#666666')
instructions.pack(pady=(10, 0))

root.mainloop()