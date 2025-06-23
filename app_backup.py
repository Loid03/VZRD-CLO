import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
from decimal import Decimal
import json

# Import from VzrdClothing package
from VzrdClothing.models_db import db, Product, Customer, Order, OrderItem, Contact, Newsletter, User, Favorite
from forms import LoginForm, RegisterForm, ProfileForm, ProductForm, OrderStatusForm, SearchForm

logging.basicConfig(level=logging.DEBUG)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "vzrd-secret-key-2024")
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

with app.app_context():
    try:
        db.create_all()
        
        # Initialize database with sample products if empty
        if Product.query.count() == 0:
            sample_products = [
            Product(
                name='VZRD Essential Oversized Tee',
                description='Camiseta oversized premium com ajuste moderno e tecido de alta qualidade. Perfeita para o dia a dia urbano.',
                price=89.90,
                image_url='https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
                category='oversized',
                size_options='P,M,G,GG,XG',
                stock_quantity=25,
                featured=True,
                in_stock=True
            ),
            Product(
                name='Urban Flow Oversized',
                description='Camiseta streetwear com blend de algodão premium. Design urbano para quem vive a cultura das ruas.',
                price=95.90,
                image_url='https://images.unsplash.com/photo-1576566588028-4147f3842f27?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
                category='oversized',
                size_options='P,M,G,GG,XG',
                stock_quantity=30,
                featured=True,
                in_stock=True
            ),
            Product(
                name='VZRD Signature Drop',
                description='Edição limitada da coleção assinatura VZRD. Exclusividade e estilo em uma peça única.',
                price=99.90,
                image_url='https://images.unsplash.com/photo-1583743814966-8936f37f0d2f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
                category='oversized',
                size_options='P,M,G,GG,XG',
                stock_quantity=15,
                featured=False,
                in_stock=True
            ),
            Product(
                name='Minimalist Oversized',
                description='Design minimalista com conforto oversized. Menos é mais no streetwear contemporâneo.',
                price=85.90,
                image_url='https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
                category='oversized',
                size_options='P,M,G,GG,XG',
                stock_quantity=40,
                featured=False,
                in_stock=True
            ),
            Product(
                name='Street Culture Tee',
                description='Declaração audaciosa do streetwear com silhueta oversized. Para quem não tem medo de se expressar.',
                price=92.90,
                image_url='https://images.unsplash.com/photo-1618354691373-d851c5c3a990?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
                category='oversized',
                size_options='P,M,G,GG,XG',
                stock_quantity=20,
                featured=True,
                in_stock=True
            ),
            Product(
                name='VZRD Classic Black',
                description='Camiseta preta clássica oversized, perfeita para qualquer look. O básico que nunca sai de moda.',
                price=88.90,
                image_url='https://images.unsplash.com/photo-1503341504253-dff4815485f1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
                category='oversized',
                size_options='P,M,G,GG,XG',
                stock_quantity=50,
                featured=False,
                in_stock=True
            ),
            Product(
                name='Premium Cotton Drop',
                description='Algodão ultra-premium em camiseta oversized. Qualidade superior para quem exige o melhor.',
                price=105.90,
                image_url='https://images.unsplash.com/photo-1571945153237-4929e783af4a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
                category='oversized',
                size_options='P,M,G,GG,XG',
                stock_quantity=12,
                featured=False,
                in_stock=True
            ),
            Product(
                name='Artistic Expression Tee',
                description='Design artístico encontra conforto oversized. Arte vestível para expressão autêntica.',
                price=97.90,
                image_url='https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
                category='oversized',
                size_options='P,M,G,GG,XG',
                stock_quantity=18,
                featured=False,
                in_stock=True
            )
        ]
        
            for product in sample_products:
                db.session.add(product)
            
            db.session.commit()
            print("VZRD Database initialized with sample products")
    except Exception as e:
        print(f"Database initialization error: {e}")
        print("Application will continue but some features may not work properly")

# ============================================
# MAIN ROUTES
# ============================================

@app.route('/')
def index():
    try:
        featured_products = Product.query.filter_by(featured=True, in_stock=True).all()
        featured_products_dict = [product.to_dict() for product in featured_products]
        return render_template('index.html', featured_products=featured_products_dict)
    except Exception as e:
        print(f"Database error in index route: {e}")
        return render_template('index.html', featured_products=[])

@app.route('/produtos')
def produtos():
    try:
        products = Product.query.filter_by(in_stock=True).all()
        products_dict = [product.to_dict() for product in products]
        return render_template('produtos.html', products=products_dict)
    except Exception as e:
        print(f"Database error in produtos route: {e}")
        return render_template('produtos.html', products=[])



@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            subject = request.form.get('subject', 'Contato do Site')
            
            if name and email and message:
                contact = Contact(name=name, email=email, message=message, subject=subject)
                db.session.add(contact)
                db.session.commit()
                flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
            else:
                flash('Por favor, preencha todos os campos obrigatórios.', 'error')
        except Exception as e:
            print(f"Error saving contact: {e}")
            flash('Erro ao enviar mensagem. Tente novamente.', 'error')
        
        return redirect(url_for('contato'))
    
    return render_template('contato.html')

# ============================================
# API ROUTES - CART & SHOPPING
# ============================================

@app.route('/api/newsletter', methods=['POST'])
def subscribe_newsletter():
    try:
        email = request.form.get('email') or request.json.get('email')
        if not email:
            return jsonify({'success': False, 'message': 'Email é obrigatório'}), 400
        
        # Check if email already exists
        existing = Newsletter.query.filter_by(email=email).first()
        if existing:
            if existing.active:
                return jsonify({'success': False, 'message': 'Email já cadastrado'}), 400
            else:
                existing.active = True
                db.session.commit()
                return jsonify({'success': True, 'message': 'Newsletter reativada com sucesso!'})
        
        newsletter = Newsletter(email=email)
        db.session.add(newsletter)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Inscrição realizada com sucesso!'})
    except Exception as e:
        print(f"Error subscribing to newsletter: {e}")
        return jsonify({'success': False, 'message': 'Erro ao processar inscrição'}), 500

@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({'success': True, 'product': product.to_dict()})
    except Exception as e:
        print(f"Error getting product: {e}")
        return jsonify({'success': False, 'message': 'Produto não encontrado'}), 404

@app.route('/api/create-order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer_name', 'customer_email', 'customer_phone', 'items']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Calculate total amount from items
        total_amount = 0
        order_items_data = []
        
        for item in data['items']:
            product = Product.query.get(item['product_id'])
            if not product or not product.in_stock:
                return jsonify({'error': f'Produto {item["product_id"]} não disponível'}), 400
            
            # Check stock
            if product.stock_quantity < item['quantity']:
                return jsonify({'error': f'Estoque insuficiente para {product.name}'}), 400
            
            item_total = float(product.price) * item['quantity']
            total_amount += item_total
            
            order_items_data.append({
                'product_id': product.id,
                'product_name': product.name,
                'size': item['size'],
                'quantity': item['quantity'],
                'unit_price': float(product.price)
            })
        
        # Create or get customer
        customer = Customer.query.filter_by(email=data['customer_email']).first()
        if not customer:
            customer = Customer(
                name=data['customer_name'],
                email=data['customer_email'],
                phone=data['customer_phone'],
                address=data.get('customer_address'),
                city=data.get('customer_city'),
                state=data.get('customer_state'),
                zipcode=data.get('customer_zipcode')
            )
            db.session.add(customer)
            db.session.flush()
        
        # Create order
        order = Order(
            customer_id=customer.id,
            total_amount=Decimal(str(total_amount)),
            status='pending',
            shipping_address=data.get('customer_address'),
            notes=data.get('notes')
        )
        
        db.session.add(order)
        db.session.flush()
        
        # Add order items and update stock
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                size=item_data['size'],
                unit_price=Decimal(str(item_data['unit_price']))
            )
            db.session.add(order_item)
            
            # Update product stock
            product = Product.query.get(item_data['product_id'])
            product.stock_quantity -= item_data['quantity']
            if product.stock_quantity <= 0:
                product.in_stock = False
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'order_id': order.id,
            'total_amount': total_amount,
            'message': 'Pedido criado com sucesso!'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating order: {e}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/pedido/<int:order_id>')
def order_success(order_id):
    try:
        order = Order.query.get_or_404(order_id)
        return render_template('order_success.html', order=order.to_dict())
    except Exception as e:
        print(f"Error loading order: {e}")
        flash('Pedido não encontrado.', 'error')
        return redirect(url_for('index'))

# ============================================
# ADMIN ROUTES
# ============================================

@app.route('/admin')
def admin_dashboard():
    try:
        stats = {
            'total_products': Product.query.count(),
            'total_orders': Order.query.count(),
            'total_customers': Customer.query.count(),
            'newsletter_subscribers': Newsletter.query.filter_by(active=True).count(),
            'pending_orders': Order.query.filter_by(status='pending').count(),
            'low_stock_products': Product.query.filter(Product.stock_quantity <= 5).count()
        }
        
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        low_stock_products = Product.query.filter(Product.stock_quantity <= 5).all()
        
        return render_template('admin/dashboard.html', 
                             stats=stats, 
                             recent_orders=[order.to_dict() for order in recent_orders],
                             low_stock_products=[product.to_dict() for product in low_stock_products])
    except Exception as e:
        print(f"Error loading admin dashboard: {e}")
        return render_template('admin/dashboard.html', 
                             stats={}, recent_orders=[], low_stock_products=[])

@app.route('/admin/produtos')
def admin_products():
    try:
        products = Product.query.all()
        return render_template('admin/products.html', products=[p.to_dict() for p in products])
    except Exception as e:
        print(f"Error loading admin products: {e}")
        return render_template('admin/products.html', products=[])

@app.route('/admin/pedidos')
def admin_orders():
    try:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        return render_template('admin/orders.html', orders=[order.to_dict() for order in orders])
    except Exception as e:
        print(f"Error loading admin orders: {e}")
        return render_template('admin/orders.html', orders=[])

@app.route('/admin/contatos')
def admin_contacts():
    try:
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
        return render_template('admin/contacts.html', contacts=contacts)
    except Exception as e:
        print(f"Error loading admin contacts: {e}")
        return render_template('admin/contacts.html', contacts=[])

@app.route('/admin/newsletter')
def admin_newsletter():
    try:
        subscribers = Newsletter.query.filter_by(active=True).all()
        return render_template('admin/newsletter.html', subscribers=subscribers)
    except Exception as e:
        print(f"Error loading admin newsletter: {e}")
        return render_template('admin/newsletter.html', subscribers=[])

# ============================================
# SMS NOTIFICATION ROUTE
# ============================================

@app.route('/api/send-sms', methods=['POST'])
def send_sms():
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials from environment
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_phone = os.environ.get('TWILIO_PHONE')
        
        if not all([account_sid, auth_token, twilio_phone]):
            return jsonify({'success': False, 'message': 'Twilio não configurado'}), 400
        
        data = request.get_json()
        phone = data.get('phone')
        message = data.get('message')
        
        if not phone or not message:
            return jsonify({'success': False, 'message': 'Telefone e mensagem são obrigatórios'}), 400
        
        # Format phone number (add +55 if not present)
        if not phone.startswith('+'):
            phone = '+55' + phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send SMS
        message_obj = client.messages.create(
            body=message,
            from_=twilio_phone,
            to=phone
        )
        
        return jsonify({
            'success': True, 
            'message': 'SMS enviado com sucesso',
            'sid': message_obj.sid
        })
        
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return jsonify({'success': False, 'message': f'Erro ao enviar SMS: {str(e)}'}), 500

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
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Produto não encontrado'}), 404
        
        # Check if already favorited
        favorite = Favorite.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if favorite:
            # Remove from favorites
            db.session.delete(favorite)
            is_favorited = False
            message = 'Produto removido dos favoritos'
        else:
            # Add to favorites
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
        
        # Check if favorited by current user
        is_favorited = False
        if current_user.is_authenticated:
            favorite = Favorite.query.filter_by(
                user_id=current_user.id, 
                product_id=product_id
            ).first()
            is_favorited = favorite is not None
        
        # Get related products (same category)
        related_products = Product.query.filter(
            Product.category == product.category,
            Product.id != product_id,
            Product.in_stock == True
        ).limit(4).all()
        
        return render_template('product_detail.html', 
                             product=product,
                             is_favorited=is_favorited,
                             related_products=related_products)
    except Exception as e:
        print(f"Error loading product detail: {e}")
        flash('Produto não encontrado.', 'error')
        return redirect(url_for('produtos'))

# ============================================
# SEARCH API ROUTE
# ============================================

@app.route('/api/search')
def search_api():
    try:
        query = request.args.get('query', '')
        category = request.args.get('category', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Start with base query
        products_query = Product.query.filter_by(in_stock=True)
        
        # Apply filters
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
        
        # Convert to dict for JSON response
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
# ENHANCED ADMIN ROUTES
# ============================================

@app.route('/admin')
@login_required
def admin_dashboard():
    # Check if user is admin
    if not (current_user.is_admin or current_user.email == 'admin@vzrd.com'):
        flash('Acesso negado. Apenas administradores.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Get statistics
        total_products = Product.query.count()
        total_orders = Order.query.count()
        total_users = User.query.count()
        pending_orders = Order.query.filter_by(status='pending').count()
        
        # Recent orders
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        
        # Low stock products (check if stock_quantity field exists)
        try:
            low_stock_products = Product.query.filter(Product.stock_quantity <= 5).all()
        except:
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
            
            # Add stock_quantity if field exists
            try:
                product.stock_quantity = form.stock_quantity.data
                product.size_options = form.size_options.data
            except:
                pass
            
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

def send_new_order_admin_notification(order):
    """Send SMS notification to admin when new order is created"""
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_phone = os.environ.get('TWILIO_PHONE')
        admin_phone = os.environ.get('ADMIN_PHONE')
        
        if not all([account_sid, auth_token, twilio_phone, admin_phone]):
            print("Twilio or admin phone not configured")
            return
        
        # Create message
        customer_name = order.get_customer_name()
        message = f"🆕 VZRD - Novo pedido #{order.id}\nCliente: {customer_name}\nTotal: R$ {order.total_amount}\n\nVer detalhes: {request.url_root}admin/orders/{order.id}"
        
        # Send SMS
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=twilio_phone,
            to=admin_phone
        )
        
        print(f"Admin notification sent for order {order.id}")
        
    except Exception as e:
        print(f"Error sending admin notification SMS: {e}")

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
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Produto não encontrado'}), 404
        
        # Check if already favorited
        favorite = Favorite.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if favorite:
            # Remove from favorites
            db.session.delete(favorite)
            is_favorited = False
            message = 'Produto removido dos favoritos'
        else:
            # Add to favorites
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
        
        # Check if favorited by current user
        is_favorited = False
        if current_user.is_authenticated:
            favorite = Favorite.query.filter_by(
                user_id=current_user.id, 
                product_id=product_id
            ).first()
            is_favorited = favorite is not None
        
        # Get related products (same category)
        related_products = Product.query.filter(
            Product.category == product.category,
            Product.id != product_id,
            Product.in_stock == True
        ).limit(4).all()
        
        return render_template('product_detail.html', 
                             product=product,
                             is_favorited=is_favorited,
                             related_products=related_products)
    except Exception as e:
        print(f"Error loading product detail: {e}")
        flash('Produto não encontrado.', 'error')
        return redirect(url_for('produtos'))

# ============================================
# SEARCH API ROUTE
# ============================================

@app.route('/api/search')
def search_api():
    try:
        query = request.args.get('query', '')
        category = request.args.get('category', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Start with base query
        products_query = Product.query.filter_by(in_stock=True)
        
        # Apply filters
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
        
        # Convert to dict for JSON response
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
# ENHANCED ADMIN ROUTES
# ============================================

@app.route('/admin')
@login_required
def admin_dashboard():
    # Check if user is admin (you can implement proper admin check)
    if not (current_user.is_admin or current_user.email == 'admin@vzrd.com'):
        flash('Acesso negado. Apenas administradores.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Get statistics
        total_products = Product.query.count()
        total_orders = Order.query.count()
        total_users = User.query.count()
        pending_orders = Order.query.filter_by(status='pending').count()
        
        # Recent orders
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        
        # Low stock products
        low_stock_products = Product.query.filter(Product.stock_quantity <= 5).all()
        
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
        flash('Acesso negado. Apenas administradores.', 'error')
        return redirect(url_for('index'))
    
    try:
        products = Product.query.order_by(Product.created_at.desc()).all()
        return render_template('admin/products.html', products=products)
    except Exception as e:
        print(f"Error loading admin products: {e}")
        return render_template('admin/products.html', products=[])

@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if not (current_user.is_admin or current_user.email == 'admin@vzrd.com'):
        flash('Acesso negado. Apenas administradores.', 'error')
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
                size_options=form.size_options.data,
                stock_quantity=form.stock_quantity.data,
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
        flash('Acesso negado. Apenas administradores.', 'error')
        return redirect(url_for('index'))
    
    try:
        status = request.args.get('status', '')
        orders_query = Order.query
        
        if status:
            orders_query = orders_query.filter_by(status=status)
        
        orders = orders_query.order_by(Order.created_at.desc()).all()
        return render_template('admin/orders.html', orders=orders, current_status=status)
    except Exception as e:
        print(f"Error loading admin orders: {e}")
        return render_template('admin/orders.html', orders=[], current_status='')

@app.route('/admin/orders/<int:order_id>', methods=['GET', 'POST'])
@login_required
def admin_order_detail(order_id):
    if not (current_user.is_admin or current_user.email == 'admin@vzrd.com'):
        flash('Acesso negado. Apenas administradores.', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    form = OrderStatusForm(obj=order)
    
    if form.validate_on_submit():
        try:
            old_status = order.status
            order.status = form.status.data
            order.tracking_number = form.tracking_number.data
            order.admin_notes = form.admin_notes.data
            
            db.session.commit()
            
            # Send SMS notification if status changed to shipped
            if old_status != 'shipped' and form.status.data == 'shipped':
                send_order_status_sms(order)
            
            flash('Pedido atualizado com sucesso!', 'success')
            return redirect(url_for('admin_orders'))
        except Exception as e:
            db.session.rollback()
            print(f"Error updating order: {e}")
            flash('Erro ao atualizar pedido.', 'error')
    
    return render_template('admin/order_detail.html', order=order, form=form)

def send_order_status_sms(order):
    """Send SMS notification when order status changes"""
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_phone = os.environ.get('TWILIO_PHONE')
        
        if not all([account_sid, auth_token, twilio_phone]):
            print("Twilio not configured for SMS notifications")
            return
        
        # Get customer phone
        customer_phone = None
        if order.user_id and order.user.phone:
            customer_phone = order.user.phone
        elif order.customer_id and order.customer.phone:
            customer_phone = order.customer.phone
        
        if not customer_phone:
            print("No phone number available for SMS notification")
            return
        
        # Format phone number
        if not customer_phone.startswith('+'):
            customer_phone = '+55' + customer_phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Create message
        tracking_info = f"\nRastreamento: {order.tracking_number}" if order.tracking_number else ""
        message = f"🎉 VZRD - Seu pedido #{order.id} foi enviado!{tracking_info}\n\nAcompanhe em: {request.url_root}pedido/{order.id}"
        
        # Send SMS
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=twilio_phone,
            to=customer_phone
        )
        
        print(f"SMS sent to {customer_phone} for order {order.id}")
        
    except Exception as e:
        print(f"Error sending order status SMS: {e}")

def send_new_order_admin_notification(order):
    """Send SMS notification to admin when new order is created"""
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_phone = os.environ.get('TWILIO_PHONE')
        admin_phone = os.environ.get('ADMIN_PHONE')
        
        if not all([account_sid, auth_token, twilio_phone, admin_phone]):
            print("Twilio or admin phone not configured")
            return
        
        # Create message
        customer_name = order.get_customer_name()
        message = f"🆕 VZRD - Novo pedido #{order.id}\nCliente: {customer_name}\nTotal: R$ {order.total_amount}\n\nVer detalhes: {request.url_root}admin/orders/{order.id}"
        
        # Send SMS
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=twilio_phone,
            to=admin_phone
        )
        
        print(f"Admin notification sent for order {order.id}")
        
    except Exception as e:
        print(f"Error sending admin notification SMS: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)