# Automated Plant Disease Classification 🌿🤖

## Project Overview
This project focuses on **automating plant disease classification** using **Machine Learning and Deep Learning** techniques. The goal is to create an efficient diagnostic system that enables **early detection** of plant diseases, helping prevent crop damage and promoting sustainable agriculture.

## Methodology
### 1. Data Collection
- **Source**: Kaggle's **Plant Pathogen Dataset**.
- **Data Split**: Training and validation sets were created with shuffling for better generalization.

### 2. Model Development
#### **Traditional Machine Learning Models**
- Logistic Regression
- Random Forest
- Support Vector Machine (SVM)

#### **Deep Learning Models**
- **Custom CNN**: A simple **Convolutional Neural Network (CNN)** was designed and trained.
- **Pre-trained Transfer Learning Models**:
  - MobileNetV2
  - EfficientNetV2B0
  - InceptionV3
  - NASNetMobile
  - DenseNet121

## 📊 Results
| Model              | Training Accuracy | Validation Accuracy |
|--------------------|-------------------|---------------------| 
| **Custom CNN**     | **92.76%**        | **92.43%**          |
| MobileNetV2        | 54.28%            | 52.26%              |
| EfficientNetV2B0   | 26.29%            | 25.45%              |
| InceptionV3        | 79.13%            | 62.57%              |
| NASNetMobile       | 46.34%            | 46.51%              |
| DenseNet121        | 46.43%            | 45.99%              |

**Best Model**: The **Custom CNN** outperformed all other models, achieving the highest accuracy.

## Evaluation & Insights
### **Possible Shortcomings**
- **Pre-trained models did not perform well** due to a domain mismatch with the Kaggle dataset.
- **Limited fine-tuning** of pre-trained models.
- **Overfitting or underfitting** due to the number of epochs.

### **Future Research**
- Explore alternative **deep learning architectures**.
- Fine-tune pre-trained models more effectively.
- Experiment with **unsupervised and semi-supervised learning**.
