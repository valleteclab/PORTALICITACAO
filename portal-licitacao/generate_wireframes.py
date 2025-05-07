#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

# Configurações
OUTPUT_DIR = os.path.expanduser("~/portal-licitacao/prototipos")
WIDTH = 1200
HEIGHT = 800
BG_COLOR = (245, 245, 245)
HEADER_COLOR = (25, 118, 210)
SIDEBAR_COLOR = (240, 240, 240)
TEXT_COLOR = (33, 33, 33)
ACCENT_COLOR = (25, 118, 210)
BUTTON_COLOR = (25, 118, 210)
BUTTON_TEXT_COLOR = (255, 255, 255)
CARD_COLOR = (255, 255, 255)
BORDER_COLOR = (200, 200, 200)
TABLE_HEADER_COLOR = (240, 240, 240)
TABLE_ROW_ALT_COLOR = (250, 250, 250)

# Criar diretório de saída se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Carregar fontes
try:
    # Tentar carregar fontes do sistema
    title_font = ImageFont.truetype("Arial", 24)
    subtitle_font = ImageFont.truetype("Arial", 18)
    regular_font = ImageFont.truetype("Arial", 14)
    small_font = ImageFont.truetype("Arial", 12)
except IOError:
    # Fallback para fonte padrão
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    regular_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

def draw_rounded_rectangle(draw, xy, radius=10, fill=None, outline=None):
    """Desenha um retângulo com cantos arredondados"""
    x1, y1, x2, y2 = xy
    draw.rectangle((x1 + radius, y1, x2 - radius, y2), fill=fill, outline=outline)
    draw.rectangle((x1, y1 + radius, x2, y2 - radius), fill=fill, outline=outline)
    draw.pieslice((x1, y1, x1 + 2 * radius, y1 + 2 * radius), 180, 270, fill=fill, outline=outline)
    draw.pieslice((x2 - 2 * radius, y1, x2, y1 + 2 * radius), 270, 360, fill=fill, outline=outline)
    draw.pieslice((x1, y2 - 2 * radius, x1 + 2 * radius, y2), 90, 180, fill=fill, outline=outline)
    draw.pieslice((x2 - 2 * radius, y2 - 2 * radius, x2, y2), 0, 90, fill=fill, outline=outline)
    if outline:
        draw.line((x1 + radius, y1, x2 - radius, y1), fill=outline)
        draw.line((x1 + radius, y2, x2 - radius, y2), fill=outline)
        draw.line((x1, y1 + radius, x1, y2 - radius), fill=outline)
        draw.line((x2, y1 + radius, x2, y2 - radius), fill=outline)

def draw_button(draw, xy, text, fill=BUTTON_COLOR, text_color=BUTTON_TEXT_COLOR, radius=5):
    """Desenha um botão com texto"""
    x1, y1, x2, y2 = xy
    draw_rounded_rectangle(draw, xy, radius=radius, fill=fill)
    text_width = draw.textlength(text, font=regular_font)
    text_x = x1 + (x2 - x1 - text_width) // 2
    text_y = y1 + (y2 - y1 - 14) // 2  # Aproximação da altura do texto
    draw.text((text_x, text_y), text, font=regular_font, fill=text_color)

def draw_input(draw, xy, placeholder="", value="", label=""):
    """Desenha um campo de entrada de texto"""
    x1, y1, x2, y2 = xy
    
    # Desenhar label se fornecido
    if label:
        draw.text((x1, y1 - 20), label, font=small_font, fill=TEXT_COLOR)
    
    # Desenhar campo
    draw.rectangle((x1, y1, x2, y2), fill=CARD_COLOR, outline=BORDER_COLOR)
    
    # Desenhar texto ou placeholder
    text = value if value else placeholder
    if text:
        draw.text((x1 + 10, y1 + (y2 - y1 - 14) // 2), text, 
                 font=regular_font, fill=TEXT_COLOR if value else (150, 150, 150))

def draw_select(draw, xy, options=[], selected=None, label=""):
    """Desenha um campo de seleção"""
    x1, y1, x2, y2 = xy
    
    # Desenhar label se fornecido
    if label:
        draw.text((x1, y1 - 20), label, font=small_font, fill=TEXT_COLOR)
    
    # Desenhar campo
    draw.rectangle((x1, y1, x2, y2), fill=CARD_COLOR, outline=BORDER_COLOR)
    
    # Desenhar texto selecionado ou primeiro item
    text = selected if selected else (options[0] if options else "Selecione...")
    draw.text((x1 + 10, y1 + (y2 - y1 - 14) // 2), text, 
             font=regular_font, fill=TEXT_COLOR)
    
    # Desenhar seta para baixo
    arrow_points = [(x2 - 20, y1 + (y2 - y1) // 2 - 5), 
                    (x2 - 10, y1 + (y2 - y1) // 2 + 5), 
                    (x2 - 30, y1 + (y2 - y1) // 2 + 5)]
    draw.polygon(arrow_points, fill=TEXT_COLOR)

def draw_checkbox(draw, xy, label="", checked=False):
    """Desenha uma caixa de seleção"""
    x1, y1, x2, y2 = xy
    
    # Desenhar caixa
    draw.rectangle((x1, y1, x2, y2), fill=CARD_COLOR, outline=BORDER_COLOR)
    
    # Desenhar marca de seleção se estiver marcado
    if checked:
        draw.line((x1 + 3, y1 + (y2 - y1) // 2, x1 + (x2 - x1) // 2, y2 - 3), fill=ACCENT_COLOR, width=2)
        draw.line((x1 + (x2 - x1) // 2, y2 - 3, x2 - 3, y1 + 3), fill=ACCENT_COLOR, width=2)
    
    # Desenhar label
    if label:
        draw.text((x2 + 10, y1 + (y2 - y1 - 14) // 2), label, font=regular_font, fill=TEXT_COLOR)

def draw_radio(draw, xy, label="", checked=False):
    """Desenha um botão de opção"""
    x, y = xy
    radius = 8
    
    # Desenhar círculo
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), 
                outline=BORDER_COLOR, fill=CARD_COLOR)
    
    # Desenhar ponto interno se estiver selecionado
    if checked:
        inner_radius = 4
        draw.ellipse((x - inner_radius, y - inner_radius, x + inner_radius, y + inner_radius), 
                    fill=ACCENT_COLOR)
    
    # Desenhar label
    if label:
        draw.text((x + radius + 10, y - 7), label, font=regular_font, fill=TEXT_COLOR)

def draw_table(draw, xy, headers, rows, row_height=40):
    """Desenha uma tabela com cabeçalho e linhas"""
    x1, y1, x2, y2 = xy
    col_width = (x2 - x1) // len(headers)
    
    # Desenhar cabeçalho
    draw.rectangle((x1, y1, x2, y1 + row_height), fill=TABLE_HEADER_COLOR, outline=BORDER_COLOR)
    for i, header in enumerate(headers):
        header_x = x1 + i * col_width + 10
        draw.text((header_x, y1 + (row_height - 14) // 2), header, font=regular_font, fill=TEXT_COLOR)
    
    # Desenhar linhas
    for j, row in enumerate(rows):
        row_y = y1 + (j + 1) * row_height
        # Alternar cores das linhas
        row_color = TABLE_ROW_ALT_COLOR if j % 2 == 1 else CARD_COLOR
        draw.rectangle((x1, row_y, x2, row_y + row_height), fill=row_color, outline=BORDER_COLOR)
        
        for i, cell in enumerate(row):
            cell_x = x1 + i * col_width + 10
            draw.text((cell_x, row_y + (row_height - 14) // 2), str(cell), font=regular_font, fill=TEXT_COLOR)

def draw_card(draw, xy, title="", content="", footer=""):
    """Desenha um card com título, conteúdo e rodapé"""
    x1, y1, x2, y2 = xy
    
    # Desenhar fundo do card
    draw_rounded_rectangle(draw, xy, fill=CARD_COLOR, outline=BORDER_COLOR)
    
    # Desenhar título
    if title:
        draw.text((x1 + 15, y1 + 15), title, font=subtitle_font, fill=TEXT_COLOR)
        draw.line((x1 + 10, y1 + 45, x2 - 10, y1 + 45), fill=BORDER_COLOR)
    
    # Desenhar conteúdo
    if content:
        content_y = y1 + 60 if title else y1 + 15
        # Quebrar texto em múltiplas linhas se necessário
        max_width = x2 - x1 - 30
        lines = textwrap.wrap(content, width=max_width // 7)  # Aproximação grosseira
        for i, line in enumerate(lines):
            draw.text((x1 + 15, content_y + i * 20), line, font=regular_font, fill=TEXT_COLOR)
    
    # Desenhar rodapé
    if footer:
        draw.line((x1 + 10, y2 - 45, x2 - 10, y2 - 45), fill=BORDER_COLOR)
        draw.text((x1 + 15, y2 - 30), footer, font=small_font, fill=TEXT_COLOR)

def draw_tabs(draw, xy, tabs, active_index=0):
    """Desenha uma barra de abas"""
    x1, y1, x2, y2 = xy
    tab_width = (x2 - x1) // len(tabs)
    
    for i, tab in enumerate(tabs):
        tab_x1 = x1 + i * tab_width
        tab_x2 = tab_x1 + tab_width
        
        # Desenhar fundo da aba
        if i == active_index:
            draw.rectangle((tab_x1, y1, tab_x2, y2), fill=CARD_COLOR, outline=BORDER_COLOR)
            draw.line((tab_x1, y2, tab_x2, y2), fill=ACCENT_COLOR, width=3)
        else:
            draw.rectangle((tab_x1, y1, tab_x2, y2), fill=BG_COLOR, outline=BORDER_COLOR)
        
        # Desenhar texto da aba
        text_width = draw.textlength(tab, font=regular_font)
        text_x = tab_x1 + (tab_width - text_width) // 2
        draw.text((text_x, y1 + (y2 - y1 - 14) // 2), tab, 
                 font=regular_font, fill=ACCENT_COLOR if i == active_index else TEXT_COLOR)

def draw_pagination(draw, xy, current_page=1, total_pages=5):
    """Desenha controles de paginação"""
    x1, y1, x2, y2 = xy
    width = x2 - x1
    
    # Desenhar botões de navegação
    button_width = 40
    button_height = 30
    
    # Botão anterior
    prev_button = (x1, y1, x1 + button_width, y1 + button_height)
    draw_button(draw, prev_button, "<", fill=CARD_COLOR, text_color=TEXT_COLOR)
    
    # Páginas
    page_width = 30
    pages_start_x = x1 + button_width + 10
    
    for i in range(1, min(total_pages + 1, 6)):
        page_x1 = pages_start_x + (i - 1) * (page_width + 5)
        page_x2 = page_x1 + page_width
        
        if i == current_page:
            draw_button(draw, (page_x1, y1, page_x2, y1 + button_height), str(i))
        else:
            draw_button(draw, (page_x1, y1, page_x2, y1 + button_height), str(i), 
                       fill=CARD_COLOR, text_color=TEXT_COLOR)
    
    # Botão próximo
    next_button = (x2 - button_width, y1, x2, y1 + button_height)
    draw_button(draw, next_button, ">", fill=CARD_COLOR, text_color=TEXT_COLOR)

def draw_search(draw, xy, placeholder="Buscar..."):
    """Desenha uma caixa de pesquisa"""
    x1, y1, x2, y2 = xy
    
    # Desenhar campo
    draw.rectangle((x1, y1, x2, y2), fill=CARD_COLOR, outline=BORDER_COLOR)
    
    # Desenhar ícone de lupa (simplificado)
    icon_x = x1 + 15
    icon_y = y1 + (y2 - y1) // 2
    draw.ellipse((icon_x - 5, icon_y - 5, icon_x + 5, icon_y + 5), outline=TEXT_COLOR)
    draw.line((icon_x + 4, icon_y + 4, icon_x + 10, icon_y + 10), fill=TEXT_COLOR, width=2)
    
    # Desenhar placeholder
    draw.text((icon_x + 15, y1 + (y2 - y1 - 14) // 2), placeholder, 
             font=regular_font, fill=(150, 150, 150))

def draw_notification(draw, xy, message, type="info"):
    """Desenha uma notificação"""
    x1, y1, x2, y2 = xy
    
    # Definir cor com base no tipo
    if type == "success":
        color = (76, 175, 80)
    elif type == "warning":
        color = (255, 152, 0)
    elif type == "error":
        color = (244, 67, 54)
    else:  # info
        color = (33, 150, 243)
    
    # Desenhar fundo
    draw_rounded_rectangle(draw, xy, fill=(color[0], color[1], color[2], 50), outline=color)
    
    # Desenhar ícone (simplificado)
    icon_x = x1 + 20
    icon_y = y1 + (y2 - y1) // 2
    
    if type == "info":
        draw.ellipse((icon_x - 8, icon_y - 8, icon_x + 8, icon_y + 8), outline=color)
        draw.text((icon_x - 2, icon_y - 10), "i", font=regular_font, fill=color)
    elif type == "success":
        draw.ellipse((icon_x - 8, icon_y - 8, icon_x + 8, icon_y + 8), outline=color)
        draw.line((icon_x - 4, icon_y, icon_x - 1, icon_y + 4), fill=color, width=2)
        draw.line((icon_x - 1, icon_y + 4, icon_x + 5, icon_y - 3), fill=color, width=2)
    elif type == "warning":
        draw.polygon([(icon_x, icon_y - 8), (icon_x + 8, icon_y + 8), (icon_x - 8, icon_y + 8)], outline=color)
        draw.text((icon_x - 2, icon_y - 5), "!", font=regular_font, fill=color)
    elif type == "error":
        draw.ellipse((icon_x - 8, icon_y - 8, icon_x + 8, icon_y + 8), outline=color)
        draw.line((icon_x - 4, icon_y - 4, icon_x + 4, icon_y + 4), fill=color, width=2)
        draw.line((icon_x + 4, icon_y - 4, icon_x - 4, icon_y + 4), fill=color, width=2)
    
    # Desenhar mensagem
    draw.text((icon_x + 20, y1 + (y2 - y1 - 14) // 2), message, font=regular_font, fill=TEXT_COLOR)

def draw_common_elements(img, title, is_logged_in=True):
    """Desenha elementos comuns a todas as telas"""
    draw = ImageDraw.Draw(img)
    
    # Fundo
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=BG_COLOR)
    
    # Cabeçalho
    draw.rectangle((0, 0, WIDTH, 60), fill=HEADER_COLOR)
    draw.text((20, 18), "Portal de Licitação", font=title_font, fill=(255, 255, 255))
    
    # Barra de navegação
    if is_logged_in:
        # Ícones de usuário e notificações
        draw.ellipse((WIDTH - 40, 15, WIDTH - 20, 35), outline=(255, 255, 255))
        draw.ellipse((WIDTH - 80, 15, WIDTH - 60, 35), outline=(255, 255, 255))
        
        # Barra lateral
        draw.rectangle((0, 60, 220, HEIGHT), fill=SIDEBAR_COLOR)
        
        # Itens do menu
        menu_items = [
            "Dashboard", "Licitações", "Contratos", 
            "Fornecedores", "Relatórios", "Configurações"
        ]
        
        for i, item in enumerate(menu_items):
            y = 100 + i * 50
            # Destacar item atual baseado no título
            if item.lower() in title.lower():
                draw.rectangle((0, y - 10, 220, y + 30), fill=ACCENT_COLOR)
                draw.text((20, y), item, font=regular_font, fill=(255, 255, 255))
            else:
                draw.text((20, y), item, font=regular_font, fill=TEXT_COLOR)
    
    # Título da página
    if is_logged_in:
        draw.text((240, 80), title, font=title_font, fill=TEXT_COLOR)
    else:
        draw.text((WIDTH // 2 - draw.textlength(title, font=title_font) // 2, 80), 
                 title, font=title_font, fill=TEXT_COLOR)
    
    return draw

def create_home_page():
    """Cria a página inicial do portal"""
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = draw_common_elements(img, "Portal de Licitação", is_logged_in=False)
    
    # Banner principal
    banner_rect = (100, 130, WIDTH - 100, 330)
    draw_rounded_rectangle(draw, banner_rect, fill=CARD_COLOR, outline=BORDER_COLOR)
    
    # Texto do banner
    banner_title = "Bem-vindo ao Portal de Licitação"
    draw.text((banner_rect[0] + 30, banner_rect[1] + 30), banner_title, font=title_font, fill=TEXT_COLOR)
    
    banner_text = "Plataforma completa para gerenciamento de processos licitatórios, desde o planejamento até a execução contratual, atendendo a todas as modalidades previstas na Lei nº 14.133/2021."
    wrapped_text = textwrap.wrap(banner_text, width=70)
    for i, line in enumerate(wrapped_text):
        draw.text((banner_rect[0] + 30, banner_rect[1] + 80 + i * 25), line, font=regular_font, fill=TEXT_COLOR)
    
    # Botões de acesso
    login_button = (banner_rect[0] + 30, banner_rect[1] + 180, banner_rect[0] + 180, banner_rect[1] + 220)
    draw_button(draw, login_button, "Acessar o Sistema")
    
    register_button = (banner_rect[0] + 200, banner_rect[1] + 180, banner_rect[0] + 350, banner_rect[1] + 220)
    draw_button(draw, register_button, "Cadastrar-se", fill=(76, 175, 80))
    
    # Cards de informações
    card_width = (WIDTH - 200) // 3 - 20
    card_height = 200
    
    # Card 1
    card1_rect = (100, 360, 100 + card_width, 360 + card_height)
    draw_card(draw, card1_rect, "Licitações Abertas", 
             "Acesse as licitações em andamento e envie suas propostas.", 
             "Ver todas >")
    
    # Card 2
    card2_rect = (100 + card_width + 20, 360, 100 + 2 * card_width + 20, 360 + card_height)
    draw_card(draw, card2_rect, "Contratos Vigentes", 
             "Consulte os contratos vigentes e suas informações.", 
             "Ver todos >")
    
    # Card 3
    card3_rect = (100 + 2 * card_width + 40, 360, 100 + 3 * card_width + 40, 360 + card_height)
    draw_card(draw, card3_rect, "Transparência", 
             "Acesse dados públicos sobre licitações e contratos.", 
             "Saiba mais >")
    
    # Rodapé
    draw.rectangle((0, HEIGHT - 60, WIDTH, HEIGHT), fill=(50, 50, 50))
    draw.text((20, HEIGHT - 40), "© 2025 Portal de Licitação - Todos os direitos reservados", 
             font=small_font, fill=(200, 200, 200))
    
    # Salvar imagem
    img.save(os.path.join(OUTPUT_DIR, "home.png"))

def create_login_page():
    """Cria a página de login"""
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = draw_common_elements(img, "Login / Cadastro", is_logged_in=False)
    
    # Card de login
    login_card = (WIDTH // 2 - 200, 150, WIDTH // 2 + 200, 550)
    draw_rounded_rectangle(draw, login_card, fill=CARD_COLOR, outline=BORDER_COLOR)
    
    # Título do card
    draw.text((login_card[0] + 30, login_card[1] + 30), "Acesso ao Sistema", 
             font=subtitle_font, fill=TEXT_COLOR)
    
    # Abas de login
    tabs_rect = (login_card[0] + 30, login_card[1] + 80, login_card[2] - 30, login_card[1] + 120)
    draw_tabs(draw, tabs_rect, ["Login", "Cadastro"], active_index=0)
    
    # Campos de login
    email_input = (login_card[0] + 30, login_card[1] + 160, login_card[2] - 30, login_card[1] + 200)
    draw_input(draw, email_input, placeholder="Email", label="Email")
    
    password_input = (login_card[0] + 30, login_card[1] + 240, login_card[2] - 30, login_card[1] + 280)
    draw_input(draw, password_input, placeholder="••••••••", label="Senha")
    
    # Checkbox "Lembrar-me"
    remember_checkbox = (login_card[0] + 30, login_card[1] + 310, login_card[0] + 50, login_card[1] + 330)
    draw_checkbox(draw, remember_checkbox, label="Lembrar-me")
    
    # Link "Esqueci minha senha"
    draw.text((login_card[2] - 150, login_card[1] + 320), "Esqueci minha senha", 
             font=small_font, fill=ACCENT_COLOR)
    
    # Botão de login
    login_button = (login_card[0] + 30, login_card[1] + 370, login_card[2] - 30, login_card[1] + 410)
    draw_button(draw, login_button, "Entrar")
    
    # Ou login com GOV.BR
    draw.text((login_card[0] + (login_card[2] - login_card[0]) // 2 - 50, login_card[1] + 440), 
             "Ou acesse com", font=small_font, fill=TEXT_COLOR)
    
    govbr_button = (login_card[0] + 30, login_card[1] + 470, login_card[2] - 30, login_card[1] + 510)
    draw_button(draw, govbr_button, "GOV.BR", fill=(0, 94, 162))
    
    # Salvar imagem
    img.save(os.path.join(OUTPUT_DIR, "login-cadastro.png"))

def create_dashboard_orgao():
    """Cria o dashboard para órgãos públicos"""
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = draw_common_elements(img, "Dashboard - Órgão Público")
    
    # Área de conteúdo
    content_area = (240, 120, WIDTH - 20, HEIGHT - 20)
    
    # Cards de resumo
    card_width = (content_area[2] - content_area[0]) // 4 - 15
    card_height = 100
    
    # Card 1 - Licitações Ativas
    card1_rect = (content_area[0], content_area[1], content_area[0] + card_width, content_area[1] + card_height)
    draw_card(draw, card1_rect, "Licitações Ativas", "12", "")
    
    # Card 2 - Contratos Vigentes
    card2_rect = (card1_rect[2] + 20, content_area[1], card1_rect[2] + 20 + card_width, content_area[1] + card_height)
    draw_card(draw, card2_rect, "Contratos Vigentes", "28", "")
    
    # Card 3 - Valor Contratado
    card3_rect = (card2_rect[2] + 20, content_area[1], card2_rect[2] + 20 + card_width, content_area[1] + card_height)
    draw_card(draw, card3_rect, "Valor Contratado", "R$ 1.245.678,90", "")
    
    # Card 4 - Economia Gerada
    card4_rect = (card3_rect[2] + 20, content_area[1], card3_rect[2] + 20 + card_width, content_area[1] + card_height)
    draw_card(draw, card4_rect, "Economia Gerada", "R$ 325.421,30", "")
    
    # Gráfico de licitações por modalidade (simulado)
    chart1_rect = (content_area[0], content_area[1] + card_height + 20, 
                  content_area[0] + (content_area[2] - content_area[0]) // 2 - 10, 
                  content_area[1] + card_height + 270)
    draw_card(draw, chart1_rect, "Licitações por Modalidade", "", "")
    
    # Desenhar gráfico de barras simulado
    chart_area = (chart1_rect[0] + 30, chart1_rect[1] + 50, chart1_rect[2] - 30, chart1_rect[3] - 30)
    bar_width = 40
    bar_spacing = 20
    bar_colors = [(25, 118, 210), (76, 175, 80), (255, 152, 0), (244, 67, 54)]
    
    # Dados simulados
    categories = ["Pregão", "Concorrência", "Concurso", "Leilão"]
    values = [8, 3, 1, 2]
    
    # Desenhar barras
    max_value = max(values)
    for i, (category, value) in enumerate(zip(categories, values)):
        bar_height = (chart_area[3] - chart_area[1]) * value / max_value
        bar_x = chart_area[0] + i * (bar_width + bar_spacing)
        bar_y = chart_area[3] - bar_height
        
        # Barra
        draw.rectangle((bar_x, bar_y, bar_x + bar_width, chart_area[3]), 
                      fill=bar_colors[i % len(bar_colors)])
        
        # Valor
        draw.text((bar_x + bar_width // 2 - 5, bar_y - 20), str(value), 
                 font=small_font, fill=TEXT_COLOR)
        
        # Categoria
        draw.text((bar_x, chart_area[3] + 10), category, 
                 font=small_font, fill=TEXT_COLOR)
    
    # Gráfico de licitações por situação (simulado)
    chart2_rect = (chart1_rect[2] + 20, content_area[1] + card_height + 20, 
                  content_area[2], 
                  content_area[1] + card_height + 270)
    draw_card(draw, chart2_rect, "Licitações por Situação", "", "")
    
    # Desenhar gráfico de pizza simulado
    center_x = (chart2_rect[0] + chart2_rect[2]) // 2
    center_y = (chart2_rect[1] + chart2_rect[3]) // 2
    radius = 80
    
    # Dados simulados
    statuses = ["Em Andamento", "Concluídas", "Suspensas", "Canceladas"]
    percentages = [40, 35, 15, 10]
    colors = [(25, 118, 210), (76, 175, 80), (255, 152, 0), (244, 67, 54)]
    
    # Desenhar fatias
    start_angle = 0
    for i, (status, percentage, color) in enumerate(zip(statuses, percentages, colors)):
        end_angle = start_angle + 360 * percentage / 100
        draw.pieslice((center_x - radius, center_y - radius, center_x + radius, center_y + radius), 
                     start_angle, end_angle, fill=color)
        
        # Legenda
        legend_x = chart2_rect[0] + 30
        legend_y = chart2_rect[3] - 80 + i * 20
        
        draw.rectangle((legend_x, legend_y, legend_x + 15, legend_y + 15), fill=color)
        draw.text((legend_x + 25, legend_y), f"{status} ({percentage}%)", 
                 font=small_font, fill=TEXT_COLOR)
        
        start_angle = end_angle
    
    # Tabela de licitações recentes
    table_rect = (content_area[0], chart1_rect[3] + 20, content_area[2], HEIGHT - 40)
    draw_card(draw, table_rect, "Licitações Recentes", "", "")
    
    # Desenhar tabela
    table_area = (table_rect[0] + 20, table_rect[1] + 50, table_rect[2] - 20, table_rect[3] - 20)
    headers = ["Nº", "Modalidade", "Objeto", "Valor Estimado", "Situação", "Ações"]
    
    rows = [
        ["001/2025", "Pregão", "Aquisição de material de escritório", "R$ 45.000,00", "Em Andamento", ""],
        ["002/2025", "Concorrência", "Construção de escola municipal", "R$ 1.200.000,00", "Publicada", ""],
        ["003/2025", "Pregão", "Serviços de limpeza", "R$ 120.000,00", "Em Análise", ""],
        ["004/2025", "Leilão", "Venda de veículos usados", "R$ 80.000,00", "Concluída", ""]
    ]
    
    draw_table(draw, table_area, headers, rows)
    
    # Adicionar botões de ação na última coluna
    button_y = table_area[1] + 20
    for i in range(len(rows)):
        button_x = table_area[0] + 5 * (table_area[2] - table_area[0]) // 6 + 10
        button_rect = (button_x, button_y + i * 40 + 10, button_x + 60, button_y + i * 40 + 30)
        draw_button(draw, button_rect, "Ver", fill=ACCENT_COLOR, text_color=BUTTON_TEXT_COLOR, radius=3)
    
    # Paginação
    pagination_rect = (table_area[0], table_area[3] + 10, table_area[2], table_area[3] + 40)
    draw_pagination(draw, pagination_rect)
    
    # Salvar imagem
    img.save(os.path.join(OUTPUT_DIR, "dashboard-orgao.png"))

def create_dashboard_fornecedor():
    """Cria o dashboard para fornecedores"""
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = draw_common_elements(img, "Dashboard - Fornecedor")
    
    # Área de conteúdo
    content_area = (240, 120, WIDTH - 20, HEIGHT - 20)
    
    # Cards de resumo
    card_width = (content_area[2] - content_area[0]) // 4 - 15
    card_height = 100
    
    # Card 1 - Licitações Participando
    card1_rect = (content_area[0], content_area[1], content_area[0] + card_width, content_area[1] + card_height)
    draw_card(draw, card1_rect, "Participando", "5", "")
    
    # Card 2 - Contratos Ativos
    card2_rect = (card1_rect[2] + 20, content_area[1], card1_rect[2] + 20 + card_width, content_area[1] + card_height)
    draw_card(draw, card2_rect, "Contratos Ativos", "3", "")
    
    # Card 3 - Valor Contratado
    card3_rect = (card2_rect[2] + 20, content_area[1], card2_rect[2] + 20 + card_width, content_area[1] + card_height)
    draw_card(draw, card3_rect, "Valor Contratado", "R$ 245.678,90", "")
    
    # Card 4 - Taxa de Sucesso
    card4_rect = (card3_rect[2] + 20, content_area[1], card3_rect[2] + 20 + card_width, content_area[1] + card_height)
    draw_card(draw, card4_rect, "Taxa de Sucesso", "65%", "")
    
    # Alertas e notificações
    alerts_rect = (content_area[0], content_area[1] + card_height + 20, 
                  content_area[0] + (content_area[2] - content_area[0]) // 2 - 10, 
                  content_area[1] + card_height + 220)
    draw_card(draw, alerts_rect, "Alertas e Notificações", "", "")
    
    # Desenhar notificações
    notification1_rect = (alerts_rect[0] + 20, alerts_rect[1] + 50, alerts_rect[2] - 20, alerts_rect[1] + 90)
    draw_notification(draw, notification1_rect, "Nova licitação disponível: Pregão 005/2025", "info")
    
    notification2_rect = (alerts_rect[0] + 20, alerts_rect[1] + 100, alerts_rect[2] - 20, alerts_rect[1] + 140)
    draw_notification(draw, notification2_rect, "Proposta aceita para Pregão 002/2025", "success")
    
    notification3_rect = (alerts_rect[0] + 20, alerts_rect[1] + 150, alerts_rect[2] - 20, alerts_rect[1] + 190)
    draw_notification(draw, notification3_rect, "Contrato 003/2025 próximo do vencimento", "warning")
    
    # Oportunidades de licitação
    opportunities_rect = (alerts_rect[2] + 20, content_area[1] + card_height + 20, 
                         content_area[2], 
                         content_area[1] + card_height + 220)
    draw_card(draw, opportunities_rect, "Oportunidades de Licitação", "", "Ver todas >")
    
    # Lista de oportunidades
    opportunities = [
        "Pregão 005/2025 - Material de Informática - R$ 80.000,00",
        "Concorrência 003/2025 - Serviços de Manutenção - R$ 150.000,00",
        "Pregão 006/2025 - Mobiliário - R$ 65.000,00"
    ]
    
    for i, opportunity in enumerate(opportunities):
        y = opportunities_rect[1] + 60 + i * 40
        draw.text((opportunities_rect[0] + 30, y), opportunity, font=regular_font, fill=TEXT_COLOR)
        
        # Botão "Participar"
        button_rect = (opportunities_rect[2] - 120, y - 5, opportunities_rect[2] - 30, y + 25)
        draw_button(draw, button_rect, "Participar", fill=(76, 175, 80))
    
    # Tabela de licitações em andamento
    table_rect = (content_area[0], alerts_rect[3] + 20, content_area[2], HEIGHT - 40)
    draw_card(draw, table_rect, "Licitações em Andamento", "", "")
    
    # Desenhar tabela
    table_area = (table_rect[0] + 20, table_rect[1] + 50, table_rect[2] - 20, table_rect[3] - 20)
    headers = ["Nº", "Órgão", "Objeto", "Valor Proposto", "Situação", "Ações"]
    
    rows = [
        ["001/2025", "Prefeitura", "Material de escritório", "R$ 42.500,00", "Em Disputa", ""],
        ["002/2025", "Câmara", "Serviços de TI", "R$ 95.000,00", "Em Análise", ""],
        ["003/2025", "Prefeitura", "Serviços de limpeza", "R$ 118.000,00", "Habilitação", ""],
        ["004/2025", "Secretaria", "Equipamentos", "R$ 65.000,00", "Adjudicada", ""]
    ]
    
    draw_table(draw, table_area, headers, rows)
    
    # Adicionar botões de ação na última coluna
    button_y = table_area[1] + 20
    for i in range(len(rows)):
        button_x = table_area[0] + 5 * (table_area[2] - table_area[0]) // 6 + 10
        button_rect = (button_x, button_y + i * 40 + 10, button_x + 60, button_y + i * 40 + 30)
        draw_button(draw, button_rect, "Ver", fill=ACCENT_COLOR, text_color=BUTTON_TEXT_COLOR, radius=3)
    
    # Paginação
    pagination_rect = (table_area[0], table_area[3] + 10, table_area[2], table_area[3] + 40)
    draw_pagination(draw, pagination_rect)
    
    # Salvar imagem
    img.save(os.path.join(OUTPUT_DIR, "dashboard-fornecedor.png"))

def create_cadastro_licitacao():
    """Cria a tela de cadastro de licitação"""
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = draw_common_elements(img, "Cadastro de Licitação")
    
    # Área de conteúdo
    content_area = (240, 120, WIDTH - 20, HEIGHT - 20)
    
    # Card principal
    card_rect = (content_area[0], content_area[1], content_area[2], content_area[3])
    draw_rounded_rectangle(draw, card_rect, fill=CARD_COLOR, outline=BORDER_COLOR)
    
    # Abas do formulário
    tabs_rect = (card_rect[0] + 20, card_rect[1] + 20, card_rect[2] - 20, card_rect[1] + 60)
    tabs = ["Dados Básicos", "Itens", "Documentos", "Cronograma", "Revisão"]
    draw_tabs(draw, tabs_rect, tabs, active_index=0)
    
    # Formulário - Dados Básicos
    form_area = (card_rect[0] + 20, tabs_rect[3] + 20, card_rect[2] - 20, card_rect[3] - 60)
    
    # Linha 1 - Órgão e Unidade
    orgao_select = (form_area[0], form_area[1], form_area[0] + (form_area[2] - form_area[0]) // 2 - 10, form_area[1] + 40)
    draw_select(draw, orgao_select, ["Prefeitura Municipal"], "Prefeitura Municipal", "Órgão")
    
    unidade_select = (orgao_select[2] + 20, form_area[1], form_area[2], form_area[1] + 40)
    draw_select(draw, unidade_select, ["Secretaria de Administração"], "Secretaria de Administração", "Unidade")
    
    # Linha 2 - Modalidade e Forma
    modalidade_select = (form_area[0], orgao_select[3] + 20, form_area[0] + (form_area[2] - form_area[0]) // 2 - 10, orgao_select[3] + 60)
    draw_select(draw, modalidade_select, ["Pregão", "Concorrência", "Concurso", "Leilão"], "Pregão", "Modalidade")
    
    forma_select = (modalidade_select[2] + 20, orgao_select[3] + 20, form_area[2], orgao_select[3] + 60)
    draw_select(draw, forma_select, ["Eletrônica", "Presencial"], "Eletrônica", "Forma")
    
    # Linha 3 - Modo de Disputa e Critério de Julgamento
    modo_select = (form_area[0], modalidade_select[3] + 20, form_area[0] + (form_area[2] - form_area[0]) // 2 - 10, modalidade_select[3] + 60)
    draw_select(draw, modo_select, ["Aberto", "Fechado", "Aberto e Fechado"], "Aberto", "Modo de Disputa")
    
    criterio_select = (modo_select[2] + 20, modalidade_select[3] + 20, form_area[2], modalidade_select[3] + 60)
    draw_select(draw, criterio_select, ["Menor Preço", "Maior Desconto", "Técnica e Preço"], "Menor Preço", "Critério de Julgamento")
    
    # Linha 4 - Objeto
    objeto_label_y = criterio_select[3] + 20
    draw.text((form_area[0], objeto_label_y), "Objeto", font=small_font, fill=TEXT_COLOR)
    
    objeto_input = (form_area[0], objeto_label_y + 20, form_area[2], objeto_label_y + 100)
    draw.rectangle(objeto_input, fill=CARD_COLOR, outline=BORDER_COLOR)
    objeto_text = "Aquisição de material de escritório para atender às necessidades da Secretaria Municipal de Administração."
    wrapped_objeto = textwrap.wrap(objeto_text, width=100)
    for i, line in enumerate(wrapped_objeto):
        draw.text((objeto_input[0] + 10, objeto_input[1] + 10 + i * 20), line, font=regular_font, fill=TEXT_COLOR)
    
    # Linha 5 - Valor Estimado e Sigilo
    valor_input = (form_area[0], objeto_input[3] + 20, form_area[0] + (form_area[2] - form_area[0]) // 2 - 10, objeto_input[3] + 60)
    draw_input(draw, valor_input, "R$ 50.000,00", label="Valor Estimado")
    
    sigilo_y = objeto_input[3] + 40
    draw_checkbox(draw, (valor_input[2] + 20, sigilo_y, valor_input[2] + 40, sigilo_y + 20), "Orçamento Sigiloso")
    
    # Linha 6 - Responsável
    responsavel_select = (form_area[0], valor_input[3] + 20, form_area[2], valor_input[3] + 60)
    draw_select(draw, responsavel_select, ["João Silva - Pregoeiro"], "João Silva - Pregoeiro", "Responsável")
    
    # Botões de ação
    button_area = (card_rect[0] + 20, card_rect[3] - 50, card_rect[2] - 20, card_rect[3] - 20)
    
    cancel_button = (button_area[0], button_area[1], button_area[0] + 120, button_area[3])
    draw_button(draw, cancel_button, "Cancelar", fill=(200, 200, 200), text_color=TEXT_COLOR)
    
    save_button = (button_area[0] + 140, button_area[1], button_area[0] + 260, button_area[3])
    draw_button(draw, save_button, "Salvar Rascunho", fill=(255, 152, 0))
    
    next_button = (button_area[2] - 120, button_area[1], button_area[2], button_area[3])
    draw_button(draw, next_button, "Próximo")
    
    # Salvar imagem
    img.save(os.path.join(OUTPUT_DIR, "cadastro-licitacao.png"))

def create_envio_proposta():
    """Cria a tela de envio de proposta"""
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = draw_common_elements(img, "Envio de Proposta")
    
    # Área de conteúdo
    content_area = (240, 120, WIDTH - 20, HEIGHT - 20)
    
    # Card principal
    card_rect = (content_area[0], content_area[1], content_area[2], content_area[3])
    draw_rounded_rectangle(draw, card_rect, fill=CARD_COLOR, outline=BORDER_COLOR)
    
    # Cabeçalho com informações da licitação
    header_rect = (card_rect[0] + 20, card_rect[1] + 20, card_rect[2] - 20, card_rect[1] + 100)
    draw_rounded_rectangle(draw, header_rect, fill=(240, 240, 240))
    
    # Informações da licitação
    draw.text((header_rect[0] + 20, header_rect[1] + 15), "Pregão Eletrônico Nº 001/2025", 
             font=subtitle_font, fill=TEXT_COLOR)
    draw.text((header_rect[0] + 20, header_rect[1] + 45), 
             "Objeto: Aquisição de material de escritório para atender às necessidades da Secretaria Municipal de Administração.", 
             font=regular_font, fill=TEXT_COLOR)
    draw.text((header_rect[0] + 20, header_rect[1] + 70), 
             "Data de Abertura: 15/05/2025 às 10:00h | Valor Estimado: R$ 50.000,00", 
             font=regular_font, fill=TEXT_COLOR)
    
    # Abas do formulário
    tabs_rect = (card_rect[0] + 20, header_rect[3] + 20, card_rect[2] - 20, header_rect[3] + 60)
    tabs = ["Proposta", "Itens", "Documentos", "Revisão"]
    draw_tabs(draw, tabs_rect, tabs, active_index=1)
    
    # Formulário - Itens da Proposta
    form_area = (card_rect[0] + 20, tabs_rect[3] + 20, card_rect[2] - 20, card_rect[3] - 60)
    
    # Tabela de itens
    table_rect = (form_area[0], form_area[1], form_area[2], form_area[1] + 300)
    headers = ["Item", "Descrição", "Qtd", "Unid", "Valor Unit.", "Valor Total", "Marca/Modelo"]
    
    rows = [
        ["1", "Papel A4 (Resma)", "100", "Resma", "R$ 25,00", "R$ 2.500,00", "Report/Premium"],
        ["2", "Caneta Esferográfica Azul", "500", "Unid", "R$ 1,20", "R$ 600,00", "BIC/Cristal"],
        ["3", "Grampeador de Mesa", "50", "Unid", "R$ 18,50", "R$ 925,00", "Maped/Essential"],
        ["4", "Pasta AZ Lombo Largo", "100", "Unid", "R$ 15,80", "R$ 1.580,00", "Frama/Standard"]
    ]
    
    draw_table(draw, table_rect, headers, rows)
    
    # Botão para adicionar item
    add_button_rect = (form_area[0], table_rect[3] + 10, form_area[0] + 150, table_rect[3] + 40)
    draw_button(draw, add_button_rect, "+ Adicionar Item", fill=(76, 175, 80))
    
    # Resumo da proposta
    summary_rect = (form_area[0], table_rect[3] + 60, form_area[2], table_rect[3] + 160)
    draw_rounded_rectangle(draw, summary_rect, fill=(240, 240, 240))
    
    # Informações do resumo
    draw.text((summary_rect[0] + 20, summary_rect[1] + 15), "Resumo da Proposta", 
             font=subtitle_font, fill=TEXT_COLOR)
    draw.text((summary_rect[0] + 20, summary_rect[1] + 50), "Valor Total da Proposta: R$ 5.605,00", 
             font=regular_font, fill=TEXT_COLOR)
    draw.text((summary_rect[0] + 20, summary_rect[1] + 75), "Prazo de Entrega: 15 dias", 
             font=regular_font, fill=TEXT_COLOR)
    draw.text((summary_rect[0] + 20, summary_rect[1] + 100), "Validade da Proposta: 60 dias", 
             font=regular_font, fill=TEXT_COLOR)
    
    # Declarações
    declaration_rect = (form_area[0], summary_rect[3] + 20, form_area[0] + 20, summary_rect[3] + 40)
    draw_checkbox(draw, declaration_rect, "Declaro que sou Microempresa ou Empresa de Pequeno Porte e atendo aos requisitos da LC 123/2006.")
    
    # Botões de ação
    button_area = (card_rect[0] + 20, card_rect[3] - 50, card_rect[2] - 20, card_rect[3] - 20)
    
    back_button = (button_area[0], button_area[1], button_area[0] + 120, button_area[3])
    draw_button(draw, back_button, "Voltar", fill=(200, 200, 200), text_color=TEXT_COLOR)
    
    save_button = (button_area[0] + 140, button_area[1], button_area[0] + 260, button_area[3])
    draw_button(draw, save_button, "Salvar Rascunho", fill=(255, 152, 0))
    
    next_button = (button_area[2] - 120, button_area[1], button_area[2], button_area[3])
    draw_button(draw, next_button, "Próximo")
    
    # Salvar imagem
    img.save(os.path.join(OUTPUT_DIR, "envio-proposta.png"))

def create_sessao_lances():
    """Cria a tela de sessão de lances"""
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = draw_common_elements(img, "Sessão de Lances")
    
    # Área de conteúdo
    content_area = (240, 120, WIDTH - 20, HEIGHT - 20)
    
    # Card principal
    card_rect = (content_area[0], content_area[1], content_area[2], content_area[3])
    draw_rounded_rectangle(draw, card_rect, fill=CARD_COLOR, outline=BORDER_COLOR)
    
    # Cabeçalho com informações da licitação
    header_rect = (card_rect[0] + 20, card_rect[1] + 20, card_rect[2] - 20, card_rect[1] + 100)
    draw_rounded_rectangle(draw, header_rect, fill=(240, 240, 240))
    
    # Informações da licitação
    draw.text((header_rect[0] + 20, header_rect[1] + 15), "Pregão Eletrônico Nº 001/2025 - Sessão Pública", 
             font=subtitle_font, fill=TEXT_COLOR)
    draw.text((header_rect[0] + 20, header_rect[1] + 45), 
             "Objeto: Aquisição de material de escritório para atender às necessidades da Secretaria Municipal de Administração.", 
             font=regular_font, fill=TEXT_COLOR)
    draw.text((header_rect[0] + 20, header_rect[1] + 70), 
             "Pregoeiro: João Silva | Início da Sessão: 15/05/2025 às 10:00h", 
             font=regular_font, fill=TEXT_COLOR)
    
    # Área de conteúdo dividida em duas colunas
    left_col = (card_rect[0] + 20, header_rect[3] + 20, card_rect[0] + (card_rect[2] - card_rect[0]) // 2 - 10, card_rect[3] - 20)
    right_col = (left_col[2] + 20, header_rect[3] + 20, card_rect[2] - 20, card_rect[3] - 20)
    
    # Coluna esquerda - Lances
    # Título da seção
    draw.text((left_col[0], left_col[1]), "Item 1 - Papel A4 (Resma)", font=subtitle_font, fill=TEXT_COLOR)
    
    # Status da disputa
    status_rect = (left_col[0], left_col[1] + 40, left_col[2], left_col[1] + 80)
    draw_rounded_rectangle(draw, status_rect, fill=(25, 118, 210, 50), outline=ACCENT_COLOR)
    draw.text((status_rect[0] + 20, status_rect[1] + 10), "Disputa Aberta - Tempo Restante: 05:23", 
             font=regular_font, fill=ACCENT_COLOR)
    
    # Tabela de lances
    lance_table_rect = (left_col[0], status_rect[3] + 20, left_col[2], left_col[3] - 100)
    lance_headers = ["Classificação", "Fornecedor", "Valor do Lance", "Data/Hora"]
    
    lance_rows = [
        ["1º", "Empresa B", "R$ 22,50", "10:15:23"],
        ["2º", "Empresa A", "R$ 23,00", "10:14:45"],
        ["3º", "Empresa C", "R$ 24,30", "10:12:18"],
        ["4º", "Empresa D", "R$ 24,80", "10:10:05"],
        ["5º", "Empresa E", "R$ 25,00", "10:05:30"]
    ]
    
    draw_table(draw, lance_table_rect, lance_headers, lance_rows)
    
    # Área de envio de lance
    lance_form_rect = (left_col[0], lance_table_rect[3] + 20, left_col[2], left_col[3])
    draw_rounded_rectangle(draw, lance_form_rect, fill=(240, 240, 240))
    
    # Campos do formulário de lance
    draw.text((lance_form_rect[0] + 20, lance_form_rect[1] + 15), "Enviar Lance", 
             font=subtitle_font, fill=TEXT_COLOR)
    
    valor_lance_input = (lance_form_rect[0] + 20, lance_form_rect[1] + 50, lance_form_rect[0] + 200, lance_form_rect[1] + 80)
    draw_input(draw, valor_lance_input, "R$ ", label="Valor do Lance")
    
    enviar_lance_button = (lance_form_rect[0] + 220, lance_form_rect[1] + 50, lance_form_rect[0] + 320, lance_form_rect[1] + 80)
    draw_button(draw, enviar_lance_button, "Enviar Lance")
    
    # Coluna direita - Chat e Mensagens
    # Título da seção
    draw.text((right_col[0], right_col[1]), "Chat da Sessão", font=subtitle_font, fill=TEXT_COLOR)
    
    # Área de mensagens
    chat_area_rect = (right_col[0], right_col[1] + 40, right_col[2], right_col[3] - 60)
    draw_rounded_rectangle(draw, chat_area_rect, fill=(255, 255, 255), outline=BORDER_COLOR)
    
    # Mensagens do chat
    messages = [
        {"sender": "Sistema", "time": "10:00:00", "text": "Sessão pública iniciada."},
        {"sender": "Pregoeiro", "time": "10:01:15", "text": "Bom dia a todos. Vamos iniciar a fase de lances para o Item 1."},
        {"sender": "Empresa A", "time": "10:02:30", "text": "Bom dia, Pregoeiro."},
        {"sender": "Pregoeiro", "time": "10:05:45", "text": "Lembro que o intervalo mínimo entre lances é de R$ 0,10."},
        {"sender": "Sistema", "time": "10:10:05", "text": "Empresa D enviou lance de R$ 24,80."},
        {"sender": "Sistema", "time": "10:12:18", "text": "Empresa C enviou lance de R$ 24,30."},
        {"sender": "Sistema", "time": "10:14:45", "text": "Empresa A enviou lance de R$ 23,00."},
        {"sender": "Sistema", "time": "10:15:23", "text": "Empresa B enviou lance de R$ 22,50."}
    ]
    
    for i, msg in enumerate(messages):
        y = chat_area_rect[1] + 15 + i * 40
        sender_text = f"{msg['sender']} ({msg['time']}): "
        draw.text((chat_area_rect[0] + 15, y), sender_text, font=small_font, fill=ACCENT_COLOR)
        draw.text((chat_area_rect[0] + 15 + draw.textlength(sender_text, font=small_font), y), 
                 msg['text'], font=regular_font, fill=TEXT_COLOR)
    
    # Área de envio de mensagem
    message_input = (right_col[0], chat_area_rect[3] + 10, right_col[2] - 100, right_col[3])
    draw_input(draw, message_input, "Digite sua mensagem...")
    
    send_button = (message_input[2] + 10, message_input[1], right_col[2], message_input[3])
    draw_button(draw, send_button, "Enviar")
    
    # Salvar imagem
    img.save(os.path.join(OUTPUT_DIR, "sessao-lances.png"))

def create_habilitacao_julgamento():
    """Cria a tela de habilitação e julgamento"""
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = draw_common_elements(img, "Habilitação e Julgamento")
    
    # Área de conteúdo
    content_area = (240, 120, WIDTH - 20, HEIGHT - 20)
    
    # Card principal
    card_rect = (content_area[0], content_area[1], content_area[2], content_area[3])
    draw_rounded_rectangle(draw, card_rect, fill=CARD_COLOR, outline=BORDER_COLOR)
    
    # Cabeçalho com informações da licitação
    header_rect = (card_rect[0] + 20, card_rect[1] + 20, card_rect[2] - 20, card_rect[1] + 100)
    draw_rounded_rectangle(draw, header_rect, fill=(240, 240, 240))
    
    # Informações da licitação
    draw.text((header_rect[0] + 20, header_rect[1] + 15), "Pregão Eletrônico Nº 001/2025 - Habilitação", 
             font=subtitle_font, fill=TEXT_COLOR)
    draw.text((header_rect[0] + 20, header_rect[1] + 45), 
             "Objeto: Aquisição de material de escritório para atender às necessidades da Secretaria Municipal de Administração.", 
             font=regular_font, fill=TEXT_COLOR)
    draw.text((header_rect[0] + 20, header_rect[1] + 70), 
             "Pregoeiro: João Silva | Fase: Habilitação e Julgamento", 
             font=regular_font, fill=TEXT_COLOR)
    
    # Abas do processo
    tabs_rect = (card_rect[0] + 20, header_rect[3] + 20, card_rect[2] - 20, header_rect[3] + 60)
    tabs = ["Propostas", "Lances", "Habilitação", "Recursos", "Adjudicação"]
    draw_tabs(draw, tabs_rect, tabs, active_index=2)
    
    # Área de conteúdo
    content_rect = (card_rect[0] + 20, tabs_rect[3] + 20, card_rect[2] - 20, card_rect[3] - 20)
    
    # Fornecedor em análise
    fornecedor_rect = (content_rect[0], content_rect[1], content_rect[2], content_rect[1] + 60)
    draw_rounded_rectangle(draw, fornecedor_rect, fill=(240, 240, 240))
    
    draw.text((fornecedor_rect[0] + 20, fornecedor_rect[1] + 10), "Fornecedor em Análise: Empresa B", 
             font=subtitle_font, fill=TEXT_COLOR)
    draw.text((fornecedor_rect[0] + 20, fornecedor_rect[1] + 35), 
             "CNPJ: 12.345.678/0001-90 | Melhor Lance: R$ 22,50 por resma", 
             font=regular_font, fill=TEXT_COLOR)
    
    # Tabela de documentos
    docs_table_rect = (content_rect[0], fornecedor_rect[3] + 20, content_rect[2], fornecedor_rect[3] + 320)
    docs_headers = ["Documento", "Situação", "Validade", "Observações", "Ações"]
    
    docs_rows = [
        ["Contrato Social", "Aprovado", "N/A", "Documento conforme", ""],
        ["Certidão Negativa Federal", "Aprovado", "15/08/2025", "Documento válido", ""],
        ["Certidão Negativa Estadual", "Aprovado", "22/07/2025", "Documento válido", ""],
        ["Certidão Negativa Municipal", "Pendente", "10/06/2025", "Aguardando análise", ""],
        ["Certidão FGTS", "Aprovado", "30/09/2025", "Documento válido", ""],
        ["Certidão Trabalhista", "Reprovado", "05/04/2025", "Documento com restrição", ""]
    ]
    
    draw_table(draw, docs_table_rect, docs_headers, docs_rows)
    
    # Adicionar botões de ação na última coluna
    button_y = docs_table_rect[1] + 20
    for i in range(len(docs_rows)):
        button_x = docs_table_rect[0] + 4 * (docs_table_rect[2] - docs_table_rect[0]) // 5 + 10
        button_rect = (button_x, button_y + i * 40 + 10, button_x + 60, button_y + i * 40 + 30)
        draw_button(draw, button_rect, "Ver", fill=ACCENT_COLOR, text_color=BUTTON_TEXT_COLOR, radius=3)
    
    # Área de decisão
    decision_rect = (content_rect[0], docs_table_rect[3] + 20, content_rect[2], docs_table_rect[3] + 120)
    draw_rounded_rectangle(draw, decision_rect, fill=(240, 240, 240))
    
    draw.text((decision_rect[0] + 20, decision_rect[1] + 15), "Decisão do Pregoeiro", 
             font=subtitle_font, fill=TEXT_COLOR)
    
    # Opções de decisão
    habilitar_radio_pos = (decision_rect[0] + 40, decision_rect[1] + 60)
    draw_radio(draw, habilitar_radio_pos, "Habilitar Fornecedor", checked=False)
    
    inabilitar_radio_pos = (decision_rect[0] + 300, decision_rect[1] + 60)
    draw_radio(draw, inabilitar_radio_pos, "Inabilitar Fornecedor", checked=True)
    
    # Campo de justificativa
    justificativa_input = (decision_rect[0] + 20, decision_rect[1] + 80, decision_rect[2] - 20, decision_rect[3] - 10)
    draw_input(draw, justificativa_input, "Fornecedor inabilitado devido à restrição na Certidão Trabalhista.", label="")
    
    # Botões de ação
    button_area = (content_rect[0], decision_rect[3] + 20, content_rect[2], content_rect[3])
    
    voltar_button = (button_area[0], button_area[1], button_area[0] + 120, button_area[1] + 30)
    draw_button(draw, voltar_button, "Voltar", fill=(200, 200, 200), text_color=TEXT_COLOR)
    
    solicitar_button = (button_area[0] + 140, button_area[1], button_area[0] + 340, button_area[1] + 30)
    draw_button(draw, solicitar_button, "Solicitar Documentos Complementares", fill=(255, 152, 0))
    
    confirmar_button = (button_area[2] - 120, button_area[1], button_area[2], button_area[1] + 30)
    draw_button(draw, confirmar_button, "Confirmar")
    
    # Salvar imagem
    img.save(os.path.join(OUTPUT_DIR, "habilitacao-julgamento.png"))

def create_gestao_contratos():
    """Cria a tela de gestão de contratos"""
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = draw_common_elements(img, "Gestão de Contratos")
    
    # Área de conteúdo
    content_area = (240, 120, WIDTH - 20, HEIGHT - 20)
    
    # Barra de pesquisa e filtros
    search_rect = (content_area[0], content_area[1], content_area[0] + 400, content_area[1] + 40)
    draw_search(draw, search_rect, "Buscar contratos...")
    
    filter_button = (search_rect[2] + 20, search_rect[1], search_rect[2] + 120, search_rect[3])
    draw_button(draw, filter_button, "Filtros", fill=CARD_COLOR, text_color=TEXT_COLOR)
    
    new_button = (content_area[2] - 150, content_area[1], content_area[2], content_area[1] + 40)
    draw_button(draw, new_button, "+ Novo Contrato", fill=(76, 175, 80))
    
    # Abas de contratos
    tabs_rect = (content_area[0], content_area[1] + 60, content_area[2], content_area[1] + 100)
    tabs = ["Todos", "Vigentes", "Em Elaboração", "Encerrados", "Cancelados"]
    draw_tabs(draw, tabs_rect, tabs, active_index=1)
    
    # Tabela de contratos
    table_rect = (content_area[0], tabs_rect[3] + 20, content_area[2], HEIGHT - 80)
    headers = ["Nº", "Objeto", "Fornecedor", "Valor", "Vigência", "Situação", "Ações"]
    
    rows = [
        ["001/2025", "Material de escritório", "Empresa B", "R$ 22.500,00", "15/05/2025 a 14/05/2026", "Vigente", ""],
        ["002/2025", "Serviços de limpeza", "Empresa C", "R$ 118.000,00", "01/06/2025 a 31/05/2026", "Vigente", ""],
        ["003/2025", "Equipamentos de TI", "Empresa A", "R$ 65.000,00", "10/06/2025 a 09/06/2026", "Em elaboração", ""],
        ["004/2025", "Manutenção predial", "Empresa D", "R$ 95.000,00", "20/06/2025 a 19/06/2026", "Vigente", ""],
        ["005/2025", "Serviços gráficos", "Empresa E", "R$ 35.000,00", "01/07/2025 a 30/06/2026", "Vigente", ""]
    ]
    
    draw_table(draw, table_rect, headers, rows)
    
    # Adicionar botões de ação na última coluna
    button_y = table_rect[1] + 20
    for i in range(len(rows)):
        button_x = table_rect[0] + 6 * (table_rect[2] - table_rect[0]) // 7 + 10
        
        # Botão Ver
        ver_button_rect = (button_x, button_y + i * 40 + 10, button_x + 50, button_y + i * 40 + 30)
        draw_button(draw, ver_button_rect, "Ver", fill=ACCENT_COLOR, text_color=BUTTON_TEXT_COLOR, radius=3)
        
        # Botão Editar
        edit_button_rect = (button_x + 60, button_y + i * 40 + 10, button_x + 110, button_y + i * 40 + 30)
        draw_button(draw, edit_button_rect, "Editar", fill=(255, 152, 0), text_color=BUTTON_TEXT_COLOR, radius=3)
    
    # Paginação
    pagination_rect = (content_area[0], HEIGHT - 60, content_area[2], HEIGHT - 30)
    draw_pagination(draw, pagination_rect)
    
    # Salvar imagem
    img.save(os.path.join(OUTPUT_DIR, "gestao-contratos.png"))

# Gerar todos os protótipos
def generate_all_wireframes():
    create_home_page()
    create_login_page()
    create_dashboard_orgao()
    create_dashboard_fornecedor()
    create_cadastro_licitacao()
    create_envio_proposta()
    create_sessao_lances()
    create_habilitacao_julgamento()
    create_gestao_contratos()
    print("Todos os protótipos foram gerados com sucesso!")

if __name__ == "__main__":
    generate_all_wireframes()
