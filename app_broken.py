import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from decimal import Decimal
import json

# Import from VzrdClothing package
from VzrdClothing.models_db import db, Product, Customer, Order, OrderItem, Contact, Newsletter

logging.basicConfig(level=logging.DEBUG)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "vzrd-secret-key-2024")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

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

@app.route('/produto/<int:product_id>')
def product_detail(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        if not product.in_stock:
            flash('Produto indisponível no momento.', 'error')
            return redirect(url_for('produtos'))
        
        # Get related products (same category, excluding current product)
        related_products = Product.query.filter(
            Product.category == product.category,
            Product.id != product_id,
            Product.in_stock == True
        ).limit(4).all()
        
        related_products_dict = [p.to_dict() for p in related_products]
        
        return render_template('produto_detalhes.html', 
                             product=product.to_dict(), 
                             related_products=related_products_dict)
    except Exception as e:
        print(f"Database error in product_detail route: {e}")
        flash('Erro ao carregar produto.', 'error')
        return redirect(url_for('produtos'))

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
    
    # Get related products (same category, excluding current product)
    related_products = models.Product.query.filter(
        models.Product.category == product.category,
        models.Product.id != product_id,
        models.Product.in_stock == True
    ).limit(4).all()
    
    related_products_dict = [p.to_dict() for p in related_products]
    
    return render_template('produto_detalhes.html', 
                         product=product.to_dict(), 
                         related_products=related_products_dict)

@app.route('/api/newsletter', methods=['POST'])
def subscribe_newsletter():
    email = request.form.get('email')
    if not email:
        return {'success': False, 'message': 'Email é obrigatório'}, 400
    
    # Check if email already exists
    existing = models.Newsletter.query.filter_by(email=email).first()
    if existing:
        if existing.active:
            return {'success': False, 'message': 'Email já cadastrado'}, 400
        else:
            existing.active = True
            db.session.commit()
            return {'success': True, 'message': 'Newsletter reativada com sucesso!'}
    
    newsletter = models.Newsletter(email=email)
    db.session.add(newsletter)
    db.session.commit()
    return {'success': True, 'message': 'Inscrição realizada com sucesso!'}

@app.route('/admin/products')
def admin_products():
    products = models.Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/contacts')
def admin_contacts():
    contacts = models.Contact.query.order_by(models.Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

@app.route('/admin/newsletter')
def admin_newsletter():
    subscribers = models.Newsletter.query.filter_by(active=True).all()
    return render_template('admin/newsletter.html', subscribers=subscribers)

# ============================================
# PAYMENT SYSTEM ROUTES
# ============================================

@app.route('/checkout')
def checkout():
    return render_template('checkout.html', mercadopago_public_key=os.environ.get("MERCADOPAGO_PUBLIC_KEY"))

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
        order_items = []
        
        for item in data['items']:
            product = models.Product.query.get(item['product_id'])
            if not product or not product.in_stock:
                return jsonify({'error': f'Produto {item["product_id"]} não disponível'}), 400
            
            item_total = float(product.price) * item['quantity']
            total_amount += item_total
            
            order_items.append({
                'product_id': product.id,
                'product_name': product.name,
                'size': item['size'],
                'quantity': item['quantity'],
                'unit_price': float(product.price)
            })
        
        # Create order in database
        order = models.Order(
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            customer_phone=data['customer_phone'],
            customer_address=data.get('customer_address'),
            customer_city=data.get('customer_city'),
            customer_state=data.get('customer_state'),
            customer_zipcode=data.get('customer_zipcode'),
            total_amount=Decimal(str(total_amount)),
            status='pending'
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Add order items
        for item_data in order_items:
            order_item = models.OrderItem(
                order_id=order.id,
                product_id=item_data['product_id'],
                product_name=item_data['product_name'],
                size=item_data['size'],
                quantity=item_data['quantity'],
                unit_price=Decimal(str(item_data['unit_price']))
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'order_id': order.id,
            'total_amount': total_amount
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/create-payment', methods=['POST'])
def create_payment():
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        payment_method = data.get('payment_method')
        
        order = models.Order.query.get_or_404(order_id)
        
        # Create Mercado Pago preference
        preference_data = {
            "items": [
                {
                    "title": f"VZRD - Pedido #{order.id}",
                    "quantity": 1,
                    "unit_price": float(order.total_amount),
                    "currency_id": "BRL"
                }
            ],
            "payer": {
                "name": order.customer_name,
                "email": order.customer_email,
                "phone": {
                    "number": order.customer_phone
                }
            },
            "back_urls": {
                "success": request.host_url + f"payment/success/{order.id}",
                "failure": request.host_url + f"payment/failure/{order.id}",
                "pending": request.host_url + f"payment/pending/{order.id}"
            },
            "auto_return": "approved",
            "external_reference": str(order.id),
            "notification_url": request.host_url + "api/payment/webhook",
            "statement_descriptor": "VZRD STREETWEAR"
        }
        
        # Set payment methods based on selection
        if payment_method == 'pix':
            preference_data["payment_methods"] = {
                "excluded_payment_methods": [{"id": "visa"}, {"id": "master"}, {"id": "amex"}],
                "excluded_payment_types": [{"id": "credit_card"}, {"id": "debit_card"}],
                "installments": 1
            }
        elif payment_method == 'credit_card':
            preference_data["payment_methods"] = {
                "excluded_payment_methods": [{"id": "pix"}],
                "excluded_payment_types": [{"id": "bank_transfer"}],
                "installments": 12
            }
        elif payment_method == 'boleto':
            preference_data["payment_methods"] = {
                "excluded_payment_methods": [{"id": "visa"}, {"id": "master"}, {"id": "amex"}, {"id": "pix"}],
                "excluded_payment_types": [{"id": "credit_card"}, {"id": "debit_card"}],
                "installments": 1
            }
        
        preference_response = mp.preference().create(preference_data)
        
        if preference_response["status"] == 201:
            preference = preference_response["response"]
            
            # Update order with preference info
            order.preference_id = preference["id"]
            order.payment_method = payment_method
            db.session.commit()
            
            return jsonify({
                'success': True,
                'preference_id': preference["id"],
                'init_point': preference["init_point"],
                'sandbox_init_point': preference.get("sandbox_init_point")
            })
        else:
            return jsonify({'error': 'Erro ao criar preferência de pagamento'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/payment/webhook', methods=['POST'])
def payment_webhook():
    try:
        data = request.get_json()
        
        if data.get("type") == "payment":
            payment_id = data["data"]["id"]
            
            # Get payment details from Mercado Pago
            payment_info = mp.payment().get(payment_id)
            
            if payment_info["status"] == 200:
                payment = payment_info["response"]
                external_reference = payment.get("external_reference")
                
                if external_reference:
                    order = models.Order.query.get(int(external_reference))
                    if order:
                        # Update order payment status
                        order.payment_id = str(payment_id)
                        order.payment_status = payment["status"]
                        
                        if payment["status"] == "approved":
                            order.status = "paid"
                        elif payment["status"] == "pending":
                            order.status = "pending_payment"
                        elif payment["status"] in ["cancelled", "rejected"]:
                            order.status = "payment_failed"
                        
                        db.session.commit()
        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return jsonify({'status': 'error'}), 500

@app.route('/payment/success/<int:order_id>')
def payment_success(order_id):
    order = models.Order.query.get_or_404(order_id)
    return render_template('payment_result.html', order=order, status='success')

@app.route('/payment/failure/<int:order_id>')
def payment_failure(order_id):
    order = models.Order.query.get_or_404(order_id)
    return render_template('payment_result.html', order=order, status='failure')

@app.route('/payment/pending/<int:order_id>')
def payment_pending(order_id):
    order = models.Order.query.get_or_404(order_id)
    return render_template('payment_result.html', order=order, status='pending')

@app.route('/admin/orders')
def admin_orders():
    orders = models.Order.query.order_by(models.Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
