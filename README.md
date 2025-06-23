# 🏮 VZRD - Otaku Graffiti Streetwear 🎌

![VZRD Logo](static/images/vzrd_logo.png)

**VZRD** é uma plataforma de e-commerce premium especializada em streetwear com estética anime e graffiti japonês. Combinamos a cultura otaku com o estilo urbano para criar peças únicas e exclusivas.

## ✨ Funcionalidades

### 🎯 Core Features
- **E-commerce Completo**: Catálogo de produtos, carrinho, checkout
- **Autenticação**: Sistema completo de login/registro com Flask-Login
- **Painel Admin**: Dashboard com estatísticas, gestão de produtos e pedidos
- **Sistema de Favoritos**: Usuários podem favoritar produtos (coração toggle)
- **Busca Avançada**: Filtros por nome, categoria, faixa de preço
- **Sistema de Reviews**: Avaliações com estrelas e comentários

### 🎨 Design & UX
- **Estética Anime + Graffiti**: Paleta neon roxo/azul com efeitos glitch
- **Fontes Temáticas**: Permanent Marker, Zen Tokyo Zoo, Poppins
- **Animações**: Integrate com Animate.css para transições suaves
- **Responsive**: Design adaptativo para todos os dispositivos
- **Ícones Japoneses**: Menu com emojis temáticos (🈶 🏮 🎌 📮)

### 📱 Automações
- **SMS via Twilio**: Notificações automáticas para admin e clientes
- **Newsletter**: Sistema de inscrição para updates
- **Drops Exclusivos**: Página com countdown para lançamentos limitados

### 🛠 Tecnologias

**Backend:**
- Python 3.11
- Flask (Web Framework)
- SQLAlchemy (ORM)
- Flask-Login (Autenticação)
- Flask-WTF (Formulários)
- SQLite/PostgreSQL (Database)
- Twilio (SMS)
- SendGrid (Email)

**Frontend:**
- HTML5/CSS3/JavaScript
- Bootstrap 5
- Animate.css
- Font Awesome
- Google Fonts

## 🚀 Como Rodar o Projeto

### 📋 Pré-requisitos
- Python 3.11+
- pip (gerenciador de pacotes Python)

### 🔧 Instalação

1. **Clone o repositório:**
```bash
git clone <repo-url>
cd vzrd-ecommerce
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
# Database
DATABASE_URL=sqlite:///vzrd_store.db

# Flask
SESSION_SECRET=your-secret-key-here

# Twilio SMS (opcional)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
ADMIN_PHONE_NUMBER=+5511916292538
```

4. **Execute a aplicação:**
```bash
python app.py
```

5. **Acesse no navegador:**
```
http://localhost:5000
```

## 👤 Credenciais de Teste

### Admin:
- **Email:** admin@vzrd.com
- **Senha:** vzrd123
- **Acesso:** Dashboard completo, gestão de produtos/pedidos

### Usuário:
- **Email:** user@vzrd.com  
- **Senha:** 123456
- **Acesso:** Compras, favoritos, perfil

## 📁 Estrutura do Projeto

```
vzrd-ecommerce/
├── app.py                 # Aplicação principal
├── models.py             # Modelos do banco de dados
├── forms.py              # Formulários WTF
├── requirements.txt      # Dependências Python
├── .env.example         # Exemplo de variáveis de ambiente
├── README.md            # Este arquivo
├── static/              # Arquivos estáticos
│   ├── css/
│   │   └── anime_style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── vzrd_logo.png
├── templates/           # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── produtos.html
│   ├── produto_detail.html
│   ├── drops.html
│   ├── admin/
│   └── auth/
└── VzrdClothing/       # Package com modelos
    ├── __init__.py
    └── models_db.py
```

## 🎌 Páginas Principais

- **🏠 Home:** Landing page com produtos em destaque
- **🈶 Produtos:** Catálogo com busca e filtros avançados  
- **🏮 Drops:** Lançamentos exclusivos com countdown
- **👤 Perfil:** Gestão de conta do usuário
- **❤️ Favoritos:** Lista de produtos favoritados
- **🛒 Checkout:** Processo de compra
- **⚙️ Admin:** Dashboard administrativo (apenas admins)

## 📱 Recursos de SMS

Configure o Twilio para receber notificações automáticas:

- **Novo Pedido:** Admin recebe SMS quando pedido é criado
- **Confirmação:** Cliente recebe SMS de confirmação
- **Atualizações:** SMS quando status do pedido muda

## 🎯 Roadmap Futuro

- [ ] **Mascote VZRD**: Personagem anime interativo
- [ ] **Trailer em Vídeo**: Opening estilo anime da marca
- [ ] **História da Marca**: Página com storytelling visual
- [ ] **Chatbot IA**: Atendimento otaku com personalidade
- [ ] **Realidade Aumentada**: Experimentar produtos virtualmente
- [ ] **Gamificação**: Sistema de pontos e conquistas
- [ ] **Comunidade**: Fórum para otakus e streetwear lovers

## 📞 Suporte

Para dúvidas ou suporte:
- **Email:** vzrd@gmail.com
- **WhatsApp:** (11) 91629-2538

## 🎨 Créditos

- **Design:** Inspirado na cultura anime e graffiti japonês
- **Fontes:** Google Fonts (Permanent Marker, Zen Tokyo Zoo, Poppins)
- **Ícones:** Font Awesome
- **Animações:** Animate.css
- **Imagens:** Unsplash (placeholder products)

---

**🎌 VZRD - Onde otakus encontram seu estilo nas ruas 🏮**

*Desenvolvido com ❤️ para a comunidade anime e streetwear*