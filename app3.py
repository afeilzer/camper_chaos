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
    flash
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
# Models
# ------------------------------------------------------------------------------
class Item(db.Model):
    """Represents a single piece of camping gear."""
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


class PackList(db.Model):
    """Represents a named packlist, which can hold many items."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relationship to PackListItem (the join table)
    items = db.relationship('PackListItem', backref='packlist', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<PackList {self.name}>"


class PackListItem(db.Model):
    """Join table associating PackList and Item, possibly with a quantity."""
    id = db.Column(db.Integer, primary_key=True)
    packlist_id = db.Column(db.Integer, db.ForeignKey('pack_list.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    
    # Optionally store the quantity of this item specifically in this packlist
    item_quantity = db.Column(db.Integer, default=1)

    # Relationship to Item
    item = db.relationship('Item')

    def __repr__(self):
        return f"<PackListItem packlist={self.packlist_id} item={self.item_id}>"


# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------
def generate_item_number():
    """Generates a unique item number."""
    return str(uuid.uuid4())[:8]





# ------------------------------------------------------------------------------
# Routes for Items
# ------------------------------------------------------------------------------
@app.route('/')
def home():
    """
    Show the list of items with optional sorting and filtering.
    Also display a dropdown of existing packlists to add items to.
    """
    # 1. Grab sort parameters from query string
    sort_col = request.args.get('sort', 'id')   # default to 'id'
    sort_order = request.args.get('order', 'asc')

    # 2. Grab filter parameter
    filter_text = request.args.get('filter_text', '').strip()

    # 3. Build query
    query = Item.query

    # 4. Apply filter if provided
    if filter_text:
        query = query.filter(
            (Item.name.ilike(f'%{filter_text}%')) |
            (Item.category.ilike(f'%{filter_text}%')) |
            (Item.season.ilike(f'%{filter_text}%'))
        )

    # 5. Validate the column requested for sorting
    valid_sort_columns = {
        'id': Item.id,
        'name': Item.name,
        'weight': Item.weight,
        'season': Item.season,
        'category': Item.category,
        'quantity': Item.quantity,
    }
    sort_column = valid_sort_columns.get(sort_col, Item.id)

    # 6. Apply sorting
    if sort_order == 'desc':
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # 7. Execute query
    items = query.all()

    # 8. Retrieve existing PackLists for the dropdown
    packlists = PackList.query.order_by(PackList.name.asc()).all()

    # 9. Render template, passing sorting/filter info for the UI
    return render_template(
        'index.html',
        items=items,
        packlists=packlists,
        filter_text=filter_text,
        sort_col=sort_col,
        sort_order=sort_order
    )


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """
    Add a new item to the database.
    """
    if request.method == 'POST':
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

    return render_template('add_item.html')


@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    """
    Edit an existing item.
    """
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.description = request.form.get('description')
        item.weight = request.form.get('weight')
        item.season = request.form.get('season')
        item.keywords = request.form.get('keywords')
        item.category = request.form.get('category')
        item.url = request.form.get('url')
        item.quantity = request.form.get('quantity', 1, type=int)

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
    Delete an item.
    """
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('home'))


# ------------------------------------------------------------------------------
# CSV Import/Export (unchanged from your previous logic, except minor detail)
# ------------------------------------------------------------------------------
@app.route('/export_csv')
def export_csv():
    items = Item.query.all()
    csv_filename = 'camping_items.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'item_number', 'name', 'description', 'weight',
            'season', 'keywords', 'category', 'image_path',
            'url', 'quantity'
        ])
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
        download_name=csv_filename
    )


@app.route('/import_csv', methods=['GET', 'POST'])
def import_csv():
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
                existing_item = Item.query.filter_by(item_number=row['item_number']).first()
                if existing_item:
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

        os.remove(filepath)
        flash('Items imported successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('import_csv.html')


# ------------------------------------------------------------------------------
# Routes for PackLists
# ------------------------------------------------------------------------------
@app.route('/packlists')
def view_packlists():
    """
    Show a list of all packlists.
    """
    packlists = PackList.query.order_by(PackList.name.asc()).all()
    return render_template('packlists.html', packlists=packlists)


@app.route('/packlist/create', methods=['GET', 'POST'])
def create_packlist():
    """
    Create a new, named packlist.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('Packlist name is required.', 'danger')
            return redirect(url_for('create_packlist'))
        
        packlist = PackList(name=name)
        db.session.add(packlist)
        db.session.commit()
        flash('Packlist created!', 'success')
        return redirect(url_for('view_packlists'))
    
    return render_template('create_packlist.html')


@app.route('/packlist/<int:packlist_id>')
def show_packlist(packlist_id):
    """
    Show a 2-column layout of the items in this packlist.  
    The template itself will handle the 2-column display.
    """
    packlist = PackList.query.get_or_404(packlist_id)
    return render_template('show_packlist.html', packlist=packlist)


@app.route('/packlist/<int:packlist_id>/delete', methods=['POST'])
def delete_packlist(packlist_id):
    """
    Delete a packlist (and its associated items).
    """
    packlist = PackList.query.get_or_404(packlist_id)
    db.session.delete(packlist)
    db.session.commit()
    flash('Packlist deleted.', 'success')
    return redirect(url_for('view_packlists'))


@app.route('/packlist/<int:packlist_id>/clear', methods=['POST'])
def clear_packlist(packlist_id):
    """
    Remove all items from an existing packlist (but keep the packlist itself).
    """
    packlist = PackList.query.get_or_404(packlist_id)
    # This deletes all PackListItem rows for this packlist
    PackListItem.query.filter_by(packlist_id=packlist.id).delete()
    db.session.commit()
    flash('All items removed from the packlist.', 'success')
    return redirect(url_for('show_packlist', packlist_id=packlist.id))


@app.route('/add_to_packlist', methods=['POST'])
def add_to_packlist():
    """
    From the main page, user can select items and pick a packlist (existing or new).
    This route handles that form submission and adds the items to the chosen packlist.
    """
    # The 'packlist_id' is passed as a hidden form field or from a dropdown.
    packlist_id = request.form.get('packlist_id', type=int)
    if not packlist_id:
        flash('No packlist selected!', 'danger')
        return redirect(url_for('home'))

    # The checkboxes (selected_items) are item IDs from the home page
    selected_items = request.form.getlist('selected_items')
    
    # If none selected, just redirect
    if not selected_items:
        flash('No items selected!', 'warning')
        return redirect(url_for('home'))

    packlist = PackList.query.get_or_404(packlist_id)
    # For each item ID, if it's not already in the packlist, add it
    for item_id_str in selected_items:
        item_id = int(item_id_str)
        existing_rel = PackListItem.query.filter_by(packlist_id=packlist_id, item_id=item_id).first()
        if not existing_rel:
            # Create the association
            new_packlist_item = PackListItem(packlist_id=packlist_id, item_id=item_id)
            db.session.add(new_packlist_item)

    db.session.commit()
    flash('Items added to packlist!', 'success')
    return redirect(url_for('show_packlist', packlist_id=packlist_id))


@app.route('/packlist/<int:packlist_id>/remove_item/<int:packlist_item_id>', methods=['POST'])
def remove_item_from_packlist(packlist_id, packlist_item_id):
    """
    Remove a single item from a packlist.
    """
    packlist_item = PackListItem.query.get_or_404(packlist_item_id)
    if packlist_item.packlist_id != packlist_id:
        flash("Item doesn't belong to this packlist.", 'danger')
        return redirect(url_for('show_packlist', packlist_id=packlist_id))
    db.session.delete(packlist_item)
    db.session.commit()
    flash('Item removed from packlist.', 'success')
    return redirect(url_for('show_packlist', packlist_id=packlist_id))


# ------------------------------------------------------------------------------
# Run the App
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
