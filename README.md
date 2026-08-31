# 1. Create fresh virtual environment
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Upgrade core tools and install dependencies
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt