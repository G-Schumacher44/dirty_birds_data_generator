import pandas as pd
import pytest
from pathlib import Path
import subprocess

# Path to the generator script relative to the project root
GENERATOR_SCRIPT = Path(__file__).parent.parent / "penguin_synthetic_generator_v0.4.0.py"

@pytest.fixture(scope="module")
def generated_data(tmp_path_factory):
    """
    A pytest fixture that runs the data generator script once per test module.
    It creates data in a temporary directory and returns the paths to the
    clean and messy output files.
    """
    # Create a temporary directory for this test session
    tmp_dir = tmp_path_factory.mktemp("data")
    clean_file = tmp_dir / "test_clean_data.csv"
    messy_file = tmp_dir / "test_messy_data.csv"
    num_penguins = 100

    # Build the command to run the generator
    command = [
        "python", str(GENERATOR_SCRIPT),
        "--clean-output", str(clean_file),
        "--messy-output", str(messy_file),
        "--num-penguins", str(num_penguins),
        "--mess-level", "moderate",
        "--duplicate-rate", "0.5",
        "--species-missing-rate", "0.1",
        "--mislabel-rate", "0.0" # Ensure no mislabels for default tests
    ]

    # Run the generator script
    subprocess.run(command, check=True, capture_output=True, text=True)

    # Return the paths and the number of penguins for tests to use
    return {
        "clean_file": clean_file,
        "messy_file": messy_file,
        "num_penguins": num_penguins
    }

def test_files_are_created(generated_data):
    """Test that the generator successfully creates the output files."""
    assert generated_data["clean_file"].exists(), "Clean file was not created."
    assert generated_data["messy_file"].exists(), "Messy file was not created."

def test_clean_csv_has_correct_rows(generated_data):
    """Test the clean file has the expected number of rows."""
    df_clean = pd.read_csv(generated_data["clean_file"])
    assert not df_clean.empty, "Clean CSV is empty."
    assert len(df_clean) == generated_data["num_penguins"], f"Expected {generated_data['num_penguins']} clean penguins."

def test_messy_csv_has_more_rows_than_clean(generated_data):
    """Test that the messy file has more rows (due to resights) than the clean one."""
    df_clean = pd.read_csv(generated_data["clean_file"])
    df_messy = pd.read_csv(generated_data["messy_file"])
    assert len(df_messy) > len(df_clean), "Messy CSV should have more rows than clean CSV due to resights."

def test_required_columns_present(generated_data):
    """Test that all expected columns are present in the messy file."""
    df_messy = pd.read_csv(generated_data["messy_file"])
    expected_cols = [
        'tag_id', 'species', 'bill_length_mm', 'bill_depth_mm',
        'flipper_length_mm', 'body_mass_g', 'age_group', 'sex',
        'colony_id', 'island', 'capture_date', 'health_status',
        'study_name', 'clutch_completion', 'date_egg'
    ]
    for col in expected_cols:
        assert col in df_messy.columns, f"Missing expected column: {col}"

def test_species_missingness_injected(generated_data):
    """Test that the species column in the messy file contains missing values."""
    df_messy = pd.read_csv(generated_data["messy_file"])
    
    # Calculate the expected number of missing species values
    total_rows = len(df_messy)
    missing_rate_in_test = 0.1 # From the fixture command
    expected_missing_count = int(total_rows * missing_rate_in_test)

    actual_missing_count = df_messy['species'].isna().sum()

    # Allow for a small tolerance due to integer conversion and randomness
    assert abs(actual_missing_count - expected_missing_count) <= 1, \
        f"Expected ~{expected_missing_count} missing species, but found {actual_missing_count}."

def test_no_date_collision_for_same_tag(generated_data):
    """
    Ensures that for any given tag_id, all corresponding capture_date values are unique.
    This prevents the "mislabeled" duplicate scenario where a resight fails to get a new date.
    """
    df_messy = pd.read_csv(generated_data["messy_file"])

    # Filter for tagged penguins and drop rows with invalid dates for this specific check
    tagged_df = df_messy.dropna(subset=['tag_id', 'capture_date'])

    # Check for duplicates on the combination of tag_id and capture_date
    duplicates = tagged_df[tagged_df.duplicated(subset=['tag_id', 'capture_date'], keep=False)]

    assert duplicates.empty, f"Found {len(duplicates)} rows with the same tag_id and capture_date but different data."

def test_resight_duplicate_rate(generated_data):
    """Verifies that the number of resight records is consistent with the duplicate_rate."""
    df_clean = pd.read_csv(generated_data["clean_file"])
    df_messy = pd.read_csv(generated_data["messy_file"])

    resight_rows_added = len(df_messy) - len(df_clean)

    initial_tagged_count = df_clean['tag_id'].notna().sum()
    duplicate_rate_in_test = 0.5  # From the fixture command
    expected_resights = int(initial_tagged_count * duplicate_rate_in_test * 0.95)  # Account for 5% survival drop

    assert abs(resight_rows_added - expected_resights) / expected_resights < 0.15, \
        f"Expected ~{expected_resights} resights, but found {resight_rows_added}."

def test_mislabeled_duplicates_are_created(tmp_path):
    """
    Tests that the --mislabel-rate argument correctly creates duplicates
    with the same tag_id and capture_date.
    """
    messy_file = tmp_path / "mislabeled_data.csv"
    clean_file = tmp_path / "clean_for_mislabel_test.csv"
    mislabel_rate = 0.1
    num_penguins = 200 # Use a slightly larger number for a more stable test

    command = [
        "python", str(GENERATOR_SCRIPT),
        "--messy-output", str(messy_file),
        "--clean-output", str(clean_file),
        "--num-penguins", str(num_penguins),
        "--mislabel-rate", str(mislabel_rate)
    ]
    subprocess.run(command, check=True)

    df_messy = pd.read_csv(messy_file)
    df_clean = pd.read_csv(clean_file)

    # The number of mislabels is based on the number of valid (tagged, dated) records in the clean set
    initial_valid_records = df_clean.dropna(subset=['tag_id', 'capture_date'])
    expected_mislabels = int(len(initial_valid_records) * mislabel_rate)

    # Find the number of *added* mislabeled rows by checking for duplicates on tag and date
    actual_mislabels = df_messy.duplicated(subset=['tag_id', 'capture_date']).sum()

    assert abs(actual_mislabels - expected_mislabels) <= 2, \
        f"Expected ~{expected_mislabels} mislabeled duplicates, but found {actual_mislabels}."