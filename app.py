import spacy
from faker import Faker
import pycountry
import random
import re
import pickle
import ipaddress
from pathlib import Path, PosixPath, WindowsPath
from flask import Flask, render_template, request, jsonify

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import SpacyNlpEngine

app = Flask(__name__)


# nlp = spacy.load("en_core_web_trf")

faker = Faker()


class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "pathlib" and name == "PosixPath":
            return WindowsPath
        return super().find_class(module, name)

def generate_fake_ip(original_ip):
    def random_ipv4_octet():
        return str(random.randint(0, 255))
    def random_ipv6_group():
        return ''.join(random.choice('0123456789abcdef') for _ in range(4))
    try:
        ip = ipaddress.ip_address(original_ip)
    except ValueError:
        return original_ip

    if ip.version == 4:
        parts = original_ip.split('.')
        fake_ip = '.'.join(random_ipv4_octet() if part.isdigit() else part for part in parts)
    elif ip.version == 6:
        parts = original_ip.split(':')
        fake_ip = ':'.join(random_ipv6_group() if part else '' for part in parts)

    return fake_ip
def generate_fake_location(original_location):
    fake = Faker()
    location_parts = original_location.strip().split(',')
    location_parts = [part.strip().lower() for part in location_parts]
    if len(location_parts) == 1:
        part = location_parts[0]
        countries = {country.name.lower() for country in pycountry.countries}
        if part in countries:
            fake_location = fake.country()
        else:
            fake_location = fake.city()
    elif len(location_parts) == 2:
        fake_location = f"{fake.city()}, {fake.state_abbr()}" # Generate a fake city and state abbreviation
    elif len(location_parts) == 3:
        fake_location = f"{fake.city()}, {fake.state_abbr()}, {fake.country()}" # Generate a fake city, state, and country
    else:
        fake_location = fake.city()

    return fake_location
def generate_fake_phone_number(original_phone_number):
    mask = ''.join(['X' if char.isdigit() else char for char in original_phone_number])
    fake_number = ''.join([random.choice('0123456789') if char == 'X' else char for char in mask])
    return fake_number
def generate_fake_email():
    fake = Faker()
    fake_email = fake.email()
    email_providers = ['gmail', 'yahoo', 'outlook', 'hotmail', 'aol']
    return fake_email.split('@')[0] + '@' + random.choice(email_providers) + '.' + fake_email.split('@')[1].split('.')[1]


def generate_fake_name(original_name):
    fake = Faker()
    if ' ' in original_name.strip(): # Check if the original name contains a space (indicating a full name)
        fake_name = fake.name()
    else:
        fake_name = fake.first_name()

    return fake_name


def generate_fake_credit_card(original_cc):

    # Generate a new credit card number with the same length and structure
    def generate_digits(length):
        return ''.join(str(random.randint(0, 9)) for _ in range(length))
    fake_cc = ''.join(generate_digits(1) if char.isdigit() else char for char in original_cc)

    return fake_cc


def generate_fake_ssn(original_ssn):
    def generate_digit():
        return str(random.randint(0, 9))
    fake_ssn = ''.join(generate_digit() if char.isdigit() else char for char in original_ssn)

    return fake_ssn
class LoadedSpacyNlpEngine(SpacyNlpEngine):
    def __init__(self, loaded_spacy_model):
        super().__init__()
        self.nlp = {"en": loaded_spacy_model}

# Load a model a-priori
# nlp = spacy.load("en_core_web_trf")
# with open("C:\\Users\\ddasgupta\\PycharmProjects\\pythonProject9\\nlp_ner_model.pkl", "rb") as f:
# nlp_ner = pickle.load(f)
with open('nlp_ner_model.pkl', 'rb') as f:
    model = CustomUnpickler(f).load()
    model=pickle.load(f)

# Pass the loaded model to the new LoadedSpacyNlpEngine
loaded_nlp_engine = LoadedSpacyNlpEngine(loaded_spacy_model = model)

# Pass the engine to the analyzer
analyzer = AnalyzerEngine(nlp_engine = loaded_nlp_engine)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        t = analyzer.analyze(text, language="en")
        entities = []
        for entity in t:
            if entity.score > 0.5:
                entities.append((text[entity.start:entity.end], entity.entity_type))
        # doc = nlp(text)
        # entities = [(ent.text, ent.label_) for ent in doc.ents]
        # print(analyzer.analyze(text="My name is Debarshi.", language="en"))
        # entities=[('debarshi','name'),('kolkata','city')]
        # print(entities)
    else:
        text = ""
        entities = []

    return render_template("index.html", text=text, entities=entities)


@app.route("/anonymize", methods=["POST"])
def anonymize():
    data = request.get_json()
    entity_text = data["text"]
    entity_label = data["label"]

    # Generate anonymized data based on the label
    if entity_label=="PHONE_NUMBER":
        fake_number = generate_fake_phone_number(str(entity_text))
        anonymized_data=fake_number
    elif entity_label=="EMAIL_ADDRESS":
        fake_email=generate_fake_email()
        anonymized_data=fake_email


    elif entity_label == "PERSON":
        anonymized_data = generate_fake_name(entity_text)
    elif entity_label in ["GPE", "LOCATION"]:
        anonymized_data = generate_fake_location(entity_text)
    elif entity_label=="CREDIT_CARD":
        anonymized_data=generate_fake_credit_card(str(entity_text))
    elif entity_label=="US_SSN":
        anonymized_data=generate_fake_ssn(str(entity_text))
    elif entity_label=="US_BANK_NUMBER":
        anonymized_data=generate_fake_ssn(str(entity_text))

    elif entity_label == "US_PASSPORT":
        anonymized_data = generate_fake_ssn(str(entity_text))
    elif entity_label=="IP_ADDRESS":
        anonymized_data=generate_fake_ip(entity_text)
    elif entity_label == "ORG":
        anonymized_data = faker.company()
    elif entity_label == "DATE":
        anonymized_data = faker.date()
    elif entity_label == "MONEY":
        anonymized_data = faker.pricetag()
    else:
        anonymized_data = entity_text # Default anonymized value for unsupported labels

    return jsonify({"anonymized_data": anonymized_data})


if __name__ == "__main__":
    app.run(debug=True)
