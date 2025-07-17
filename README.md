

# Centrecom Laptop Web Scraper

This Python script scrapes laptop product data from Centrecom's website and saves the results in both JSON and CSV formats.<br>
Literally generated this readme with chatgpt. Still it could be useful for a specific purpose.

---

## 📌 How It Works

The script:

1. Prompts for a base URL of a laptop search or category page (e.g., `https://www.centrecom.com.au/laptops?view=category`).
2. Iterates through paginated results using the `&pagenumber=` query parameter.
3. Extracts product details including:
   - Name
   - Product URL
   - Image URL
   - Features
   - Sale Price
   - Original Price (if available)
   - Stock icon details
4. Saves data to:
   - `centrecom_laptops.json`
   - `centrecom_laptops.csv`

---

## 🔧 Requirements

Install the following packages before running the script:

```bash
pip install requests beautifulsoup4 lxml
````

---

## 🚀 Usage

1. Open your terminal or command prompt.
2. Run the script:

```bash
python scriptname.py
```

3. Paste the base Centrecom URL when prompted, for example:

```
https://www.centrecom.com.au/laptops?view=category
```

4. The script will begin scraping all pages, but repeating the last page so control c on the script after it gets and saves the last page.

---

## 🗂 Output

* `centrecom_laptops.json`: Contains structured product data in JSON format.
* `centrecom_laptops.csv`: Spreadsheet-friendly version of the same data.

---

## 🐞 Known Bugs / Limitations

* **New pages dont stop:** When doing the scan it will not stop scanning even if there is no more new laptops, this is because on the centrecom website if you go `&pagenumber=` +1 and there is no more pages it will just load the last page

---

## ⏱ Notes

* The script includes a 2-second delay between page requests for politeness.
* Product URLs are normalized to be fully qualified.
* Works best when run with a stable internet connection and correct base URL.

---

## ⚠️ Disclaimer

This script is for **educational and personal use only**. Please ensure that your scraping activity complies with Centrecom’s [Terms of Service](https://www.centrecom.com.au/terms).

---

```

You can now save this as `README.md` in the same directory as your script. Let me know if you want help turning this into a GitHub project or adding a license file.
```
