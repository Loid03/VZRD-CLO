import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
from decimal import Decimal
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import from VzrdClothing package
from VzrdClothing.models_db import db, Product, Customer, Order, OrderItem, Contact, Newsletter, User, Favorite
from forms import LoginForm, RegisterForm, ProfileForm, ProductForm, OrderStatusForm, SearchForm

logging.basicConfig(level=logging.DEBUG)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or os.environ.get("FLASK_SECRET_KEY", "vzrd-secret-key-2024")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para acessar esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# configure the database - use SQLite for reliability
database_url = "sqlite:///vzrd_store.db"
print(f"Using VZRD database: {database_url}")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
}

# initialize extensions
db.init_app(app)
CORS(app)

# ============================================
# CREATE DATABASE TABLES
# ============================================

with app.app_context():
    try:
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Add sample data if none exists
        if Product.query.count() == 0:
            sample_products = [
                {
                    'name': 'VZRD Tokyo Nights',
                    'description': 'Camiseta oversized inspirada nas luzes neon de Tokyo. Tecido premium 100% algodão com estampa exclusiva VZRD.',
                    'price': Decimal('89.90'),
                    'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                    'category': 'oversized',
                    'featured': True,
                    'in_stock': True
                },
                {
                    'name': 'Street Samurai',
                    'description': 'Design exclusivo com elementos japoneses modernos. Camiseta oversized de alta qualidade.',
                    'price': Decimal('94.90'),
                    'image_url': 'https://images.unsplash.com/photo-1503341504253-dff4815485f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                    'category': 'streetwear',
                    'featured': True,
                    'in_stock': True
                },
                {
                    'name': 'Neon Dreams',
                    'description': 'Estampa vibrante com cores neon que capturam a essência cyberpunk.',
                    'price': Decimal('79.90'),
                    'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                    'category': 'oversized',
                    'featured': False,
                    'in_stock': True
                },
                {
                    'name': 'Anime Rebellion',
                    'description': 'Para os verdadeiros otakus de plantão. Design exclusivo que mistura anime culture com street attitude.',
                    'price': Decimal('99.90'),
                    'image_url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                    'category': 'premium',
                    'featured': True,
                    'in_stock': True
                }
            ]
            
            for product_data in sample_products:
                product = Product(**product_data)
                db.session.add(product)
            
            # Create admin user
            admin_user = User(
                username='admin',
                email='admin@vzrd.com',
                first_name='Admin',
                last_name='VZRD',
                is_admin=True
            )
            admin_user.set_password('vzrd123')
            db.session.add(admin_user)
            
            # Create test user
            test_user = User(
                username='testuser',
                email='user@vzrd.com',
                first_name='João',
                last_name='Silva'
            )
            test_user.set_password('123456')
            db.session.add(test_user)
            
            db.session.commit()
            print("✓ Sample data added successfully!")
    except Exception as e:
        print(f"Database initialization error: {e}")

# ============================================
# MAIN ROUTES
# ============================================

@app.route('/')
def index():
    try:
        featured_products = Product.query.filter_by(featured=True, in_stock=True).limit(6).all()
        search_form = SearchForm()
        return render_template('index.html', featured_products=featured_products, search_form=search_form)
    except Exception as e:
        print(f"Database error in index route: {e}")
        return render_template('index.html', featured_products=[], search_form=SearchForm())

@app.route('/produtos')
def produtos():
    try:
        search_form = SearchForm()
        query = request.args.get('query', '')
        category = request.args.get('category', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        products_query = Product.query.filter_by(in_stock=True)
        
        if query:
            products_query = products_query.filter(
                Product.name.ilike(f'%{query}%') | 
                Product.description.ilike(f'%{query}%')
            )
        
        if category:
            products_query = products_query.filter_by(category=category)
        
        if min_price is not None:
            products_query = products_query.filter(Product.price >= min_price)
        
        if max_price is not None:
            products_query = products_query.filter(Product.price <= max_price)
        
        products = products_query.all()
        
        user_favorites = []
        if current_user.is_authenticated:
            try:
                favorites = Favorite.query.filter_by(user_id=current_user.id).all()
                user_favorites = [fav.product_id for fav in favorites]
            except:
                user_favorites = []
        
        return render_template('produtos.html', 
                             products=products, 
                             search_form=search_form,
                             user_favorites=user_favorites,
                             query=query,
                             category=category,
                             min_price=min_price,
                             max_price=max_price)
    except Exception as e:
        print(f"Database error in produtos route: {e}")
        flash('Erro ao carregar produtos.', 'error')
        return render_template('produtos.html', products=[], search_form=SearchForm(), user_favorites=[])

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/drops')
def drops():
    return render_template('drops.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        try:
            contact = Contact(
                name=request.form.get('name', ''),
                email=request.form.get('email', ''),
                subject=request.form.get('subject', ''),
                message=request.form.get('message', '')
            )
            db.session.add(contact)
            db.session.commit()
            flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
            return redirect(url_for('contato'))
        except Exception as e:
            db.session.rollback()
            print(f"Error saving contact: {e}")
            flash('Erro ao enviar mensagem. Tente novamente.', 'error')
    
    return render_template('contato.html')

@app.route('/subscribe-newsletter', methods=['POST'])
def subscribe_newsletter():
    try:
        email = request.form.get('email') or request.get_json().get('email')
        if not email:
            return jsonify({'success': False, 'message': 'E-mail é obrigatório'}), 400
        
        existing = Newsletter.query.filter_by(email=email).first()
        if existing:
            return jsonify({'success': False, 'message': 'E-mail já cadastrado'})
        
        newsletter = Newsletter(email=email, active=True)
        db.session.add(newsletter)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Obrigado por se inscrever!'})
    except Exception as e:
        db.session.rollback()
        print(f"Error subscribing to newsletter: {e}")
        return jsonify({'success': False, 'message': 'Erro interno'}), 500

# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Bem-vindo, {user.get_full_name()}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('E-mail ou senha incorretos.', 'error')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Conta criada com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            flash('Erro ao criar conta. Tente novamente.', 'error')
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        try:
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.phone = form.phone.data
            current_user.address = form.address.data
            current_user.city = form.city.data
            current_user.state = form.state.data
            current_user.zipcode = form.zipcode.data
            
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            print(f"Error updating profile: {e}")
            flash('Erro ao atualizar perfil.', 'error')
    
    return render_template('auth/profile.html', form=form)

# ============================================
# FAVORITES ROUTES
# ============================================

@app.route('/favoritos')
@login_required
def favoritos():
    try:
        favorites = db.session.query(Favorite, Product).join(Product).filter(
            Favorite.user_id == current_user.id
        ).all()
        
        favorite_products = [product for _, product in favorites]
        
        return render_template('favoritos.html', products=favorite_products)
    except Exception as e:
        print(f"Error loading favorites: {e}")
        flash('Erro ao carregar favoritos.', 'error')
        return render_template('favoritos.html', products=[])

@app.route('/api/toggle-favorite', methods=['POST'])
@login_required
def toggle_favorite():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        
        if not product_id:
            return jsonify({'success': False, 'message': 'ID do produto é obrigatório'}), 400
        
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Produto não encontrado'}), 404
        
        favorite = Favorite.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if favorite:
            db.session.delete(favorite)
            is_favorited = False
            message = 'Produto removido dos favoritos'
        else:
            favorite = Favorite(user_id=current_user.id, product_id=product_id)
            db.session.add(favorite)
            is_favorited = True
            message = 'Produto adicionado aos favoritos'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'is_favorited': is_favorited,
            'message': message
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error toggling favorite: {e}")
        return jsonify({'success': False, 'message': 'Erro interno do servidor'}), 500

# ============================================
# PRODUCT DETAIL ROUTE
# ============================================

@app.route('/produto/<int:product_id>')
def product_detail(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        
        is_favorited = False
        if current_user.is_authenticated:
            favorite = Favorite.query.filter_by(
                user_id=current_user.id, 
                product_id=product_id
            ).first()
            is_favorited = favorite is not None
        
        related_products = Product.query.filter(
            Product.category == product.category,
            Product.id != product_id,
            Product.in_stock == True
        ).limit(4).all()
        
        return render_template('produto_detail.html', 
                             product=product,
                             is_favorited=is_favorited,
                             related_products=related_products)
    except Exception as e:
        print(f"Error loading product detail: {e}")
        flash('Produto não encontrado.', 'error')
        return redirect(url_for('produtos'))

# ============================================
# ADMIN ROUTES
# ============================================

@app.route('/admin')
@login_required
def admin_dashboard():
    if not (current_user.is_admin or current_user.email == 'admin@vzrd.com'):
        flash('Acesso negado. Apenas administradores.', 'error')
        return redirect(url_for('index'))
    
    try:
        total_products = Product.query.count()
        total_orders = Order.query.count()
        total_users = User.query.count()
        pending_orders = Order.query.filter_by(status='pending').count()
        
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        low_stock_products = []
        
        return render_template('admin/dashboard.html',
                             total_products=total_products,
                             total_orders=total_orders,
                             total_users=total_users,
                             pending_orders=pending_orders,
                             recent_orders=recent_orders,
                             low_stock_products=low_stock_products)
    except Exception as e:
        print(f"Error loading admin dashboard: {e}")
        flash('Erro ao carregar dashboard.', 'error')
        return render_template('admin/dashboard.html',
                             total_products=0,
                             total_orders=0,
                             total_users=0,
                             pending_orders=0,
                             recent_orders=[],
                             low_stock_products=[])

@app.route('/admin/products')
@login_required  
def admin_products():
    if not (current_user.is_admin or current_user.email == 'admin@vzrd.com'):
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))
    
    try:
        products = Product.query.order_by(Product.created_at.desc()).all()
        return render_template('admin/products.html', products=products)
    except Exception as e:
        print(f"Error loading products: {e}")
        return render_template('admin/products.html', products=[])

@app.route('/admin/add-product', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if not (current_user.is_admin or current_user.email == 'admin@vzrd.com'):
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))
    
    form = ProductForm()
    if form.validate_on_submit():
        try:
            product = Product(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                image_url=form.image_url.data,
                category=form.category.data,
                featured=form.featured.data,
                in_stock=form.in_stock.data
            )
            
            db.session.add(product)
            db.session.commit()
            
            flash('Produto adicionado com sucesso!', 'success')
            return redirect(url_for('admin_products'))
        except Exception as e:
            db.session.rollback()
            print(f"Error adding product: {e}")
            flash('Erro ao adicionar produto.', 'error')
    
    return render_template('admin/add_product.html', form=form)

@app.route('/admin/orders')
@login_required
def admin_orders():
    if not (current_user.is_admin or current_user.email == 'admin@vzrd.com'):
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))
    
    try:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        return render_template('admin/orders.html', orders=orders)
    except Exception as e:
        print(f"Error loading orders: {e}")
        return render_template('admin/orders.html', orders=[])

@app.route('/admin/order/<int:order_id>')
@login_required
def admin_order_detail(order_id):
    if not (current_user.is_admin or current_user.email == 'admin@vzrd.com'):
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))
    
    try:
        order = Order.query.get_or_404(order_id)
        form = OrderStatusForm(obj=order)
        return render_template('admin/order_detail.html', order=order, form=form)
    except Exception as e:
        print(f"Error loading order: {e}")
        flash('Pedido não encontrado.', 'error')
        return redirect(url_for('admin_orders'))

@app.route('/admin/contacts')
@login_required
def admin_contacts():
    if not (current_user.is_admin or current_user.email == 'admin@vzrd.com'):
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))
    
    try:
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
        return render_template('admin/contacts.html', contacts=contacts)
    except Exception as e:
        print(f"Error loading contacts: {e}")
        return render_template('admin/contacts.html', contacts=[])

@app.route('/admin/newsletter')
@login_required
def admin_newsletter():
    if not (current_user.is_admin or current_user.email == 'admin@vzrd.com'):
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))
    
    try:
        subscribers = Newsletter.query.order_by(Newsletter.subscribed_at.desc()).all()
        return render_template('admin/newsletter.html', subscribers=subscribers)
    except Exception as e:
        print(f"Error loading newsletter: {e}")
        return render_template('admin/newsletter.html', subscribers=[])

# ============================================
# CART AND ORDER ROUTES
# ============================================

@app.route('/api/product/<int:product_id>')
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'success': True,
            'product': product.to_dict()
        })
    except Exception as e:
        print(f"Error getting product: {e}")
        return jsonify({'success': False, 'message': 'Produto não encontrado'}), 404

@app.route('/api/create-order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        
        # Create customer first
        customer = Customer(
            name=data.get('customer_name', ''),
            email=data.get('customer_email', ''),
            phone=data.get('customer_phone', ''),
            address=data.get('customer_address', ''),
            city=data.get('customer_city', ''),
            state=data.get('customer_state', ''),
            zipcode=data.get('customer_zipcode', '')
        )
        db.session.add(customer)
        db.session.flush()
        
        # Create order
        order = Order(
            customer_id=customer.id,
            total_amount=Decimal(str(data.get('total_amount', 0))),
            status='pending',
            payment_status='pending'
        )
        
        if current_user.is_authenticated:
            order.user_id = current_user.id
        
        db.session.add(order)
        db.session.flush()
        
        # Add order items
        cart_items = data.get('items', [])
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product_id'],
                product_name=item['product_name'],
                size=item['size'],
                quantity=item['quantity'],
                unit_price=Decimal(str(item['unit_price']))
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        # Send SMS notifications
        try:
            send_new_order_admin_notification(order)
            send_order_confirmation_sms(order)
        except Exception as e:
            print(f"SMS notification error: {e}")
        
        return jsonify({
            'success': True,
            'order_id': order.id,
            'message': 'Pedido criado com sucesso!'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating order: {e}")
        return jsonify({'success': False, 'message': 'Erro ao criar pedido'}), 500

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/order-success/<int:order_id>')
def order_success(order_id):
    try:
        order = Order.query.get_or_404(order_id)
        return render_template('order_success.html', order=order)
    except Exception as e:
        print(f"Error loading order success: {e}")
        flash('Pedido não encontrado.', 'error')
        return redirect(url_for('index'))

# ============================================
# API ROUTES
# ============================================

@app.route('/api/search')
def search_api():
    try:
        query = request.args.get('query', '')
        category = request.args.get('category', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        products_query = Product.query.filter_by(in_stock=True)
        
        if query:
            products_query = products_query.filter(
                Product.name.ilike(f'%{query}%') | 
                Product.description.ilike(f'%{query}%')
            )
        
        if category:
            products_query = products_query.filter_by(category=category)
        
        if min_price is not None:
            products_query = products_query.filter(Product.price >= min_price)
        
        if max_price is not None:
            products_query = products_query.filter(Product.price <= max_price)
        
        products = products_query.all()
        
        products_data = []
        for product in products:
            products_data.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': float(product.price),
                'image_url': product.image_url,
                'category': product.category,
                'featured': product.featured
            })
        
        return jsonify({
            'success': True,
            'products': products_data,
            'count': len(products_data)
        })
        
    except Exception as e:
        print(f"Error in search API: {e}")
        return jsonify({'success': False, 'message': 'Erro na busca'}), 500

# ============================================
# SMS NOTIFICATION FUNCTIONS
# ============================================

def send_new_order_admin_notification(order):
    """Send SMS notification to admin when new order is created"""
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_phone = os.environ.get('TWILIO_PHONE_NUMBER')
        admin_phone = os.environ.get('ADMIN_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, twilio_phone, admin_phone]):
            print("Twilio credentials not configured")
            return False
        
        # Create message
        customer_name = order.get_customer_name() if hasattr(order, 'get_customer_name') else 'Cliente'
        total = f"R$ {order.total_amount:.2f}"
        
        message = f"""🆕 VZRD - Novo Pedido #{order.id}
👤 Cliente: {customer_name}
💰 Total: {total}
📱 Status: {order.status.title()}

🎌 Acesse o painel admin para mais detalhes!"""
        
        # Send SMS
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=twilio_phone,
            to=admin_phone
        )
        
        print(f"✓ Admin SMS sent for order {order.id}")
        return True
        
    except Exception as e:
        print(f"Error sending admin SMS: {e}")
        return False

def send_order_confirmation_sms(order, customer_phone):
    """Send SMS confirmation to customer"""
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_phone = os.environ.get('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, twilio_phone]):
            print("Twilio credentials not configured")
            return False
        
        # Format phone number
        if not customer_phone.startswith('+'):
            customer_phone = '+55' + customer_phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Create message
        total = f"R$ {order.total_amount:.2f}"
        
        message = f"""🏮 VZRD - Pedido Confirmado!

📦 Pedido #{order.id}
💰 Total: {total}
📱 Status: Processando

🎌 Obrigado pela preferência!
Você receberá atualizações sobre seu pedido."""
        
        # Send SMS
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=twilio_phone,
            to=customer_phone
        )
        
        print(f"✓ Customer SMS sent for order {order.id}")
        return True
        
    except Exception as e:
        print(f"Error sending customer SMS: {e}")
        return False

def send_order_status_update_sms(order, customer_phone, new_status):
    """Send SMS when order status changes"""
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_phone = os.environ.get('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, twilio_phone]):
            return False
        
        # Format phone number
        if not customer_phone.startswith('+'):
            customer_phone = '+55' + customer_phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Status messages
        status_messages = {
            'pending': '⏳ Seu pedido está sendo processado',
            'confirmed': '✅ Pedido confirmado e será enviado em breve',
            'shipped': '🚚 Seu pedido foi enviado!',
            'delivered': '🎉 Pedido entregue! Obrigado pela preferência!',
            'cancelled': '❌ Pedido cancelado. Entre em contato conosco.'
        }
        
        status_emoji = {
            'pending': '⏳',
            'confirmed': '✅',
            'shipped': '🚚',
            'delivered': '🎉',
            'cancelled': '❌'
        }
        
        message = f"""{status_emoji.get(new_status, '📱')} VZRD - Atualização do Pedido

📦 Pedido #{order.id}
🔄 Status: {status_messages.get(new_status, f'Status atualizado para {new_status}')}

🎌 Acompanhe seu pedido em nosso site!"""
        
        # Send SMS
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=twilio_phone,
            to=customer_phone
        )
        
        print(f"✓ Status update SMS sent for order {order.id}")
        return True
        
    except Exception as e:
        print(f"Error sending status update SMS: {e}")
        return False

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)