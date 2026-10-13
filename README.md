# Low-Cost Blood Diagnostic Kit Using Colorimetric Biomarker Analysis

## Research Team

**Hemosapiens**

### Student Researchers

- Minjoo Lee — Team Lead
- Chaewon Seo
- Ahyun Lee
- Chaewon Lee
- Seyoung Jeon

### Faculty Advisor

- Jeongsoo Kim

[View Research Poster](research-poster.pdf)

---

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Motivation](#2-motivation)
- [3. Research Objective](#3-research-objective)
- [4. Project Evolution](#4-project-evolution)
- [5. System Concept](#5-system-concept)
- [6. Target Biomarkers](#6-target-biomarkers)
- [7. Experimental Methods](#7-experimental-methods)
  - [7.1 Total Protein — Bradford Assay](#71-total-protein--bradford-assay)
  - [7.2 Alkaline Phosphatase — Bessey–Lowry Method](#72-alkaline-phosphatase--besseylowry-method)
  - [7.3 Ammonia — Salicylate Method](#73-ammonia--salicylate-method)
- [8. Image-Based Quantification Pipeline](#8-image-based-quantification-pipeline)
- [9. Software Prototype](#9-software-prototype)
- [10. Results](#10-results)
- [11. Limitations](#11-limitations)
- [12. Future Work](#12-future-work)
- [13. Expected Impact](#13-expected-impact)
- [14. References](#14-references)

---

## 1. Project Overview

This project develops a **low-cost blood diagnostic system** that estimates biomarker concentrations from **color changes in blood samples**.

The central idea is to replace expensive spectrophotometric measurements, where possible, with a more accessible workflow based on:

1. a colorimetric biochemical reaction,
2. smartphone image capture,
3. RGB-based image analysis,
4. regression-based absorbance estimation, and
5. biomarker concentration prediction.

The long-term goal is to create a portable diagnostic platform that can be used in environments where conventional laboratory infrastructure is limited.

---

## 2. Motivation

Many people in developing regions and socially vulnerable communities have limited access to hospitals, diagnostic laboratories, and expensive analytical equipment.

Conventional blood testing often depends on instruments such as spectrophotometers, which provide reliable measurements but are costly and difficult to deploy in resource-constrained settings.

To improve accessibility, this study investigates whether **visible color changes produced by biochemical assays can be quantified using a smartphone camera** and converted into clinically meaningful biomarker estimates.

---

## 3. Research Objective

The project aims to establish a pipeline that connects:

**Biomarker concentration → Colorimetric reaction → Optical/color measurement → Image-based quantification → Concentration prediction**

The specific objectives are:

- build standard reference data using spectrophotometric measurements,
- identify visible color changes associated with different biomarker concentrations,
- map smartphone-derived RGB values to absorbance,
- convert predicted absorbance into biomarker concentration,
- implement the analysis process as an easy-to-use software prototype,
- and eventually integrate the system into a portable diagnostic kit.

---

## 4. Project Evolution

The project initially focused on developing an **image-based smart kit for bilirubin quantification**.

During the research process, the scope was broadened toward a more general **colorimetric blood biomarker analysis platform**. The final experimental stage focused on three biomarkers:

- **Total Protein**
- **Alkaline Phosphatase (ALP)**
- **Ammonia**

This shift allowed the team to evaluate whether the same smartphone-based analysis concept could be applied across multiple biochemical assays rather than to a single target.

---

## 5. System Concept

The proposed diagnostic workflow is:

```text
Blood sample
   ↓
Blood-cell removal / sample preparation
   ↓
Colorimetric reagent reaction
   ↓
Color change according to biomarker concentration
   ↓
Smartphone image capture
   ↓
Automatic image-region selection
   ↓
RGB extraction
   ↓
RGB → Absorbance prediction
   ↓
Absorbance → Biomarker concentration
   ↓
Diagnostic interpretation
```

The final system is intended to minimize dependence on laboratory equipment while maintaining quantitative analysis through standardized imaging and regression models.

---

## 6. Target Biomarkers

| Biomarker | Assay | Measurement Wavelength | Intended Diagnostic Relevance |
|---|---|---:|---|
| Total Protein | Bradford Assay | 595 nm | Abnormally low or high total protein levels |
| Alkaline Phosphatase (ALP) | Bessey–Lowry Method | 405 nm | Liver- and bone-related abnormalities |
| Ammonia | Salicylate Method | 660 nm | Hyperammonemia and related metabolic abnormalities |

The project does **not** claim clinical diagnostic validation at its current stage. These biomarkers were used to evaluate the feasibility of the proposed colorimetric measurement pipeline.

---

## 7. Experimental Methods

### 7.1 Total Protein — Bradford Assay

The total protein experiment used the **Bradford assay**, where Coomassie Brilliant Blue reacts with proteins and produces a concentration-dependent color change.

#### Procedure

1. Prepare BSA standard samples at multiple concentrations.
2. Mix each sample with Bradford reagent.
3. Incubate under light-protected room-temperature conditions.
4. Measure absorbance at **595 nm** using a spectrophotometer.
5. Construct a standard concentration–absorbance curve.
6. Capture sample images under a controlled light source.
7. Extract RGB values from the sample image.
8. Train a regression model to map RGB values to absorbance.
9. Convert predicted absorbance to total protein concentration.

For blood samples, the experimental process included dilution and centrifugation to obtain a serum-like supernatant before reaction with the Bradford reagent.

---

### 7.2 Alkaline Phosphatase — Bessey–Lowry Method

The ALP experiment used a **p-nitrophenyl phosphate (pNPP)**-based reaction.

The general reaction is:

```text
pNPP + H₂O → pNP + PO₄³⁻
```

The generated p-nitrophenol (pNP) produces a measurable color signal.

#### Procedure

1. Prepare pNPP substrate in DEA buffer at approximately pH 9.8.
2. Mix ALP samples with the substrate solution.
3. Incubate under controlled temperature and light conditions.
4. Stop the reaction using NaOH.
5. Measure absorbance near **405 nm**.
6. Compare absorbance and color changes across ALP concentrations and reaction times.

Due to a spectrophotometer lamp failure around the target wavelength, reliable quantitative absorbance data could not be obtained during this stage.

---

### 7.3 Ammonia — Salicylate Method

The ammonia experiment was based on the **salicylate method**, which produces a colored indophenol-type product.

A simplified reaction sequence is:

```text
NH₃ + OCl⁻ → NH₂Cl + OH⁻

NH₂Cl + Salicylate + Catalyst
→ Colored indophenol product
```

#### Procedure

1. Prepare ammonium samples at different concentrations.
2. Adjust the reaction condition to approximately pH 10.3.
3. Add the required reagents sequentially.
4. React the samples for approximately 20 minutes in the dark.
5. Measure absorbance near **660 nm**.

In the reported experiment, reagent quality and pH control were insufficient, and a meaningful color response was not obtained.

---

## 8. Image-Based Quantification Pipeline

The image-analysis pipeline was designed to transform a smartphone image into a quantitative biomarker estimate.

### Step 1 — Image Capture

Samples are photographed under a fixed or controlled light source.

### Step 2 — Automatic Region Selection

Instead of manually selecting the sample region, the program scans the image using a **sliding-window approach**.

For each candidate region:

- RGB variation is calculated,
- color standard deviation is evaluated,
- and the most spatially uniform region is selected.

### Step 3 — RGB Extraction

The average RGB values of the selected region are calculated.

### Step 4 — RGB-to-Absorbance Mapping

The extracted RGB values are paired with spectrophotometer measurements obtained from the same samples.

A **second-order polynomial regression model** is then used to estimate absorbance from image-derived color values.

For the total-protein experiment, the reported model achieved approximately:

```text
R² ≈ 0.998
```

### Step 5 — Absorbance-to-Concentration Conversion

The predicted absorbance is converted to biomarker concentration using an experimentally derived calibration equation.

For the reported total-protein experiment:

```text
Concentration (µg/mL)
= 73.985 × Absorbance − 4.172
```

This creates an end-to-end pipeline from smartphone image to quantitative concentration estimate.

---

## 9. Software Prototype

A web-based analysis prototype was implemented using **Streamlit**.

### Main Functions

- image upload,
- automatic RGB extraction,
- image-region selection,
- absorbance prediction,
- biomarker concentration calculation,
- real-time result display,
- tabular output,
- CSV export.

The current program should be considered a **proof-of-concept analysis tool**, rather than a clinically validated diagnostic application.

---

## 10. Results

### Total Protein

The Bradford assay produced the strongest result among the three target biomarkers.

Key findings:

- absorbance at 595 nm increased with BSA concentration,
- a usable standard curve was constructed,
- visible color differences were observed across concentrations,
- smartphone images contained sufficient color information for quantitative analysis,
- and the RGB-to-absorbance regression model achieved **R² ≈ 0.998** in the reported dataset.

These results support the feasibility of using image-based color analysis as an intermediate step toward smartphone-based biomarker quantification.

### ALP

The ALP experiment showed visible reaction trends, but reliable quantitative evaluation was limited by failure of the spectrophotometer lamp near the target wavelength.

As a result:

- meaningful 405 nm absorbance values could not be secured,
- and reaction-time differences could not be evaluated reliably.

### Ammonia

The ammonia experiment did not produce a sufficiently clear color reaction.

The reported causes were:

- use of an unsuitable or insufficiently pure reagent,
- inadequate pH control,
- and incomplete optimization of reaction conditions.

The experiment therefore requires redesign and repetition.

---

## 11. Limitations

The current study has several important limitations.

### Experimental Limitations

- insufficient control of illumination during image capture,
- limited environmental standardization,
- equipment malfunction during the ALP experiment,
- inadequate pH control during the ammonia experiment,
- reagent-quality issues,
- limited sample size,
- and insufficient clinical sample validation.

### Modeling Limitations

The current regression model was trained on a limited experimental dataset.

A high R² value on the current dataset does not by itself demonstrate:

- robustness across devices,
- robustness across lighting conditions,
- clinical accuracy,
- generalization to unseen biological samples,
- or diagnostic sensitivity and specificity.

---

## 12. Future Work

### 12.1 Standardized Imaging Hardware

Develop a physical imaging kit including:

- fixed LED illumination,
- standardized background,
- fixed camera distance,
- fixed sample position,
- and controlled imaging geometry.

### 12.2 Improved Color Representation

Extend the current RGB-based analysis to other color spaces, including:

- HSV,
- CIELAB / LAB,
- and calibrated color-difference features.

### 12.3 Color-Correction Models

Develop machine-learning-based color correction to compensate for:

- different smartphone cameras,
- white-balance variation,
- illumination differences,
- exposure differences,
- and environmental noise.

### 12.4 Biomarker-Specific Test Strips

Develop dedicated reagent strips optimized for each biomarker, with controlled:

- reagent amount,
- reaction time,
- temperature,
- pH,
- and sample volume.

### 12.5 Mobile Application

Convert the Streamlit prototype into a mobile application capable of:

- guided image capture,
- automatic quality checking,
- real-time concentration prediction,
- and user-friendly result visualization.

### 12.6 Clinical Validation

Future validation should compare smartphone-derived estimates with conventional laboratory measurements using real biological samples.

Evaluation metrics should include:

- prediction error,
- repeatability,
- sensitivity,
- specificity,
- calibration stability,
- and inter-device reproducibility.

---

## 13. Expected Impact

If successfully developed and validated, the proposed platform could reduce dependence on expensive analytical instruments for selected colorimetric blood tests.

Potential application environments include:

- low-resource clinics,
- field screening,
- public-health programs,
- educational laboratories,
- and portable point-of-care testing systems.

The project demonstrates a broader concept: **biochemical color reactions can be coupled with consumer imaging devices and lightweight regression software to create more accessible quantitative diagnostic tools.**

---

## 14. References

1. Bessey, O. A., Lowry, O. H., & Brock, M. J. (1946). *A method for the rapid determination of alkaline phosphatase with five cubic millimeters of serum.*

2. Patton, C. J., & Crouch, S. R. (1977). *Spectrophotometric and kinetics investigation of the salicylate method / related colorimetric ammonia determination work.*

> Note: The reference information above follows the citations listed in the project poster. Full bibliographic details should be verified before use in a formal paper.
