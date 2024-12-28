# Description
This app is intended to reduce the chaos around having way too many items for camping acquired over the years and needing a way to keep track of everything and come up with a common sense way to make a pack list for trips. I found myself taking way too much stuff into the woods every time I would go, and I am hoping this project will help me cut down to just the meaningful items needed for my trip. I am hoping over time to make a wholistic trip planner that will allow you to scout out locations, save a location wishlist, and use that geolocation information to help generate a packlist for the trip based on available information such as weather, regional plants and animals, regulations for the land (state, federal, etc), and information like nearby campgrounds and trails to plan activities while in the area (and have a backup plan in case the spot didnt work out).

# Getting Started

Below are step-by-step instructions to get this application running on your local machine for development and testing.

## 1. Install Python

1. Verify whether Python is installed:
   ```bash
   python --version
   ```

2. If not installed, download and install Python 3.x from python.org.

## 2. Clone the Repository

1. Open your terminal (or command prompt).
2. Navigate to the directory where you want to store the project.
3. Run:
   ```bash
   git clone https://github.com/afeilzer/camper_chaos.git
   ```

4. Navigate into the new project folder:
   ```bash
   cd camper-chaos
   ```

## 3. Create and Activate a Virtual Environment (Optional but Recommended)

1. Create a virtual environment named `venv`:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   * **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   * **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

## 4. Install Dependencies

1. Make sure you're in the root of the project directory (where `requirements.txt` is located).
2. Install all requirements:
   ```bash
   pip install -r requirements.txt
   ```

## 5. Run the Application

1. In the project directory, run the Flask app:
   ```bash
   python app.py
   ```

2. Open your web browser and go to:
   ```
   http://127.0.0.1:5000
   ```

3. You should see the Camping Gear Tracker homepage.

## Usage

### Managing Items

- **Add Items**: From the homepage (`/`), click **Add Item** to add new gear with a name, description, weight, season, etc.
- **Search & Sort**: Use the search bar above the item list to filter by name/category/season. Click column headers to sort ascending/descending.
- **Import CSV**: Click **Import CSV** in the navigation bar, choose a CSV file, and upload to bulk import items.
- **Export CSV**: Click **Export CSV** to download the entire item list.

### Working with Packlists

- **Manage Packlists**: Go to **View All Packlists** to create or delete named packlists.
- On the homepage, select items with the checkboxes, pick a packlist from the dropdown, and click **Add to Packlist**.
- View that packlist in a 2-column layout, remove items, or clear all items from it.
- Print directly from your browser for a handy physical checklist.

## Contributing

Contributions are welcome! Feel free to open issues, submit pull requests, or suggest enhancements.

1. **Fork** this repository.
2. Create a **new branch** for your feature or bug fix.
3. Submit a **pull request** once your changes are ready.

## License

This project is open-source. You may use, modify, and distribute it under the terms of your chosen open-source license. Adjust this section to reflect your actual license if you have one in place.

---

Happy Camping! If you run into any issues or have questions, please open an issue on GitHub or contact the maintainers of this repository.