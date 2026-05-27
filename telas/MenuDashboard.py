import sqlite3
import customtkinter as ctk
from tkinter import ttk
import time
from datetime import datetime, timedelta

# Paleta de Cores
FUNDO = "#F8FAFC"
MENU_LATERAL = "#E2E8F0"
CARDS = "#FFFFFF"
BOTOES = "#2563EB"
BOTOES_HOVER = "#1D4ED8"
BOTAO_SUCESSO = "#16A34A"
BOTAO_ERRO = "#DC2626"
BOTAO_ALERTA = "#D97706"
TEXTO = "#0F172A"
TEXTO_SECUNDARIO = "#475569"
DIVISORIA = "#E2E8F0"
SUCESSO = "#22C55E"
ERRO = "#EF4444"
AVISO = "#F59E0B"

# ==================
# Funções de consulta
# ==================

def _conn():
    return sqlite3.connect("banco.db")

def get_total_animais():
    with _conn() as c:
        return c.execute("SELECT COUNT(*) FROM animais WHERE ativo=1").fetchone()[0]

def get_animais_por_tipo():
    with _conn() as c:
        return c.execute("""
            SELECT tipo, COUNT(*) FROM animais
            WHERE ativo=1 GROUP BY tipo ORDER BY COUNT(*) DESC
        """).fetchall()

def get_animais_por_status():
    with _conn() as c:
        return c.execute("""
            SELECT status, COUNT(*) FROM animais
            WHERE ativo=1 GROUP BY status
        """).fetchall()

def get_total_maquinas():
    with _conn() as c:
        return c.execute("SELECT COUNT(*) FROM maquinas").fetchone()[0]

def get_maquinas_por_status():
    with _conn() as c:
        return c.execute("""
            SELECT status, COUNT(*) FROM maquinas GROUP BY status
        """).fetchall()

def get_total_funcionarios():
    with _conn() as c:
        return c.execute("SELECT COUNT(*) FROM funcionarios WHERE ativo=1").fetchone()[0]

def get_itens_estoque_baixo():
    with _conn() as c:
        return c.execute("""
            SELECT nome, quantidade, estoque_minimo FROM estoque
            WHERE quantidade <= estoque_minimo
            ORDER BY (estoque_minimo - quantidade) DESC LIMIT 5
        """).fetchall()

def get_total_estoque():
    with _conn() as c:
        return c.execute("SELECT COUNT(*) FROM estoque").fetchone()[0]

def get_movimentacoes_recentes():
    with _conn() as c:
        return c.execute("""
            SELECT e.nome, m.tipo, m.quantidade, m.data_movimentacao
            FROM movimentacoes_estoque m
            JOIN estoque e ON e.id = m.item_id
            ORDER BY m.data_movimentacao DESC LIMIT 5
        """).fetchall()

def get_producao_leite_7dias():
    with _conn() as c:
        resultado = []
        for i in range(6, -1, -1):
            dia = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            label = (datetime.now() - timedelta(days=i)).strftime("%d/%m")
            total = c.execute(
                "SELECT COALESCE(SUM(litros),0) FROM producao_leite WHERE data_producao=?", (dia,)
            ).fetchone()[0]
            resultado.append((label, float(total)))
        return resultado

def get_pesagens_recentes():
    with _conn() as c:
        return c.execute("""
            SELECT a.nome, p.peso, strftime('%d/%m/%Y', p.data_pesagem)
            FROM pesagens p JOIN animais a ON a.id = p.animal_id
            ORDER BY p.data_pesagem DESC LIMIT 5
        """).fetchall()

# ===========
# Canvas util
# ===========

def desenhar_barra_horizontal(canvas, x, y, largura, altura, valor, maximo, cor, bg="#E2E8F0"):
    canvas.create_rectangle(x, y, x + largura, y + altura, fill=bg, outline="")
    if maximo > 0:
        preench = int((valor / maximo) * largura)
        if preench > 0:
            canvas.create_rectangle(x, y, x + preench, y + altura, fill=cor, outline="")

def desenhar_grafico_linha(canvas, dados, x0, y0, largura, altura, cor="#2563EB"):
    """Desenha gráfico de linha simples no canvas."""
    if not dados or len(dados) < 2:
        canvas.create_text(x0 + largura // 2, y0 + altura // 2,
                           text="Sem dados", fill=TEXTO_SECUNDARIO, font=("Segoe UI", 10))
        return

    valores = [d[1] for d in dados]
    labels  = [d[0] for d in dados]
    maximo  = max(valores) if max(valores) > 0 else 1
    minimo  = 0

    pad = 10
    gx0, gx1 = x0 + pad, x0 + largura - pad
    gy0, gy1 = y0 + pad, y0 + altura - pad

    n = len(dados)
    step = (gx1 - gx0) / (n - 1)

    def px(i): return gx0 + i * step
    def py(v): return gy1 - ((v - minimo) / (maximo - minimo)) * (gy1 - gy0)

    # Área preenchida
    pontos_area = [gx0, gy1]
    for i, v in enumerate(valores):
        pontos_area += [px(i), py(v)]
    pontos_area += [gx1, gy1]
    canvas.create_polygon(pontos_area, fill="#DBEAFE", outline="")

    # Linha
    for i in range(n - 1):
        canvas.create_line(px(i), py(valores[i]), px(i+1), py(valores[i+1]),
                           fill=cor, width=2, smooth=True)

    # Pontos e labels
    for i, (label, v) in enumerate(zip(labels, valores)):
        canvas.create_oval(px(i)-4, py(v)-4, px(i)+4, py(v)+4, fill=cor, outline="white", width=1)
        canvas.create_text(px(i), gy1 + 12, text=label,
                           fill=TEXTO_SECUNDARIO, font=("Segoe UI", 8), anchor="n")
        if v > 0:
            canvas.create_text(px(i), py(v) - 10, text=f"{v:.1f}",
                               fill=TEXTO, font=("Segoe UI", 8, "bold"))


# ===========
# Tela
# ===========

class MenuDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color=FUNDO)
        self.controller = controller
        self.configure(fg_color="transparent")

        # Topo
        topo = ctk.CTkFrame(self, fg_color=MENU_LATERAL, corner_radius=0, height=75)
        topo.pack(fill="x")
        topo.pack_propagate(False)

        ctk.CTkLabel(topo, text="Dashboard Analítico", fg_color="transparent",
                     font=("Segoe UI", 20, "bold"), text_color=TEXTO
                     ).place(anchor="center", relx=0.5, rely=0.5)

        data_label = ctk.CTkLabel(topo, text=time.strftime("%d/%m/%Y  %H:%M"),
                                  fg_color="transparent", font=("Segoe UI", 13),
                                  text_color=TEXTO_SECUNDARIO)
        data_label.place(relx=0.97, rely=0.5, anchor="e")

        # Botão atualizar
        ctk.CTkButton(topo, text="↺  Atualizar", font=("Segoe UI", 12, "bold"),
                      fg_color=BOTOES, hover_color=BOTOES_HOVER, text_color="white",
                      width=110, height=32,
                      command=self.atualizar_tudo
                      ).place(relx=0.85, rely=0.5, anchor="e")

        # Scroll
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.scroll.pack(fill="both", expand=True, padx=0, pady=0)
        self.scroll.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self._construir()
        print("RELATÓRIO: Dashboard analítico carregado.")

    # ----------------
    def _construir(self):
        self._linha_kpis()
        self._linha_graficos()
        self._linha_tabelas()

    def atualizar_tudo(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()
        self._construir()

    # ----------------
    # KPIs
    # ----------------
    def _linha_kpis(self):
        kpi_frame = ctk.CTkFrame(self.scroll, fg_color="transparent", corner_radius=0)
        kpi_frame.pack(fill="x", padx=20, pady=(20, 5))
        kpi_frame.grid_columnconfigure((0,1,2,3), weight=1)

        animais      = get_total_animais()
        maquinas     = get_total_maquinas()
        funcionarios = get_total_funcionarios()
        estoque_low  = len(get_itens_estoque_baixo())

        kpis = [
            ("🐄  Animais Ativos",     str(animais),      BOTOES,       "#EFF6FF"),
            ("⚙️  Máquinas",           str(maquinas),     BOTAO_SUCESSO,"#F0FDF4"),
            ("👷  Funcionários",        str(funcionarios), BOTAO_ALERTA, "#FFFBEB"),
            ("⚠️  Estoque Crítico",    str(estoque_low),  BOTAO_ERRO,   "#FEF2F2"),
        ]

        for col, (titulo, valor, cor, bg) in enumerate(kpis):
            card = ctk.CTkFrame(kpi_frame, fg_color=CARDS, corner_radius=12,
                                border_width=1, border_color=DIVISORIA)
            card.grid(row=0, column=col, padx=8, pady=5, sticky="ew")

            barra_cor = ctk.CTkFrame(card, fg_color=cor, height=4, corner_radius=0)
            barra_cor.pack(fill="x")

            ctk.CTkLabel(card, text=titulo, font=("Segoe UI", 12),
                         text_color=TEXTO_SECUNDARIO, fg_color="transparent"
                         ).pack(pady=(12, 0), padx=16, anchor="w")

            ctk.CTkLabel(card, text=valor, font=("Segoe UI", 36, "bold"),
                         text_color=cor, fg_color="transparent"
                         ).pack(pady=(0, 14), padx=16, anchor="w")

    # ----------------
    # Gráficos
    # ----------------
    def _linha_graficos(self):
        graf_frame = ctk.CTkFrame(self.scroll, fg_color="transparent", corner_radius=0)
        graf_frame.pack(fill="x", padx=20, pady=5)
        graf_frame.grid_columnconfigure((0, 1), weight=1)

        # — Animais por tipo —
        card_tipo = self._card_titulo(graf_frame, "Animais por Tipo", 0, 0)
        self._grafico_barras_animais_tipo(card_tipo)

        # — Produção de Leite 7 dias —
        card_leite = self._card_titulo(graf_frame, "Produção de Leite — 7 dias (L)", 0, 1)
        self._grafico_leite(card_leite)

    def _card_titulo(self, parent, titulo, row, col, padx=8, pady=5):
        card = ctk.CTkFrame(parent, fg_color=CARDS, corner_radius=12,
                            border_width=1, border_color=DIVISORIA)
        card.grid(row=row, column=col, padx=padx, pady=pady, sticky="nsew")
        ctk.CTkLabel(card, text=titulo, font=("Segoe UI", 13, "bold"),
                     text_color=TEXTO, fg_color="transparent"
                     ).pack(anchor="w", padx=16, pady=(14, 6))
        sep = ctk.CTkFrame(card, fg_color=DIVISORIA, height=1, corner_radius=0)
        sep.pack(fill="x", padx=16, pady=(0, 8))
        return card

    def _grafico_barras_animais_tipo(self, parent):
        dados = get_animais_por_tipo()
        if not dados:
            ctk.CTkLabel(parent, text="Nenhum dado disponível",
                         font=("Segoe UI", 12), text_color=TEXTO_SECUNDARIO
                         ).pack(pady=30)
            return

        maximo = max(v for _, v in dados) if dados else 1
        cores_barras = ["#2563EB", "#16A34A", "#D97706", "#DC2626", "#7C3AED", "#0891B2"]

        inner = ctk.CTkFrame(parent, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=(0, 14))

        for i, (tipo, qtd) in enumerate(dados):
            row_frame = ctk.CTkFrame(inner, fg_color="transparent")
            row_frame.pack(fill="x", pady=4)

            ctk.CTkLabel(row_frame, text=str(tipo or "—"), font=("Segoe UI", 12),
                         text_color=TEXTO, width=80, anchor="w"
                         ).pack(side="left")

            barra_bg = ctk.CTkFrame(row_frame, fg_color="#E2E8F0", height=22,
                                    corner_radius=4)
            barra_bg.pack(side="left", fill="x", expand=True, padx=(8, 8))

            pct = qtd / maximo if maximo > 0 else 0
            cor = cores_barras[i % len(cores_barras)]

            barra_fill = ctk.CTkFrame(barra_bg, fg_color=cor, height=22, corner_radius=4)
            barra_fill.place(relwidth=pct, relheight=1.0)

            ctk.CTkLabel(row_frame, text=str(qtd), font=("Segoe UI", 12, "bold"),
                         text_color=TEXTO, width=35, anchor="e"
                         ).pack(side="left")

    def _grafico_leite(self, parent):
        import tkinter as tk
        dados = get_producao_leite_7dias()

        canvas_frame = ctk.CTkFrame(parent, fg_color="transparent")
        canvas_frame.pack(fill="x", padx=16, pady=(0, 14))

        canvas = tk.Canvas(canvas_frame, height=160, bg=CARDS, highlightthickness=0)
        canvas.pack(fill="x")
        canvas.update_idletasks()

        def _draw(event=None):
            canvas.delete("all")
            w = canvas.winfo_width()
            desenhar_grafico_linha(canvas, dados, 10, 5, w - 20, 140, cor="#2563EB")

        canvas.bind("<Configure>", _draw)

    # ----------------
    # Tabelas
    # ----------------
    def _linha_tabelas(self):
        tab_frame = ctk.CTkFrame(self.scroll, fg_color="transparent", corner_radius=0)
        tab_frame.pack(fill="x", padx=20, pady=(5, 20))
        tab_frame.grid_columnconfigure((0, 1), weight=1)

        # — Estoque crítico —
        card_est = self._card_titulo(tab_frame, "⚠️  Itens com Estoque Crítico", 0, 0)
        self._tabela_estoque_critico(card_est)

        # — Pesagens recentes —
        card_pes = self._card_titulo(tab_frame, "⚖️  Pesagens Recentes", 0, 1)
        self._tabela_pesagens(card_pes)

        # — Máquinas por status —
        card_maq = self._card_titulo(tab_frame, "⚙️  Status das Máquinas", 1, 0)
        self._barras_maquinas(card_maq)

        # — Movimentações de Estoque —
        card_mov = self._card_titulo(tab_frame, "📦  Movimentações Recentes", 1, 1)
        self._tabela_movimentacoes(card_mov)

    def _tabela_estoque_critico(self, parent):
        dados = get_itens_estoque_baixo()
        if not dados:
            ctk.CTkLabel(parent, text="✅  Todos os itens estão OK!",
                         font=("Segoe UI", 12), text_color=BOTAO_SUCESSO
                         ).pack(pady=20)
            return

        inner = ctk.CTkFrame(parent, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=(0, 14))
        inner.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(inner, fg_color="#FEE2E2", corner_radius=6, height=28)
        header.pack(fill="x", pady=(0, 4))
        for col, (txt, w) in enumerate([("Item", 180), ("Atual", 70), ("Mínimo", 70)]):
            ctk.CTkLabel(header, text=txt, font=("Segoe UI", 11, "bold"),
                         text_color=BOTAO_ERRO, width=w, anchor="w"
                         ).pack(side="left", padx=8)

        for nome, qtd, minimo in dados:
            row = ctk.CTkFrame(inner, fg_color="transparent", height=28)
            row.pack(fill="x", pady=2)
            for txt, w in [(str(nome), 180), (f"{qtd:.1f}", 70), (f"{minimo:.1f}", 70)]:
                ctk.CTkLabel(row, text=txt, font=("Segoe UI", 11),
                             text_color=TEXTO, width=w, anchor="w"
                             ).pack(side="left", padx=8)

    def _tabela_pesagens(self, parent):
        dados = get_pesagens_recentes()
        if not dados:
            ctk.CTkLabel(parent, text="Nenhuma pesagem registrada.",
                         font=("Segoe UI", 12), text_color=TEXTO_SECUNDARIO
                         ).pack(pady=20)
            return

        inner = ctk.CTkFrame(parent, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=(0, 14))

        header = ctk.CTkFrame(inner, fg_color="#DBEAFE", corner_radius=6, height=28)
        header.pack(fill="x", pady=(0, 4))
        for col, (txt, w) in enumerate([("Animal", 180), ("Peso (kg)", 80), ("Data", 90)]):
            ctk.CTkLabel(header, text=txt, font=("Segoe UI", 11, "bold"),
                         text_color=BOTOES, width=w, anchor="w"
                         ).pack(side="left", padx=8)

        for nome, peso, data in dados:
            row = ctk.CTkFrame(inner, fg_color="transparent", height=28)
            row.pack(fill="x", pady=2)
            for txt, w in [(str(nome), 180), (f"{peso:.1f}", 80), (str(data), 90)]:
                ctk.CTkLabel(row, text=txt, font=("Segoe UI", 11),
                             text_color=TEXTO, width=w, anchor="w"
                             ).pack(side="left", padx=8)

    def _barras_maquinas(self, parent):
        dados = get_maquinas_por_status()
        if not dados:
            ctk.CTkLabel(parent, text="Nenhuma máquina cadastrada.",
                         font=("Segoe UI", 12), text_color=TEXTO_SECUNDARIO
                         ).pack(pady=20)
            return

        total = sum(v for _, v in dados)
        cores_status = {
            "ativo": BOTAO_SUCESSO, "Ativo": BOTAO_SUCESSO,
            "manutenção": BOTAO_ALERTA, "Manutenção": BOTAO_ALERTA,
            "inativo": BOTAO_ERRO, "Inativo": BOTAO_ERRO,
        }

        inner = ctk.CTkFrame(parent, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=(0, 14))

        for status, qtd in dados:
            cor = cores_status.get(status, BOTOES)
            row_frame = ctk.CTkFrame(inner, fg_color="transparent")
            row_frame.pack(fill="x", pady=4)

            ctk.CTkLabel(row_frame, text=str(status or "—"), font=("Segoe UI", 12),
                         text_color=TEXTO, width=90, anchor="w"
                         ).pack(side="left")

            barra_bg = ctk.CTkFrame(row_frame, fg_color="#E2E8F0", height=20, corner_radius=4)
            barra_bg.pack(side="left", fill="x", expand=True, padx=(8, 8))

            pct = qtd / total if total > 0 else 0
            barra_fill = ctk.CTkFrame(barra_bg, fg_color=cor, height=20, corner_radius=4)
            barra_fill.place(relwidth=pct, relheight=1.0)

            ctk.CTkLabel(row_frame, text=f"{qtd}  ({int(pct*100)}%)",
                         font=("Segoe UI", 11, "bold"), text_color=TEXTO, width=70, anchor="e"
                         ).pack(side="left")

    def _tabela_movimentacoes(self, parent):
        dados = get_movimentacoes_recentes()
        if not dados:
            ctk.CTkLabel(parent, text="Nenhuma movimentação registrada.",
                         font=("Segoe UI", 12), text_color=TEXTO_SECUNDARIO
                         ).pack(pady=20)
            return

        inner = ctk.CTkFrame(parent, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=(0, 14))

        header = ctk.CTkFrame(inner, fg_color="#F0FDF4", corner_radius=6, height=28)
        header.pack(fill="x", pady=(0, 4))
        for txt, w in [("Item", 150), ("Tipo", 70), ("Qtd", 60), ("Data", 90)]:
            ctk.CTkLabel(header, text=txt, font=("Segoe UI", 11, "bold"),
                         text_color=BOTAO_SUCESSO, width=w, anchor="w"
                         ).pack(side="left", padx=8)

        for nome, tipo, qtd, data in dados:
            cor_tipo = BOTAO_SUCESSO if tipo == "Entrada" else BOTAO_ERRO
            data_fmt = data[:10] if data else "—"
            try:
                d = datetime.strptime(data_fmt, "%Y-%m-%d")
                data_fmt = d.strftime("%d/%m/%Y")
            except:
                pass

            row = ctk.CTkFrame(inner, fg_color="transparent", height=28)
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(row, text=str(nome), font=("Segoe UI", 11),
                         text_color=TEXTO, width=150, anchor="w"
                         ).pack(side="left", padx=8)
            ctk.CTkLabel(row, text=str(tipo), font=("Segoe UI", 11, "bold"),
                         text_color=cor_tipo, width=70, anchor="w"
                         ).pack(side="left")
            ctk.CTkLabel(row, text=f"{float(qtd):.1f}", font=("Segoe UI", 11),
                         text_color=TEXTO, width=60, anchor="w"
                         ).pack(side="left")
            ctk.CTkLabel(row, text=data_fmt, font=("Segoe UI", 11),
                         text_color=TEXTO_SECUNDARIO, width=90, anchor="w"
                         ).pack(side="left")