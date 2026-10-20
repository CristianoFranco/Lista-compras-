import io
import urllib.parse
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configuração da página para navegação em celulares
st.set_page_config(
    page_title="Lista de Compras",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS para Acessibilidade e Botões Grandes (Idosos)
st.markdown("""
    <style>
    /* Aumenta a fonte geral */
    html, body, [class*="css"] {
        font-size: 18px !important;
    }
    /* Estilo dos botões do Streamlit */
    .stButton > button {
        width: 100%;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 12px 20px !important;
        border-radius: 12px !important;
    }
    /* Estilo do botão do WhatsApp */
    .btn-whatsapp {
        display: inline-block;
        width: 100%;
        background-color: #25D366;
        color: white !important;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        padding: 14px 20px;
        border-radius: 12px;
        text-decoration: none;
        margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .btn-whatsapp:hover {
        background-color: #1EBE5D;
    }
    </style>
""", unsafe_allow_html=True)

# Dados Iniciais (Sem carnes, frutas ou verduras)
CATEGORIAS = {
    "Mercearia & Alimentos": [
        "Pão de forma", "Molho de tomate", "Milho verde", "Biscoito água e sal",
        "Caldo galinha", "Biscoito rancheiro", "Pão de queijo", "Farinha de trigo",
        "Arroz", "Macarrão", "Requeijão cremoso", "Café", "Óleo de soja",
        "Vinagre", "Leite UHT desnatado", "Farinha de mandioca", "Feijão carioquinha",
        "Sardinha em óleo", "Ovos brancos", "Cerveja"
    ],
    "Higiene & Limpeza": [
        "Creme dental", "Aparelho de barbear", "Desodorante", "Sabão",
        "Detergente líquido", "Desinfetante", "Amaciante", "Limpador",
        "Detergente em pó"
    ]
}

# Inicializa o estado do carrinho na sessão
if "carrinho" not in st.session_state:
    st.session_state.carrinho = {}

if "outros_itens" not in st.session_state:
    st.session_state.outros_itens = []

# Função para gerar o PDF em memória (Sem a letra 'x', apenas quantidade)
def gerar_pdf(carrinho):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Título
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, 750, "Lista de Compras")
    
    # Cabeçalho da tabela
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 720, "Item / Produto")
    p.drawString(500, 720, "Qtd")
    p.line(50, 712, 550, 712)
    
    p.setFont("Helvetica", 11)
    y = 690
    
    for item, qtd in carrinho.items():
        if qtd > 0:
            if y < 50:
                p.showPage()
                y = 750
                p.setFont("Helvetica", 11)
            
            p.drawString(50, y, str(item))
            # Quantidade como número puro
            p.drawString(500, y, str(qtd))
            y -= 20
            
    p.save()
    buffer.seek(0)
    return buffer

# Topo da Aplicação
st.title("🛒 Lista de Compras")
st.write("Toque no **+** ou **-** para ajustar as quantidades:")

# Campo para Adicionar Novo Produto
st.subheader("➕ Adicionar outro produto")
col_input, col_btn = st.columns([3, 1])
with col_input:
    novo_item = st.text_input("Novo produto", placeholder="Ex: Guardanapo, Azeitona...", label_visibility="collapsed")
with col_btn:
    if st.button("Incluir") and novo_item.strip():
        item_nome = novo_item.strip()
        if item_nome not in st.session_state.outros_itens:
            st.session_state.outros_itens.append(item_nome)
            st.session_state.carrinho[item_nome] = 1
            st.rerun()

# Se houver itens extras adicionados pelo usuário
if st.session_state.outros_itens:
    st.markdown("---")
    st.subheader("📌 Outros Itens Adicionados")
    for item in st.session_state.outros_itens:
        col_nome, col_menos, col_qtd, col_mais = st.columns([4, 1, 1, 1])
        qtd_atual = st.session_state.carrinho.get(item, 0)
        
        with col_nome:
            st.write(f"**{item}**")
        with col_menos:
            if st.button("➖", key=f"sub_{item}"):
                if qtd_atual > 0:
                    st.session_state.carrinho[item] = qtd_atual - 1
                    st.rerun()
        with col_qtd:
            st.markdown(f"<h4 style='text-align: center; margin: 0;'>{qtd_atual}</h4>", unsafe_allow_html=True)
        with col_mais:
            if st.button("➕", key=f"add_{item}"):
                st.session_state.carrinho[item] = qtd_atual + 1
                st.rerun()

# Exibição das Categorias Padrão
for cat_nome, itens in CATEGORIAS.items():
    st.markdown("---")
    st.subheader(f"📦 {cat_nome}")
    
    for item in itens:
        col_nome, col_menos, col_qtd, col_mais = st.columns([4, 1, 1, 1])
        qtd_atual = st.session_state.carrinho.get(item, 0)
        
        with col_nome:
            st.write(item)
        with col_menos:
            if st.button("➖", key=f"sub_{item}"):
                if qtd_atual > 0:
                    st.session_state.carrinho[item] = qtd_atual - 1
                    st.rerun()
        with col_qtd:
            st.markdown(f"<h4 style='text-align: center; margin: 0;'>{qtd_atual}</h4>", unsafe_allow_html=True)
        with col_mais:
            if st.button("➕", key=f"add_{item}"):
                st.session_state.carrinho[item] = qtd_atual + 1
                st.rerun()

# Filtra apenas o que possui quantidade > 0
itens_selecionados = {k: v for k, v in st.session_state.carrinho.items() if v > 0}

st.markdown("---")

# Seção de Finalização
if itens_selecionados:
    st.success(f"**Total de itens selecionados:** {sum(itens_selecionados.values())} unidades")
    
    # 1. Gerar PDF
    pdf_bytes = gerar_pdf(itens_selecionados)
    
    st.download_button(
        label="📄 1º Passo: Baixar PDF da Lista",
        data=pdf_bytes,
        file_name="lista_de_compras.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
    # 2. Link formatado para o WhatsApp
    texto_wa = "*LISTA DE COMPRAS*\n\n"
    for k, v in itens_selecionados.items():
        texto_wa += f"• {k}: *{v}*\n"
        
    url_wa = f"https://api.whatsapp.com/send?text={urllib.parse.quote(texto_wa)}"
    
    st.markdown(
        f'<a href="{url_wa}" target="_blank" class="btn-whatsapp">📲 2º Passo: Compartilhar no WhatsApp</a>',
        unsafe_allow_html=True
    )
else:
    st.info("Sua lista está vazia. Selecione pelo menos 1 item para salvar/compartilhar.")
