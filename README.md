Standardizes company names using the Serper.dev search API. Cleans duplicates, filters out locations, and handles truncation errors from search titles.

company-name-cleanser/
├── data/
│   └── companylist.xlsx           # Raw data (add to .gitignore if sensitive)
├── output/
│   └── cleaned_companies.xlsx     # Standardized names output
├── main.py                        # Python script with logic
├── requirements.txt               # Required packages
├── README.md                      # Project overview
├── .gitignore                     # Ignore output and temp files
└── LICENSE                        # MIT License
