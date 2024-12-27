import os
import csv
import uuid
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_file,
    flash,
    session
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace_with_a_secure_random_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///camping_gear.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# For image uploads
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)


# ------------------------------------------------------------------------------
# Database Model
# ------------------------------------------------------------------------------
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    weight = db.Column(db.String(50), nullable=True)
    season = db.Column(db.String(50), nullable=True)
    keywords = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    image_path = db.Column(db.String(200), nullable=True)
    url = db.Column(db.String(200), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"<Item {self.name}>"


# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------
def generate_item_number():
    """
    Generates a unique item number. 
    You could also use sequences, UUID4, or other strategies as needed.
    """
    return str(uuid.uuid4())[:8]


# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------




@app.route('/')
def home():
    """
    Show the list of items with the ability to select items for a checklist.
    """
    items = Item.query.all()
    return render_template('index.html', items=items)


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """
    Add a new item to the database.
    """
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        description = request.form.get('description')
        weight = request.form.get('weight')
        season = request.form.get('season')
        keywords = request.form.get('keywords')
        category = request.form.get('category')
        url = request.form.get('url')
        quantity = request.form.get('quantity', 1, type=int)

        # Handle image upload
        image = request.files.get('image')
        image_path = None
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Generate unique item number
        item_number = generate_item_number()

        # Create the Item instance
        new_item = Item(
            item_number=item_number,
            name=name,
            description=description,
            weight=weight,
            season=season,
            keywords=keywords,
            category=category,
            image_path=image_path,
            url=url,
            quantity=quantity
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!', 'success')
        return redirect(url_for('home'))

    # GET request => Show add form
    return render_template('add_item.html')


@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    """
    Edit an existing item in the database.
    """
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        # Update item data
        item.name = request.form.get('name')
        item.description = request.form.get('description')
        item.weight = request.form.get('weight')
        item.season = request.form.get('season')
        item.keywords = request.form.get('keywords')
        item.category = request.form.get('category')
        item.url = request.form.get('url')
        item.quantity = request.form.get('quantity', 1, type=int)

        # Handle image upload if new file provided
        image = request.files.get('image')
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item.image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        db.session.commit()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_item.html', item=item)


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    """
    Delete an item from the database.
    """
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/export_csv')
def export_csv():
    """
    Export all items to a CSV file and serve it as a download.
    """
    items = Item.query.all()
    csv_filename = 'camping_items.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow([
            'item_number', 'name', 'description', 'weight',
            'season', 'keywords', 'category', 'image_path',
            'url', 'quantity'
        ])
        # Write item rows
        for item in items:
            writer.writerow([
                item.item_number,
                item.name,
                item.description,
                item.weight,
                item.season,
                item.keywords,
                item.category,
                item.image_path if item.image_path else '',
                item.url if item.url else '',
                item.quantity
            ])

    return send_file(
        csv_filename,
        mimetype='text/csv',
        as_attachment=True,
        attachment_filename=csv_filename
    )


@app.route('/import_csv', methods=['GET', 'POST'])
def import_csv():
    """
    Import items from an uploaded CSV file.
    """
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('No file selected!', 'danger')
            return redirect(url_for('import_csv'))

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if item_number already exists
                existing_item = Item.query.filter_by(item_number=row['item_number']).first()
                if existing_item:
                    # Update existing item if you want that behavior, or skip
                    existing_item.name = row['name']
                    existing_item.description = row['description']
                    existing_item.weight = row['weight']
                    existing_item.season = row['season']
                    existing_item.keywords = row['keywords']
                    existing_item.category = row['category']
                    existing_item.image_path = row['image_path']
                    existing_item.url = row['url']
                    existing_item.quantity = int(row['quantity'])
                else:
                    # Create new item
                    new_item = Item(
                        item_number=row['item_number'],
                        name=row['name'],
                        description=row['description'],
                        weight=row['weight'],
                        season=row['season'],
                        keywords=row['keywords'],
                        category=row['category'],
                        image_path=row['image_path'],
                        url=row['url'],
                        quantity=int(row['quantity'])
                    )
                    db.session.add(new_item)
        db.session.commit()

        os.remove(filepath)  # Clean up after import
        flash('Items imported successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('import_csv.html')


@app.route('/checklist', methods=['POST'])
def generate_checklist():
    """
    Generate a printable checklist of selected items.
    """
    # 'selected_items' will be a list of item IDs as strings
    selected_items_ids = request.form.getlist('selected_items')
    # Retrieve item objects
    selected_items = Item.query.filter(Item.id.in_(selected_items_ids)).all()
    return render_template('checklist.html', selected_items=selected_items)


# ------------------------------------------------------------------------------
# Templates (Inline for demonstration, but you can put them in a /templates folder)
# ------------------------------------------------------------------------------
# We’ll store them in separate .html files in the templates folder:
#   - base.html
#   - index.html
#   - add_item.html
#   - edit_item.html
#   - import_csv.html
#   - checklist.html
#
# For brevity, sample minimal template contents are provided below.

# ------------------------------------------------------------------------------
# Run the App
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
