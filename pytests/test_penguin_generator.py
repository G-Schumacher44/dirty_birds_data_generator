import pandas as pd
import pytest
from pathlib import Path

# Constants
CLEAN_FILE = Path("synthetic_penguins_v3.5_clean.csv")
MESSY_FILE = Path("synthetic_penguins_v3.5.csv")

def test_clean_csv_exists_and_valid():
    assert CLEAN_FILE.exists(), "Clean CSV not found."
    df = pd.read_csv(CLEAN_FILE)
    assert not df.empty, "Clean CSV is empty."
    assert len(df) == 4500, "Expected 4500 clean penguins."

def test_messy_csv_exists_and_valid():
    assert MESSY_FILE.exists(), "Messy CSV not found."
    df = pd.read_csv(MESSY_FILE)
    assert len(df) > 4500, "Messy CSV should include resights and be larger than clean data."

def test_required_columns_present():
    df = pd.read_csv(MESSY_FILE)
    expected_cols = [
        'tag_id', 'species', 'bill_length_mm', 'bill_depth_mm',
        'flipper_length_mm', 'body_mass_g', 'age_group', 'sex',
        'colony_id', 'island', 'capture_date', 'health_status',
        'study_name', 'clutch_completion', 'date_egg'
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing expected column: {col}"

def test_species_missingness_injected():
    df = pd.read_csv(MESSY_FILE)
    missing = df['species'].isna().mean()
    assert 0.02 <= missing <= 0.04, f"species missing rate too low or high: {missing:.2%}"