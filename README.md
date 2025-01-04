

 # PII Detection and Anonymization

This project focuses on detecting and anonymizing Personally Identifiable Information (PII) using advanced Natural Language Processing (NLP) techniques.
![image](https://github.com/user-attachments/assets/390993ce-a80b-494d-a4df-7b23b3dd766b)


**Approach for PII Detection**

**Named Entity Recognition (NER)**  
We leverage cutting-edge NLP models to identify PII such as names, addresses, and phone numbers.

- **Base Model:** `en_core_web_trf`  
  - Utilizes a BERT-based transformer architecture for NER.
  - While powerful, it lacks inherent PII detection capabilities, leading us to adopt **Presidio** for enhanced performance.

 **Why Presidio?**
- **Machine Learning Capabilities:** Reliable and robust for PII detection.  
- **Customizable and Scalable:** Easily tailored to meet diverse and evolving needs.

---

 **Integration of Presidio with a Custom NLP Model**
We finetuned en_core_web_trf with a taset containing some custom entities so that we can flag those .

**Enhanced Detection**  
We replaced Presidio’s default `en_core_web_lg` model with the transformer-based `en_core_web_trf` for superior recognition of entities such as:
- **Person**
- **Location**
- **Organization**

 **Domain-Specific Fine-Tuning**  
The `en_core_web_trf` model was fine-tuned with financial data entities to achieve precise, industry-specific PII detection.

---

 **Anonymization**

Custom anonymization functions were developed to ensure effective and thorough anonymization of detected PII. These functions handle various data types such as:
- Names
- Email Addresses
- Phone Numbers
- Locations
- Credit Card Numbers
- IP Addresses

---

**Future Work**

1. **Alignment:**  
   - Synchronizing fine-tuned model tags with Presidio for seamless integration.  

2. **Data Quality:**  
   - Continuous enhancement of the detection pipeline to ensure the highest level of accuracy.

3. **Expansion:**  
   - Broadening the scope of PII recognizers to cover additional entities and data types.

---

**Key Features**

- **Scalable Architecture:** Supports domain-specific customization.
- **Transformer-Based NLP:** Ensures high accuracy and contextual understanding.
- **Custom Anonymization:** Protects sensitive information with tailored masking techniques.

---
 **How to Run the Project**
1. Clone the repository:
   git clone https://github.com/debleo10/pii-detection-anonymization.git
   cd pii-detection-anonymization
2. Install dependencies:
   pip install -r requirements.txt
3. Start the Flask application:
   python app.py


4. Open your browser and navigate to `http://localhost:5000`.

---

**Contributing**
Contributions are welcome! Feel free to open an issue or submit a pull request.

