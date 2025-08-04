<file name=0 path=/Users/garrettschumacher/Documents/git_repos/dirty_birds_data_generator/README.md><p align="center">
  <img src="dark_logo_banner.png" width="1000"/>
  <br>
  <em>Palmer Penguins Data Generator + QA Framework</em>
</p>

<p align="center">
  <img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="Status" src="https://img.shields.io/badge/status-alpha-lightgrey">
  <img alt="Version" src="https://img.shields.io/badge/version-v0.1.0-blueviolet">
</p>

---

# 🐧 Dirty Birds Data Generator

Dirty Birds is a synthetic data generator that simulates penguin tagging and monitoring programs for ecological analysis, QA testing, and model prototyping. The generator includes customizable randomness, optional messiness injection, and supports resight logic to mimic longitudinal tracking studies.

>📸 See it in action: [Dirty Birds Case Study](https://github.com/G-Schumacher44/dirty_birds_case_study)

___


## 🧩 TLDR;

Dirty Birds is a lightweight, standalone synthetic data generator built for ecological modeling, QA pipelines, and AI-assisted analytics workflows.

Dirty Birds simulates a realistic penguin tagging and monitoring study with:

- Species-specific modeling for **Adélie**, **Chinstrap**, and **Gentoo** penguins  
- **Biologically-informed randomness** based on peer-reviewed morphometrics  
- **Temporal logic** that mirrors real-world field conditions (tagging, resight windows, clutch dates)  
- **Clean mode** for generating analysis-ready, complete datasets  
- **Messy mode** with controlled missingness, resight overlaps, and field-style anomalies  
- **Stress-testing support** for pipelines and ML models under realistic data imperfections

🧠 Inspired by the [Palmer Penguins dataset](https://github.com/allisonhorst/palmerpenguins) — reimagined for modern workflows.

<details>
<summary> ⏯️ Quick Start</summary>
<br>

1. **Clone the repository**  
   
   ```bash
   git clone https://github.com/G-Schumacher44/dirty_birds_data_generator.git
   cd dirty_birds_data_generator
    ```

2.	**(Optional) Create a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```
3.	**Run the generator (default config, clean data)**

    ```bash
    python penguin_synthetic_generator_v0.3.0.py
    ```

</details>

---

## 📐 What’s Included

This repository contains the core components for generating and testing synthetic ecological datasets, specifically focused on penguin tracking studies:

- **`penguin_synthetic_generator_v0.3.0.py`**  
  The main generator script. Outputs clean and messy datasets simulating penguin tagging records, including longitudinal resight logic.

- **`synthetic_penguins_v3.5.csv`**  
  A sample output CSV including noise, reobservations, and controlled missingness — intended for QA, testing, or modeling.

- **`tests/`**  
  A minimal test suite to validate output structure, missing values, and column integrity.

---

## 🧭 Orientation & Getting Started

<details>
<summary><strong>🧠 Design Notes from the Architect</strong></summary>
<br>
Dirty Birds was created to fill the gap between clean, curated demo datasets and the messy, complex data typical in ecological fieldwork.

The original [Palmer Penguins dataset](https://github.com/allisonhorst/palmerpenguins) is widely used for teaching and modeling, but it lacks longitudinal structure, controlled messiness, and metadata variation. Dirty Birds addresses these limitations with:

- Multi-species support (Adélie, Chinstrap, Gentoo)  
- Realistic morphometric ranges based on field data  
- Simulated tagging, resight patterns, and seasonal clutch events  
- Field-like artifacts: missing values, duplicates, partial records  
- A **tiered realism system**: from clean, analysis-ready outputs to messy, field-style datasets for pipeline testing and skill building

The goal was not just to replicate a dataset — but to simulate real-world constraints. Dirty Birds helps teams validate pipelines, stress-test models, and teach robust data practices with credible synthetic data grounded in ecological research.

</details>

</details>

<details>
<summary><strong>🫆 Version Release Notes</strong></summary>

### ✅ v0.3.0 (Current)



---

### 🔮 v0.4.0 (Planned)

(more robust tagging systems, yaml configuration<move to an agnostic system that can generate any species style data>)

</details>

</details> 

<details>
<summary>⚙️ Project Structure</summary>



</details>

<details>
<summary><strong>📖 Sources and References</strong></summary>

**📚 Research-Backed Design**

The generator is grounded in real-world penguin research.

I based colony sizes on published ecological studies, modeled species-specific morphometrics using real measurements, and designed the temporal structure (e.g. tag dates, egg laying, resight windows) to mirror field realities.

Even the injected messiness — like partial sex assignments, missing weights, or resight overlaps — was crafted based on documented fieldwork constraints and data collection patterns.

Behind this generator is a layer of ecological research: peer-reviewed literature, dataset audits, and tagging program documentation all informed the logic. Our goal was to build not just plausible data — but credible synthetic data.

**Sources**

- [Palmer Penguins Extended Dataset (Kaggle)](https://www.kaggle.com/datasets/samybaladram/palmers-penguin-dataset-extended)  
  *(used as a baseline dataset for structure and values across key features)*
- [Original Palmer Penguins R package](https://github.com/allisonhorst/palmerpenguins)  
  *(provided foundational variable definitions and column semantics)*
- [USAP Continental Field Manual (2024)](https://www.usap.gov/usapgov/travelAndDeployment/documents/Continental-Field-Manual-2024.pdf)  
  *(used for tag/resight timing and field logistics modeling)*
- [Adélie Penguin Breeding Census – AADC Collection #154](https://data.aad.gov.au/aadc/biodiversity/display_collection.cfm?collection_id=154)  
  *(used for colony size distributions, clutch timing patterns, and site-specific breeding variability)*
- [Ropert‑Coudert et al. (2018) – *Two Massive Breeding Failures in an Adélie Colony*](https://doi.org/10.3389/fmars.2018.00264)  
  *(used to model temporal breeding variability and extreme event scenarios)*
- [Schmidt et al. (2021) – *Sub-Colony Habitat & Reproductive Success in Adélie Penguins*](https://doi.org/10.1038/s41598-021-94861-7)  
  *(used to parameterize habitat-scale effects on nest success rates)*
- [Palmer Station Morphometric Dataset (2007–2009, EDI)](https://data.key2stats.com/data-set/view/1299)  
  *(public-domain measurements of bill length, depth, flipper length, body mass, and sex across Adélie, Chinstrap, and Gentoo penguins — used to model species-specific distributions and dimorphism)*
- [Tyler et al. (2020) – *Morphometric & Genetic Evidence for Four Gentoo Penguin Clades*](https://doi.org/10.1002/ece3.6973)  
  *(used to parameterize Gentoo body size, bill morphology, and subspecies variation)*
- [Fattorini & Olmastroni (2021) – *Morphometric Sexing in Adélie Penguins*](https://doi.org/10.1007/s00300-021-02893-6)  
  *(used to model bill length, bill depth, body mass, and sex-based morphometric differences)*

</details>

---

## ▶️ Setup 

### 📦 Dev Setup


___

### ▶️ CLI Usage


___

## 🧪 Testing and Validation Guide

This project includes a comprehensive testing framework to ensure the integrity and quality of the synthetic data. Running these tests is highly recommended, especially after making changes to the configuration or generating new datasets.

<details>
<summary>🎯 Test Objectives</summary>


</details>  

<details>
<summary>🛠️ Running the Tests</summary>


</details>

___

## 🤝 On Generative AI Use

Generative AI tools (Gemini 2.5-PRO, ChatGPT 4o - 4.1) were used throughout this project as part of an integrated workflow — supporting code generation, documentation refinement, and idea testing. These tools accelerated development, but the logic, structure, and documentation reflect intentional, human-led design. This repository reflects a collaborative process: where automation supports clarity, and iteration deepens understanding.

---

## 📦 Licensing

This project is licensed under the [MIT License](LICENSE).</file>
