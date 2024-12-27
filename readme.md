Camping Gear Tracker
A Flask-based web application to track your camping gear, organize items into packlists, and generate printable packing lists. This project demonstrates:

Item Management: Create, read, update, and delete camping gear items.
CSV Import/Export: Easily import and export your item list.
Search & Sort: Filter items by name/category/season and sort them by various columns.
Packlists: Create named packlists, add items to them from the main item list, and display/print them in a 2-column layout.
Modern UI: Uses Bootstrap for a responsive layout.
Features
Item Management

Track name, description, weight, season, keywords, category, quantity, etc.
Upload an image and link to an external URL for each item.
CSV Support

Export your current item list to a CSV file.
Import items from a CSV file (updating existing items by matching an item number, or adding new items).
Packlists

Create multiple named packlists.
Add items from the main page into a selected packlist.
Remove/clear items from a packlist.
Print packlists for easy packing references.
Search & Sort

Search items by name, category, or season (case-insensitive).
Sort by column (name, weight, season, category, quantity).
Getting Started
Below are step-by-step instructions to get this application running on your local machine for development and testing.

1. Install Python
Verify whether Python is installed:
bash
Copy code
python --version
If not installed, download and install Python 3.x from python.org.
2. Clone the Repository
Open your terminal (or command prompt).

Navigate to the directory where you want to store the project.

Run:

bash
Copy code
git clone https://github.com/your-github-username/camping-gear-tracker.git
Replace your-github-username and the repository name with the actual path for your GitHub repo.

Navigate into the new project folder:

bash
Copy code
cd camping-gear-tracker
3. Create and Activate a Virtual Environment (Optional but Recommended)
Create a virtual environment named venv:
bash
Copy code
python -m venv venv
Activate the virtual environment:
Windows:
bash
Copy code
venv\Scripts\activate
macOS/Linux:
bash
Copy code
source venv/bin/activate
4. Install Dependencies
Make sure you’re in the root of the project directory (where requirements.txt is located).
Install all requirements:
bash
Copy code
pip install -r requirements.txt
5. Run the Application
In the project directory, run the Flask app:
bash
Copy code
python app.py
Open your web browser and go to:
arduino
Copy code
http://127.0.0.1:5000
You should see the Camping Gear Tracker homepage.
Usage
Add Items: From the homepage (/), click Add Item to add new gear with a name, description, weight, season, etc.
Search & Sort: Use the search bar above the item list to filter by name/category/season. Click column headers to sort ascending/descending.
Import CSV: Click Import CSV in the navigation bar, choose a CSV file, and upload to bulk import items.
Export CSV: Click Export CSV to download the entire item list.
Manage Packlists: Go to View All Packlists to create or delete named packlists.
On the homepage, select items with the checkboxes, pick a packlist from the dropdown, and click Add to Packlist.
View that packlist in a 2-column layout, remove items, or clear all items from it.
Print directly from your browser for a handy physical checklist.
Contributing
Contributions are welcome! Feel free to open issues, submit pull requests, or suggest enhancements.

Fork this repository.
Create a new branch for your feature or bug fix.
Submit a pull request once your changes are ready.
License
This project is open-source. You may use, modify, and distribute it under the terms of your chosen open-source license. Adjust this section to reflect your actual license if you have one in place.

Happy Camping! If you run into any issues or have questions, please open an issue on GitHub or contact the maintainers of this repository.