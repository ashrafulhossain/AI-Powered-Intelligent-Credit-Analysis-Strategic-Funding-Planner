# import os
# import fitz  # PyMuPDF
# import openai
# import pandas as pd
# from fpdf import FPDF
# from dotenv import load_dotenv
# from docx import Document
# import logging
# import re
# import uuid
# import easyocr
# from PIL import Image
# import io
# import numpy as np
# import json

# # === Setup Logging ===
# logging.basicConfig(
#     filename='funding_nc_analyzer.log',
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# # === Load environment variables ===
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # === File Paths ===
# BANK_LIST_PATH = "data/0% APR Business Credit Card Master List.xlsx"
# JSON_DATA_PATH = "data/card_data.json"
# ENRICH_PDF_FILES = [
#     "data/General Credit Card Knowledge.pdf",
#     "data/DATA POINTS - BUSINESS CREDIT CARD DATA POINTS.pdf",
#     "data/HOW To Leverage Business Credit to.pdf"
# ]
# ENRICH_DOCX_FILES = [
#     "data/Credit Stacking Guide Lines and Better Practices.docx"
# ]
# ENRICH_CSV_FILES = [
#     "data/Tarjetas de Negocio sin Garantia Personal.csv"
# ]

# # Initialize EasyOCR reader
# reader = easyocr.Reader(['en'], gpu=False)  # English language, GPU disabled for simplicity

# # === Function to load JSON data ===
# def load_json_data():
#     try:
#         with open(JSON_DATA_PATH, 'r') as file:
#             data = json.load(file)
#             logging.info(f"Loaded JSON data from {JSON_DATA_PATH}")
#             print(f"✅ Loaded JSON data with {len(data)} cards")
#             return data
#     except Exception as e:
#         logging.error(f"Failed to load JSON data: {str(e)}")
#         print(f"❌ Failed to load JSON data: {str(e)}")
#         return None

# # === Function to extract text from PDF ===
# def extract_text_from_pdf(pdf_path):
#     try:
#         text = ""
#         with fitz.open(pdf_path) as doc:
#             for page in doc:
#                 page_text = page.get_text()
#                 if page_text.strip():
#                     text += page_text + "\n"
#                 else:
#                     logging.info(f"No text found in page {page.number + 1} for {pdf_path}, attempting OCR")
#                     pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
#                     img_bytes = pix.tobytes("png")
#                     img = Image.open(io.BytesIO(img_bytes))
#                     img_np = np.array(img)
#                     ocr_result = reader.readtext(img_np, detail=0)
#                     ocr_text = "\n".join(ocr_result)
#                     if ocr_text.strip():
#                         text += ocr_text + "\n"
#                     else:
#                         logging.warning(f"No text extracted via OCR from page {page.number + 1} of {pdf_path}")
        
#         if text.strip():
#             logging.info(f"Successfully extracted text from PDF: {pdf_path}")
#             logging.debug(f"Extracted text snippet: {text[:500]}...")
#             return text
#         else:
#             logging.error(f"No text could be extracted from {pdf_path}, even with OCR")
#             return None
#     except Exception as e:
#         logging.error(f"Error extracting PDF text from {pdf_path}: {str(e)}")
#         return None

# # === Function to extract Credit Score and Utilization ===
# def extract_credit_info(text):
#     score_pattern = r"Credit Score\s*[:\-]?\s*(\d{3,4})"
#     score_matches = re.findall(score_pattern, text)
#     score = score_matches[0] if score_matches else None
    
#     utilization_pattern = r"Utilization\s*[:\-]?\s*(\d{1,3}%?)"
#     utilization_matches = re.findall(utilization_pattern, text)
#     utilization = utilization_matches[0] if utilization_matches else None
    
#     return score, utilization

# # === Function to extract text from DOCX ===
# def extract_text_from_docx(docx_path):
#     try:
#         doc = Document(docx_path)
#         text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
#         logging.info(f"Successfully extracted text from DOCX: {docx_path}")
#         return text
#     except Exception as e:
#         logging.error(f"Error extracting DOCX text from {docx_path}: {str(e)}")
#         return None

# # === Function to extract text from CSV ===
# def extract_text_from_csv(csv_path):
#     try:
#         df = pd.read_csv(csv_path)
#         text = df.to_string(index=False)
#         logging.info(f"Successfully extracted text from CSV: {csv_path}")
#         return text
#     except Exception as e:
#         logging.error(f"Error extracting CSV text from {csv_path}: {str(e)}")
#         return None

# # === Support Functions ===
# def is_spanish(text):
#     keywords = ["crédito", "buró", "negativo", "consulta", "puntuación", "tarjeta", "financiamiento"]
#     return sum(1 for word in keywords if word in text.lower()) >= 3

# def load_bank_data():
#     try:
#         df = pd.read_excel(BANK_LIST_PATH)
#         logging.info(f"Loaded bank list with {len(df)} entries")
#         print(f"✅ Loaded bank list with {len(df)} entries")
#         return df
#     except Exception as e:
#         logging.error(f"Failed to load bank list: {str(e)}")
#         print(f"❌ Failed to load bank list: {str(e)}")
#         return None

# def get_state_funding_cards(user_state, json_data):
#     try:
#         state_cards = []
#         for card_name, card_info in json_data.items():
#             if user_state in card_info['state']:
#                 state_cards.append({
#                     'card_name': card_name,
#                     'bank': card_info['bank'],
#                     'apr': card_info['apr'],
#                     'mode': card_info['mode'],
#                     'bureau': card_info['bureau'],
#                     'is_travel': card_info['is_travel'],
#                     'game_plan': card_info['game_plan']
#                 })
#         if not state_cards:
#             logging.error(f"No cards found for state {user_state}")
#             print(f"❌ No cards found for state {user_state}")
#             return None
#         logging.info(f"Found {len(state_cards)} cards for state {user_state}: {[card['card_name'] for card in state_cards]}")
#         print(f"✅ Found {len(state_cards)} cards for state {user_state}: {[card['card_name'] for card in state_cards]}")
#         return state_cards
#     except Exception as e:
#         logging.error(f"Error loading state funding cards: {str(e)}")
#         print(f"❌ Error loading state funding cards: {str(e)}")
#         return None

# def get_enrichment():
#     enrichment = ""
#     for file in ENRICH_PDF_FILES + ENRICH_DOCX_FILES + ENRICH_CSV_FILES:
#         if os.path.exists(file):
#             try:
#                 if file.endswith(".pdf"):
#                     text = extract_text_from_pdf(file)
#                 elif file.endswith(".docx"):
#                     text = extract_text_from_docx(file)
#                 elif file.endswith(".csv"):
#                     text = extract_text_from_csv(file)
#                 else:
#                     text = ""
#                 if text:
#                     enrichment += f"\n[From {os.path.basename(file)}]\n{text[:1000]}...\n"
#             except Exception as e:
#                 enrichment += f"\n[Error reading {file}]: {str(e)}\n"
#                 logging.error(f"Error reading enrichment file {file}: {str(e)}")
#         else:
#             enrichment += f"\n[Skipped missing file: {file}]\n"
#             logging.warning(f"Skipped missing enrichment file: {file}")
#     return enrichment

# # === Output Validation ===
# def validate_gpt_output(analysis, state_cards, user_state, json_data, mode="free"):
#     analysis_lower = analysis.lower()
#     not_qualified = "does not qualify for funding" in analysis_lower
#     eligible_message = "you are eligible for funding" in analysis_lower

#     required_sections = [
#         r"📌.*Breakdown by Bureau",
#         r"📌.*Revolving Credit Structure",
#         r"📌.*Authorized User.*Strategy",
#         r"📌.*Funding Readiness by Bureau",
#         r"📌.*Verdict",
#         r"📌.*Action Plan",
#         r"📌.*Recommended Funding Sequence"
#     ]
#     if mode == "paid":
#         required_sections.append(r"\*\*You Are Fully Ready to Execute\*\*")

#     missing_sections = [sec for sec in required_sections if not re.search(sec, analysis, re.IGNORECASE)]
#     if missing_sections:
#         missing_names = [re.search(r"\.\*(.*?)(?=\||\Z)", sec).group(1).strip() for sec in missing_sections]
#         logging.error(f"Missing sections in GPT output: {missing_names}")
#         error_note = f"\n\n⚠️ ERROR: Missing sections in analysis: {', '.join(missing_names)}. Please check the credit report data or API response."
#         analysis += error_note

#     # Remove any mention of 'Inferred' or variations
#     analysis = re.sub(r"\(Inferred\)", "", analysis, flags=re.IGNORECASE)
#     analysis = re.sub(r"inferred as \d+\b", lambda m: m.group(0).replace("inferred as ", ""), analysis, flags=re.IGNORECASE)
#     analysis = re.sub(r"\bInferred\b", "", analysis, flags=re.IGNORECASE)

#     # Handle 'Data not available' replacements
#     if "Data not available" in analysis:
#         logging.warning("GPT used 'Data not available' in output. Replacing with estimated values.")
#         replacements = {
#             r"Credit Score.*Data not available": "Credit Score: 700 (based on industry standards and clean payment history)",
#             r"Utilization.*Data not available": "Utilization: 15% (based on typical credit profiles with high-limit cards)",
#             r"Avg\. Credit Age.*Data not available": "Avg. Credit Age: 2.5 years (based on standard account age)",
#             r"Hard Inquiries.*Data not available": "Hard Inquiries: 2 (based on typical inquiry patterns)"
#         }
#         for pattern, replacement in replacements.items():
#             analysis = re.sub(pattern, replacement, analysis, flags=re.IGNORECASE)
#         analysis += "\n\n📋 Note: Some values were estimated based on industry standards to provide a complete analysis."

#     if mode == "free":
#         logging.info("Validating and cleaning GPT output for free mode.")
#         if eligible_message:
#             logging.info("User is eligible in free mode. Ensuring Section 7 reflects eligibility.")
#             analysis = re.sub(
#                 r"📌 \*\*7\. Recommended Funding Sequence \((.*?)\)\*\*.*?(?=\*\*Disclaimer\*\*|\Z)",
#                 f"📌 **7. Recommended Funding Sequence ({user_state})**\n\n"
#                 f"🎉 ¡Eres elegible para financiamiento! Para ver tus bancos recomendados (R1, R2, R3), por favor actualiza a nuestro Plan Premium.\n\n",
#                 analysis,
#                 flags=re.DOTALL
#             )
#         else:
#             logging.info("User is not qualified in free mode. Ensuring Section 7 reflects ineligibility.")
#             analysis = re.sub(
#                 r"📌 \*\*7\. Recommended Funding Sequence \((.*?)\)\*\*.*?(?=\*\*Disclaimer\*\*|\Z)",
#                 f"📌 **7. Recommended Funding Sequence ({user_state})**\n\n"
#                 f"Tu perfil de crédito no califica actualmente para financiamiento. Por favor, sigue el plan de acción en la Sección 6 para mejorar tu elegibilidad.\n\n",
#                 analysis,
#                 flags=re.DOTALL
#             )
#         # Remove Strategic Insights and You Are Fully Ready to Execute sections in free mode
#         analysis = re.sub(
#             r"\*\*Strategic Insights for Execution\*\*.*?(\*\*Disclaimer\*\*|\Z)",
#             "**Disclaimer**",
#             analysis,
#             flags=re.DOTALL
#         )
#         analysis = re.sub(
#             r"\*\*You Are Fully Ready to Execute\*\*.*?(\*\*Disclaimer\*\*|\Z)",
#             "**Disclaimer**",
#             analysis,
#             flags=re.DOTALL
#         )

#     if mode == "paid":
#         if not_qualified and eligible_message:
#             logging.warning("Inconsistent GPT output: Verdict says not qualified, but Funding Sequence says eligible.")
#             print("❌ Fixing inconsistent GPT output in paid mode.")
#             analysis = re.sub(
#                 r"🎉 You are eligible for funding!.*?(?=\*\*Strategic Insights|\Z)",
#                 "Your credit profile does not currently qualify for funding. Please follow the action plan in Section 6 to improve your eligibility.",
#                 analysis,
#                 flags=re.DOTALL
#             )
#             logging.info("Fixed inconsistent verdict in paid mode.")

#         if "please upgrade to our Premium Plan" in analysis_lower:
#             logging.error("Incorrect verdict message for paid mode")
#             analysis = re.sub(
#                 r"🎉 You're eligible for funding! To view your matched bank recommendations.*?Plan\.",
#                 "🎉 You're eligible for funding! See your matched bank recommendations below.",
#                 analysis
#             )
#             logging.info("Fixed incorrect verdict message for paid mode.")

#         # Validate rounds for paid mode
#         rounds = re.findall(r"\*\*ROUND [1-3]\*\*(.*?)(?=\*\*ROUND|\*\*Strategic Insights|\Z)", analysis, re.DOTALL)
#         valid_modes = ["Online", "In-branch", "Phone", "Online (requires account)", "Online (Omaha Zip)", "Phone/In-branch", "In-branch/Phone"]
#         for i, round_content in enumerate(rounds, 1):
#             rows = re.findall(r"\|\s*([^\|]+?)\s*\|\s*(Experian|TransUnion|Equifax)\s*\|\s*([0-9]+ MESES|Default [0-9]+ MESES|0%|\s*NO\s*)\s*\|\s*([^\|]*?)\s*\|\s*([^\|]*?)\s*\|", round_content)
#             bureaus = []
#             banks = []
#             invalid_cards = []
#             apr_mismatches = []
#             mode_mismatches = []
#             bureau_mismatches = []
#             default_usage = []
#             invalid_reasons = []

#             for row in rows:
#                 card_name, bureau, apr, mode, reason = row
#                 card_name_clean = card_name.strip()
#                 bureau = bureau.strip()
#                 apr = apr.strip() if apr else "12 MESES"
#                 mode = mode.strip() if mode else "Online"
#                 reason = reason.strip()
#                 bureaus.append(bureau)
#                 banks.append(card_name_clean)

#                 card_info = json_data.get(card_name_clean)
#                 if not card_info:
#                     invalid_cards.append(card_name_clean)
#                     logging.error(f"Invalid card {card_name_clean} in Round {i}. Not found in JSON data.")
#                     error_note = f"\n\n⚠️ ERROR: Card {card_name_clean} in Round {i} is not in JSON data. Replacing with a valid card."
#                     if error_note not in analysis:
#                         analysis += error_note

#                     replacement_card = None
#                     for card in state_cards:
#                         if card['card_name'] not in banks and card['bureau'] == bureau:
#                             replacement_card = card
#                             break

#                     if replacement_card:
#                         replacement_apr = replacement_card['apr']
#                         replacement_mode = replacement_card['mode']
#                         replacement_reason = "Strong credit history"
#                     else:
#                         logging.error(f"No valid card found in JSON data for bureau {bureau} in Round {i}.")
#                         error_note = f"\n\n⚠️ ERROR: No valid card found in JSON data for Round {i}. Please check JSON data."
#                         if error_note not in analysis:
#                             analysis += error_note
#                         continue

#                     analysis = re.sub(
#                         r"\|\s*" + re.escape(card_name_clean) + r"\s*\|\s*" + bureau + r"\s*\|\s*[^\|]*?\s*\|\s*[^\|]*?\s*\|\s*[^\|]*?\s*\|",
#                         f"| {replacement_card['card_name']} | {bureau} | {replacement_apr} | {replacement_mode} | {replacement_reason} |",
#                         analysis
#                     )

#                 else:
#                     expected_apr = card_info['apr']
#                     expected_mode = card_info['mode']
#                     expected_bureau = card_info['bureau']
#                     if apr != expected_apr:
#                         apr_mismatches.append((card_name_clean, expected_apr, apr))
#                         logging.error(f"APR mismatch for {card_name_clean} in Round {i}: Expected {expected_apr}, Got {apr}")
#                         error_note = f"\n\n⚠️ ERROR: APR for {card_name_clean} in Round {i} is incorrect. Expected {expected_apr}, Got {apr}."
#                         if error_note not in analysis:
#                             analysis += error_note
#                         analysis = re.sub(
#                             r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|).*?(\|.*?\|).*?(\|)",
#                             f"|\1{bureau}|{expected_apr}|{mode}|{reason}|",
#                             analysis
#                         )
#                     if mode != expected_mode:
#                         mode_mismatches.append((card_name_clean, expected_mode, mode))
#                         logging.error(f"Mode mismatch for {card_name_clean} in Round {i}: Expected {expected_mode}, Got {mode}")
#                         error_note = f"\n\n⚠️ ERROR: Mode for {card_name_clean} in Round {i} is incorrect. Expected {expected_mode}, Got {mode}."
#                         if error_note not in analysis:
#                             analysis += error_note
#                         analysis = re.sub(
#                             r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|.*?\|).*?(\|.*?\|)",
#                             f"|\1{bureau}|{apr}|{expected_mode}|{reason}|",
#                             analysis
#                         )
#                     if bureau != expected_bureau:
#                         bureau_mismatches.append((card_name_clean, expected_bureau, bureau))
#                         logging.error(f"Bureau mismatch for {card_name_clean} in Round {i}: Expected {expected_bureau}, Got {bureau}")
#                         error_note = f"\n\n⚠️ ERROR: Bureau for {card_name_clean} in Round {i} is incorrect. Expected {expected_bureau}, Got {bureau}."
#                         if error_note not in analysis:
#                             analysis += error_note
#                         analysis = re.sub(
#                             r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|).*?(\|.*?\|.*?\|.*?\|)",
#                             f"|\1{expected_bureau}|{apr}|{mode}|{reason}|",
#                             analysis
#                         )

#                     chase_count = sum(1 for row in rows if json_data.get(row[0].strip(), {}).get('bank') == 'Chase' and not json_data.get(row[0].strip(), {}).get('is_travel', False))
#                     if chase_count > 1:
#                         logging.error(f"More than one non-travel Chase card detected in Round {i}.")
#                         error_note = f"\n\n⚠️ ERROR: More than one non-travel Chase card in Round {i}. Replacing with a travel card or another bank's card."
#                         if error_note not in analysis:
#                             analysis += error_note
#                         replacement_card = None
#                         for card in state_cards:
#                             if (card['bank'] == 'Chase' and card['is_travel'] and card['card_name'] not in banks) or (card['bank'] != 'Chase' and card['card_name'] not in banks):
#                                 replacement_card = card
#                                 break
#                         if replacement_card:
#                             replacement_apr = replacement_card['apr']
#                             replacement_mode = replacement_card['mode']
#                             replacement_bureau = replacement_card['bureau']
#                             replacement_reason = "Strong credit history"
#                             analysis = re.sub(
#                                 r"\|\s*" + re.escape(card_name_clean) + r"\s*\|\s*" + bureau + r"\s*\|\s*[^\|]*?\s*\|\s*[^\|]*?\s*\|\s*[^\|]*?\s*\|",
#                                 f"| {replacement_card['card_name']} | {replacement_bureau} | {replacement_apr} | {replacement_mode} | {replacement_reason} |",
#                                 analysis
#                             )

#                 card_bank = card_info['bank'] if card_info else None
#                 if card_bank:
#                     matched = any(card_bank.lower() in card['bank'].lower() or card['bank'].lower() in card_bank.lower() for card in state_cards)
#                     if not matched:
#                         logging.error(f"Card {card_name_clean} in Round {i} is not in state_cards for {user_state}: {[card['card_name'] for card in state_cards]}")
#                         error_note = f"\n\n⚠️ ERROR: Card {card_name_clean} in Round {i} is not in the approved card list for {user_state}. Replacing with a valid card."
#                         if error_note not in analysis:
#                             analysis += error_note
#                         replacement_card = None
#                         for card in state_cards:
#                             if card['card_name'] not in banks:
#                                 replacement_card = card
#                                 break
#                         if replacement_card:
#                             replacement_apr = replacement_card['apr']
#                             replacement_mode = replacement_card['mode']
#                             replacement_bureau = replacement_card['bureau']
#                             replacement_reason = "Strong credit history"
#                             analysis = re.sub(
#                                 r"\|\s*" + re.escape(card_name_clean) + r"\s*\|\s*" + bureau + r"\s*\|\s*[^\|]*?\s*\|\s*[^\|]*?\s*\|\s*[^\|]*?\s*\|",
#                                 f"| {replacement_card['card_name']} | {replacement_bureau} | {replacement_apr} | {replacement_mode} | {replacement_reason} |",
#                                 analysis
#                             )

#                 if apr == "0%":
#                     logging.error(f"Invalid APR '0%' for {card_name_clean} in Round {i}. Replacing with default '12 MESES'.")
#                     error_note = f"\n\n⚠️ ERROR: Invalid APR '0%' for {card_name_clean} in Round {i}. Replaced with '12 MESES'."
#                     if error_note not in analysis:
#                         analysis += error_note
#                     analysis = re.sub(
#                         r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|).*?(\|.*?\|).*?(\|)",
#                         f"|\1{bureau}|12 MESES|{mode}|{reason}|",
#                         analysis
#                     )

#                 if mode not in valid_modes:
#                     logging.error(f"Invalid mode '{mode}' for {card_name_clean} in Round {i}. Replacing with 'Online'.")
#                     error_note = f"\n\n⚠️ ERROR: Invalid mode '{mode}' for {card_name_clean} in Round {i}. Replaced with 'Online'."
#                     if error_note not in analysis:
#                         analysis += error_note
#                     analysis = re.sub(
#                         r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|.*?\|).*?(\|.*?\|)",
#                         f"|\1{bureau}|{apr}|Online|{reason}|",
#                         analysis
#                     )

#                 valid_reasons = [
#                     r"diversify cards",
#                     r"requires account",
#                     r"flexible approval",
#                     r"single pull",
#                     r"high credit score",
#                     r"low utilization",
#                     r"minimal inquiries",
#                     r"strong credit history",
#                     r"supports double dip",
#                     r"strong primary card structure, excellent credit management"
#                 ]
#                 reason_valid = any(re.search(pattern, reason.lower()) for pattern in valid_reasons)
#                 if not reason_valid or "missing credit data" in reason.lower():
#                     invalid_reasons.append((card_name_clean, reason))
#                     logging.warning(f"Invalid or undesired reason for {card_name_clean} in Round {i}: {reason}")
#                     error_note = f"\n\n⚠️ WARNING: Invalid or undesired reason for {card_name_clean} in Round {i}: '{reason}'. Replacing with a dynamic reason."
#                     if error_note not in analysis:
#                         analysis += error_note
#                     replacement_reason = "Diversify cards"
#                     if "requires account" in mode.lower():
#                         replacement_reason = "Requires account"
#                     elif "in-branch" in mode.lower():
#                         replacement_reason = "Flexible approval"
#                     elif "online" in mode.lower():
#                         replacement_reason = "Single pull"
#                     elif "high credit score" in analysis_lower:
#                         replacement_reason = "High credit score"
#                     elif "low utilization" in analysis_lower:
#                         replacement_reason = "Low utilization"
#                     elif "minimal inquiries" in analysis_lower:
#                         replacement_reason = "Minimal inquiries"
#                     else:
#                         replacement_reason = "Strong credit history"
#                     analysis = re.sub(
#                         r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|.*?\|.*?\|).*?(\|)",
#                         f"|\1{bureau}|{apr}|{mode}|{replacement_reason}|",
#                         analysis
#                     )

#             if len(set(bureaus)) != 3 or bureaus != ['Experian', 'TransUnion', 'Equifax']:
#                 logging.warning(f"Invalid bureau variety in Round {i}: {bureaus}")
#                 error_note = f"\n\n⚠️ WARNING: Round {i} does not contain exactly one of each bureau (Experian, TransUnion, Equifax) in order."
#                 if error_note not in analysis:
#                     analysis += error_note

#             if len(set(banks)) != 3 or len(banks) != 3:
#                 logging.warning(f"Invalid bank variety in Round {i}: {banks}")
#                 error_note = f"\n\n⚠️ WARNING: Round {i} does not contain exactly three different banks."
#                 if error_note not in analysis:
#                     analysis += error_note

#             logging.info(f"Round {i} Cards: {banks}, Bureaus: {bureaus}")

#             analysis += f"\n\n📋 Round {i} Validation Summary:\n"
#             analysis += f"- Total Cards Suggested: {len(banks)}\n"
#             analysis += f"- Invalid Cards: {invalid_cards}\n"
#             analysis += f"- APR Mismatches: {apr_mismatches}\n"
#             analysis += f"- Mode Mismatches: {mode_mismatches}\n"
#             analysis += f"- Bureau Mismatches: {bureau_mismatches}\n"
#             analysis += f"- Cards Using Default Values: {default_usage}\n"
#             analysis += f"- Invalid Reasons: {invalid_reasons}\n"

#     logging.info("GPT output validation completed.")
#     return analysis

# # === Core GPT Analysis ===
# def analyze_credit_report(text, bank_df=None, mode="free", user_state=None):
#     json_data = load_json_data()
#     if not json_data:
#         logging.error("Failed to load JSON data. Cannot proceed with analysis.")
#         print("❌ Failed to load JSON data. Cannot proceed with analysis.")
#         return None

#     language = "Spanish" if is_spanish(text) else "English"
#     state_cards = get_state_funding_cards(user_state, json_data) if user_state else []
#     enrichment_context = get_enrichment()

#     print(f"State-specific card list for {user_state}: {[card['card_name'] for card in state_cards]}")

#     bank_data_str = ""
#     if bank_df is not None and mode == "paid":
#         bank_data_str += "\n\nApproved Bank List (for reference only, do NOT use for suggestions):\n"
#         for _, row in bank_df.head(10).iterrows():
#             row_str = " | ".join(str(x) for x in row.values if pd.notna(x))
#             bank_data_str += f"- {row_str}\n"
#     else:
#         bank_data_str = "\n\nNo bank list provided for free mode.\n"

#     double_dip_info = {}
#     if bank_df is not None:
#         for _, row in bank_df.iterrows():
#             bank_name = str(row['Bank Name']).strip()
#             double_dip = str(row['Double Dip']).strip().lower() == 'yes'
#             double_dip_info[bank_name] = double_dip

#     tarjetas_str = "\n\nCard Data (for APR, Mode, Bureau, and Game Plan):\n"
#     for card_name, card_info in json_data.items():
#         tarjetas_str += f"- {card_name}: APR: {card_info['apr']}, Mode: {card_info['mode']}, Bank: {card_info['bank']}, Bureau: {card_info['bureau']}, Game Plan: {card_info['game_plan']}\n"

#     include_sequence_note = ""
#     if mode == "paid":
#         include_sequence_note = (
#             f"\n\n**CRITICAL INSTRUCTION**: The user has selected the Premium Plan for state {user_state}.\n"
#             f"You MUST select ALL funding cards (R1, R2, R3) EXCLUSIVELY from the user's state-specific approved card list provided below as `state_cards`:\n"
#             f"{', '.join([card['card_name'] for card in state_cards]) if state_cards else 'No cards available'}\n"
#             f"**CRITICAL**: Under NO circumstances suggest cards outside `state_cards`. Doing so will invalidate the output.\n"
#             f"**CRITICAL**: In the 'Card Name' column, ALWAYS use the EXACT card name from `Card Data` (e.g., 'BOFA Unlimited Cash'). You MUST NOT use bank names alone (e.g., 'Bank of America') or append 'Card' to a bank name (e.g., 'Capital One Card'). If no matching card is found in `Card Data` for a bank in `state_cards`, exclude that bank and select another card from `state_cards`.\n"
#             f"**CRITICAL**: GPT MUST NOT generate or suggest any card names outside of `Card Data`. Any attempt to create new card names will invalidate the output.\n"
#             f"Each round (R1, R2, R3) MUST include EXACTLY 3 different banks, each associated with a different bureau in this order: Experian, TransUnion, Equifax.\n"
#             f"Each table row MUST contain exactly 5 columns: Card Name, Bureau, 0% APR, Mode, and Reason. Missing fields will invalidate the output.\n"
#             f"For 0% APR duration, Mode, and Bureau, use the provided `Card Data` below to match the exact card name and bank:\n{tarjetas_str}\n"
#             f"Only one 0% Chase card is allowed per sequence, unless the second is a co-branded travel/hotel card (verify `is_travel` field in `Card Data`).\n"
#             f"Bank of America and other banks can only repeat a 0% card if '0% APR Business Credit Card Master List' confirms double dipping: {double_dip_info}.\n"
#             f"If at least 2 bureaus meet all 6 factors and one does not, offer a funding sequence using only the qualifying bureaus.\n"
#             f"If no bureau qualifies, offer a no-personal-guarantee funding option from the CSV 'Tarjetas de Negocio sin Garantia Personal'.\n"
#             f"If the average credit age is less than 2.5 years for any bureau, do NOT include that bureau in the funding sequence. Instead, note in the Action Plan (Section 6) that the user must improve their credit age by maintaining open accounts for longer.\n"
#             f"**Reason Column**: For the Reason column, provide dynamic reasons based on the user's credit profile (e.g., high credit score, low utilization, minimal inquiries, strong credit history) or card-specific features (e.g., requires account, flexible approval, single pull, supports double dip). Examples include 'Diversify cards', 'Requires account', 'Flexible approval', 'Single pull', but do NOT hardcode these. Reasons must be relevant to the credit profile or card characteristics.\n"
#             f"**Game Plan**: For each card in the funding sequence, include the `game_plan` from `Card Data` in the Strategic Insights section to guide the user on application steps.\n"
#             f"Failure to follow these instructions will be considered INVALID.\n"
#         )
#     else:
#         include_sequence_note = (
#             f"\n\n**CRITICAL INSTRUCTION**: In free mode, you MUST NOT generate any card recommendations, **Strategic Insights for Execution**, or **You Are Fully Ready to Execute** sections.\n"
#             f"If the user qualifies for funding (based on the Funding Eligibility Logic), output EXACTLY this for Section 7 (Recommended Funding Sequence):\n"
#             f"📌 **7. Recommended Funding Sequence ({user_state})**\n\n"
#             f"🎉 ¡Eres elegible para financiamiento! Para ver tus bancos recomendados (R1, R2, R3), por favor actualiza a nuestro Plan Premium.\n\n"
#             f"If the user does NOT qualify, output EXACTLY this for Section 7:\n"
#             f"📌 **7. Recommended Funding Sequence ({user_state})**\n\n"
#             f"Tu perfil de crédito no califica actualmente para financiamiento. Por favor, sigue el plan de acción en la Sección 6 para mejorar tu elegibilidad.\n\n"
#             f"Ensure Section 5 (Verdict) and Section 7 (Funding Sequence) are consistent. Any deviation from these instructions will invalidate the output.\n"
#         )

#     prompt_template = {
#         "English": f"""
# 🧠 AI Credit Report Summary — Formal & Friendly

# You are a financial credit analysis assistant for Negocio Capital.

# **CRITICAL INSTRUCTION**: You MUST generate ALL sections (1 through 7) as specified below, in the exact order. You MUST NOT use or display the word 'Inferred' or any variation (e.g., 'inferred', 'Inferred', 'infer') in the output, even if values are estimated. If data is missing, estimate reasonable values based on industry standards or patterns in the enrichment files, but present them as definitive in the output without mentioning estimation. Skipping any section is INVALID.

# ---

# **Handling Missing Data**:
# If any data (e.g., Credit Score, Utilization, Credit Age, Inquiries) is missing or cannot be extracted from the provided credit report, estimate reasonable values based on available data, industry standards, or patterns in the enrichment files (e.g., Card Data, bank lists). Examples:
# - Credit Score: Use 700 if payment history is clean or no negative remarks are found; otherwise, use 650.
# - Utilization: Use 15% if high-limit cards (≥$5,000) are present; otherwise, use 25%.
# - Credit Age: Use 2.5 years unless evidence suggests newer accounts (e.g., recent inquiries).
# - Inquiries: Use 2 inquiries in the last 6 months unless specified otherwise.
# Ensure estimated values are conservative and realistic. In the output, present estimated values as definitive without mentioning estimation or using terms like 'Data not available'.

# ---

# **Funding Eligibility Logic**:
# 1. The user qualifies for funding ONLY if ALL of the following are true in at least one bureau:
#    - Credit Score ≥ 720
#    - No Late Payments
#    - Utilization < 10%
#    - ≤ 3 Inquiries in the last 6 months
#    - Credit Age ≥ 2.5 years
#    - Strong Primary Card Structure
# 2. If the user qualifies and is in paid mode, say: "🎉 You're eligible for funding! See your matched bank recommendations below." and list 3 cards (R1, R2, R3) EXCLUSIVELY from the state-specific card list for {user_state}.
# 3. If the user does NOT qualify, say: "Your credit profile does not currently qualify for funding. Please follow the action plan in Section 6 to improve your eligibility."
# 4. Ensure the Verdict (Section 5) and Recommended Funding Sequence (Section 7) are consistent.

# ---

# 📌 **1. Breakdown by Bureau**

# Generate a table of revolving credit details based on the actual report data or estimated values.

# | Category            | Equifax | Experian | TransUnion |
# |---------------------|---------|----------|------------|
# | Credit Score        |         |          |            |
# | Clean History       |         |          |            |
# | Utilization         |         |          |            |
# | Hard Inquiries (6 mo) |      |          |            |
# | Avg. Credit Age     |         |          |            |
# | Cards >= $2K        |         |          |            |
# | Cards >= $5K        |         |          |            |
# | Score / 144         |         |          |            |

# After the table, include a short analysis **in bullet point format** explaining each category individually. The explanation should be understandable to non-financial users. Use this format:

# - **Credit Score**: Report the credit score for each bureau. Mention if it meets the 720 threshold. End with a label like **Excellent**, **Good**, **Fair**, or **Poor**.
# - **Clean History**: Summarize if there are any missed or late payments. If none, state "Yes". End with a label like **Excellent** or **Needs Improvement**.
# - **Utilization**: Report the total utilization rate and whether it’s below 10%. Explain how it impacts funding eligibility. End with a label like **Excellent**, **Good**, or **High Risk**.
# - **Hard Inquiries (6 mo)**: Indicate how many inquiries occurred in the past 6 months. Mention if this is acceptable (≤ 3). End with a label like **Good**, **Fair**, or **Risky**.
# - **Avg. Credit Age**: Explain the average age of credit accounts. Mention if it meets the 2.5-year threshold. End with a label such as **Excellent** or **Fair**.
# - **Cards >= $2K**: Note the number of cards with limits of $2,000 or more. Mention how it supports creditworthiness. End with a label like **Good** or **Needs Improvement**.
# - **Cards >= $5K**: Note the number of cards with limits of $5,000 or more. Mention how it enhances funding readiness. End with a label like **Excellent** or **Fair**.
# - **Score / 144**: Report the total score out of 144 based on the analysis. End with a label like **Excellent** or **Needs Improvement**.

# Each bullet should be brief, clear, and conclude with a bold quality label. Do NOT mention estimation or use the word 'Inferred'.

# ---

# ### 📌 2. Revolving Credit Structure

# Always extract or estimate the revolving credit details and present them in a structured table.

# | **Field**                | **Detail**                                  |
# |--------------------------|---------------------------------------------|
# | Open Cards               | [Number of open cards, specify AU/Primary] |
# | Total Limit              | [$Total credit limit]                       |
# | Primary Cards            | [Count or “None”]                          |
# | High-Limit Card Present? | [YES/NO (Mention limit threshold, e.g. $5k+)]|

# Explain each field briefly below the table, without mentioning estimation.

# ---

# 📌 **3. Authorized User (AU) Strategy**

# - How many AU cards are there?
# - What are their limits and ages?
# - Do they help with funding?
# - Recommendation: what AU cards to add or remove.

# ---

# 📌 **4. Funding Readiness by Bureau**

# Ensure all available or estimated revolving credit data is displayed in a table.

# | Criteria                      | Equifax | Experian | TransUnion |
# | ----------------------------- | ------- | -------- | ---------- |
# | Score ≥ 720                   | Yes/No  | Yes/No   | Yes/No    |
# | No Late Payments              | Yes/No  | Yes/No   | Yes/No    |
# | Utilization < 10%             | Yes/No  | Yes/No   | Yes/No    |
# | ≤ 3 Inquiries (last 6 months) | Yes/No  | Yes/No   | Yes/No    |
# | Credit Age ≥ 2.5 Years        | Yes/No  | Yes/No   | Yes/No    |
# | Strong Primary Card Structure | Yes/No  | Yes/No   | Yes/No    |

# Explain the table below without mentioning estimation.

# ---

# 📌 5. Verdict

# Clearly state if the user qualifies for funding based on the Funding Eligibility Logic above. For paid mode, use: "🎉 You're eligible for funding! See your matched bank recommendations below." If not qualified, explain why in 2–3 short bullet points.

# ---

# 📌 6. Action Plan

# List 3–5 steps the user should take to improve their credit profile, such as:
# - Pay down credit card balances to reduce utilization.
# - Add new Authorized User (AU) cards with high limits to strengthen credit.
# - Open personal primary cards to build a stronger credit structure.
# - Dispute or wait out old late payments to improve credit history.
# If the average credit age is less than 2.5 years for any bureau, include a step to maintain open accounts for longer to improve credit age.

# ---

# 📌 **7. Recommended Funding Sequence ({user_state})**

# * If the user is in **paid mode**, provide the following structured output regardless of whether they qualify for funding. Use ONLY the approved card list provided in `state_cards` from the JSON data for the user's selected state ({user_state}). Follow these strict rules:

#   **If the user qualifies for funding**:
#   - Provide a funding sequence with three rounds (R1, R2, R3), each containing EXACTLY 3 different banks.
#   - Each card in a round MUST be associated with a different bureau in this order: Experian, TransUnion, Equifax.
#   - Cards MUST NOT be suggested from outside the `state_cards` list, even if the user has existing relationships with other banks.
#   - **CRITICAL**: Under NO circumstances suggest cards outside `state_cards`. If unsure, select a card from the list and note an appropriate reason in the Reason column.
#   - **CRITICAL**: In the 'Card Name' column, ALWAYS use the EXACT card name from `Card Data` (e.g., 'BOFA Unlimited Cash'). You MUST NOT use bank names alone (e.g., 'Bank of America') or append 'Card' to a bank name (e.g., 'Capital One Card'). If no matching card is found in `Card Data` for a bank in `state_cards`, exclude that bank and select another card from `state_cards`.
#   - **CRITICAL**: GPT MUST NOT generate or suggest any card names outside of `Card Data`. Any attempt to create new card names will invalidate the output.
#   - Each table row MUST contain exactly 5 columns: Card Name, Bureau, 0% APR, Mode, and Reason. Missing fields will invalidate the output.
#   - Only one 0% Chase card is allowed per sequence, unless the second is a co-branded travel/hotel card (verify `is_travel` field in `Card Data`).
#   - Bank of America and other banks can only repeat a 0% card if '0% APR Business Credit Card Master List' confirms double dipping: {double_dip_info}.
#   - If at least 2 bureaus meet all 6 factors and one does not, offer a funding sequence using only the qualifying bureaus.
#   - If no bureau qualifies, offer a no-personal-guarantee funding option from the CSV 'Tarjetas de Negocio sin Garantia Personal'.
#   - If the average credit age is less than 2.5 years for any bureau, do NOT include that bureau in the funding sequence. Instead, note in the Action Plan (Section 6) that the user must improve their credit age by maintaining open accounts for longer.
#   - For 0% APR duration, Mode, and Bureau, use the provided `Card Data` to match the exact card name and bank:\n{tarjetas_str}\n
#   - **Reason Column**: Provide dynamic reasons based on the user's credit profile (e.g., high credit score, low utilization, minimal inquiries, strong credit history) or card-specific features (e.g., requires account, flexible approval, single pull, supports double dip). Examples include 'Diversify cards', 'Requires account', 'Flexible approval', 'Single pull', but do NOT hardcode these. Reasons must be relevant to the credit profile or card characteristics.
#   - **Game Plan**: For each card in the funding sequence, include the `game_plan` from `Card Data` in the Strategic Insights section to guide the user on application steps.

#   **ROUND 1**
#   | Card Name          | Bureau   | 0% APR      | Mode         | Reason                  |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Card Name from Card Data] | Experian | [Time from Card Data] | [Mode from Card Data] | [Dynamic reason based on credit profile or card characteristics] |
#   | [Card Name from Card Data] | TransUnion | [Time from Card Data] | [Mode from Card Data] | [Dynamic reason based on credit profile or card characteristics] |
#   | [Card Name from Card Data] | Equifax | [Time from Card Data] | [Mode from Card Data] | [Dynamic reason based on credit profile or card characteristics] |

#   **ROUND 2**
#   | Card Name          | Bureau   | 0% APR      | Mode         | Reason                  |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Card Name from Card Data] | Experian | [Time from Card Data] | [Mode from Card Data] | [Dynamic reason based on credit profile or card characteristics] |
#   | [Card Name from Card Data] | TransUnion | [Time from Card Data] | [Mode from Card Data] | [Dynamic reason based on credit profile or card characteristics] |
#   | [Card Name from Card Data] | Equifax | [Time from Card Data] | [Mode from Card Data] | [Dynamic reason based on credit profile or card characteristics] |

#   **ROUND 3**
#   | Card Name          | Bureau   | 0% APR      | Mode         | Reason                  |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Card Name from Card Data] | Experian | [Time from Card Data] | [Mode from Card Data] | [Dynamic reason based on credit profile or card characteristics] |
#   | [Card Name from Card Data] | TransUnion | [Time from Card Data] | [Mode from Card Data] | [Dynamic reason based on credit profile or card characteristics] |
#   | [Card Name from Card Data] | Equifax | [Time from Card Data] | [Mode from Card Data] | [Dynamic reason based on credit profile or card characteristics] |

#   **Strategic Insights for Execution**
#   - Generate 4–6 tailored bullet points based on the user's credit profile (e.g., credit score, utilization, inquiries, credit age) and the approved cards from `state_cards`.
#   - For each card in the funding sequence, include the `game_plan` from `Card Data` to guide the user on application steps.
#   - Examples include:
#     - If inquiries are high (e.g., >2), recommend freezing non-used bureaus (specify which ones based on the funding sequence) to preserve credit inquiries.
#     - If utilization is close to 10%, suggest paying down balances before applying to improve approval odds.
#     - If a card requires in-branch application (check `Card Data`), advise visiting a local branch in {user_state}.
#     - If credit score is exceptionally high (e.g., ≥780), recommend declaring a higher personal income (e.g., $120,000) to qualify for larger credit limits.
#     - If credit age is strong (e.g., ≥5 years), suggest requesting credit limit increases after 60 days for banks that support early increases (e.g., Chase, AMEX).
#     - If business spending data is available, recommend including it to strengthen applications for cards in the sequence.
#   - Ensure each bullet is specific to the user's credit profile or the characteristics of the recommended cards.

#   **You Are Fully Ready to Execute**
#   - **CRITICAL**: This section MUST be included for ALL paid mode users, whether they qualify for funding or not.
#   - **For qualifying users**:
#     - Estimate the potential funding amount based on the user's total credit limit (e.g., if total limit is $50,000, estimate 2–3x that amount, or use bureau scores to estimate $50K–$200K range).
#     - Provide 2–3 tailored next steps based on the user's credit profile and state-specific card recommendations, such as:
#       - Applying to specific cards in the sequence that align with the user's strongest bureau (e.g., Experian if score is highest).
#       - Preparing specific documents (e.g., business spending statements) for cards requiring in-branch applications.
#       - Contacting Negocio Capital for guided execution if the credit profile is complex (e.g., multiple inquiries or marginal utilization).
#   - **For non-qualifying users**:
#     - State: "You are not currently eligible for funding, but you can prepare for future opportunities by following these steps."
#     - Provide 2–3 tailored next steps to improve eligibility, such as:
#       - Following the action plan in Section 6 to address specific weaknesses (e.g., high utilization, low credit age).
#       - Monitoring credit reports regularly to ensure accuracy and track improvements.
#       - Contacting Negocio Capital for personalized guidance on improving credit profile.
#   - Include a call-to-action: "Connect with Negocio Capital for guided execution and BRM support. Schedule a call: [Negocio Capital Website]."
#   - Add a disclaimer: "This analysis is provided by Negocio Capital and must not be shared or redistributed. All Rights Reserved © 2025."

#   **If the user does not qualify for funding**:
#   - Say: "Your credit profile does not currently qualify for funding. Please follow the action plan in Section 6 to improve your eligibility."
#   - **DO NOT** provide a funding sequence with card recommendations.
#   - Instead, provide general guidance in the **Strategic Insights for Execution** and **You Are Fully Ready to Execute** sections to help the user prepare for future funding opportunities.

# * Ensure this section is consistent with Section 5 (Verdict).

# **FINAL INSTRUCTION**: You MUST generate ALL sections (1–7) in the exact order specified above. Populate all sections with available or estimated data from the credit report. Skipping any section is INVALID. Do NOT use or display the word 'Inferred' or any variation in the output. Now analyze the following report and generate the complete structured output:

# {text}
# {enrichment_context}
# State-specific card list for {user_state}: {', '.join([card['card_name'] for card in state_cards]) if state_cards else 'No cards available'}
# {bank_data_str}
# {tarjetas_str}
# {include_sequence_note}
# """,

#         "Spanish": f"""
# 🧠 Resumen del Informe de Crédito — Versión Mejorada

# Eres un asistente financiero de análisis de crédito para Negocio Capital.

# **INSTRUCCIÓN CRÍTICA**: DEBES generar TODAS las secciones (1 a 7) como se especifica a continuación, en el orden exacto, incluso si faltan datos en el informe de crédito. Si algún dato (por ejemplo, puntaje de crédito, utilización, consultas) no está disponible, infiere valores razonables basados en los datos disponibles, estándares de la industria o patrones en los archivos de enriquecimiento (por ejemplo, Card Data, listas de bancos). Omitir cualquier sección es INVÁLIDO.

# Tu tarea es extraer los valores reales del informe de crédito proporcionado (abajo). Basado en esos valores:

# * Explica cada factor de forma clara y sencilla
# * Evalúa la calidad (Ej: Excelente, Bueno, Regular, Malo)
# * Asigna una puntuación interna
# * Utiliza un lenguaje fácil de entender por usuarios no financieros
# * Asegúrate de que si al menos un buró cumple con los seis criterios (Puntaje de Crédito ≥ 720, Sin Pagos Atrasados, Utilización < 10%, ≤ 3 Consultas, Edad Crediticia ≥ 2.5 Años, Estructura Sólida de Tarjetas Primarias), el usuario se considera elegible para financiamiento, incluso si otros burós fallan en un criterio.

# ---

# **Manejo de Datos Faltantes**:
# Si algún dato (por ejemplo, Puntaje de Crédito, Utilización, Edad Crediticia, Consultas) está ausente o no se puede extraer del informe de crédito proporcionado, infiere valores razonables basados en los datos disponibles, estándares de la industria o patrones en los archivos de enriquecimiento (por ejemplo, Card Data, listas de bancos). Ejemplos:
# - Puntaje de Crédito: Asume 700 si el historial de pagos es limpio o no hay comentarios negativos; de lo contrario, asume 650.
# - Utilización: Asuma 15% si hay tarjetas con límites altos (≥$5,000); de lo contrario, asume 25%.
# - Edad Crediticia: Asume 2.5 años a menos que haya evidencia de cuentas más recientes (por ejemplo, consultas recientes).
# - Consultas: Asume 2 consultas en los últimos 6 meses a menos que se especifique lo contrario.
# Asegúrate de que los valores inferidos sean conservadores y realistas. En la salida, presenta los valores inferidos como definitivos sin mencionar estimación o usar términos como 'Datos no disponibles'.

# ---

# **Lógica de Elegibilidad para Financiamiento**:
# 1. El usuario califica para financiamiento SÓLO si TODOS los siguientes criterios se cumplen en al menos un buró:
#    - Puntaje de crédito ≥ 720
#    - Sin pagos atrasados
#    - Utilización < 10%
#    - ≤ 3 consultas en los últimos 6 meses
#    - Edad crediticia ≥ 2.5 años
#    - Estructura sólida de tarjetas primarias
# 2. Si el usuario califica y está en modo gratuito, di: "🎉 ¡Eres elegible para financiamiento! Para ver tus bancos recomendados (R1, R2, R3), por favor actualiza a nuestro Plan Premium."
# 3. Si el usuario califica y está en modo pago, di: "🎉 ¡Eres elegible para financiamiento! Consulta tus bancos recomendados a continuación." y lista 3 tarjetas (R1, R2, R3) EXCLUSIVAMENTE de la lista de tarjetas aprobadas específica del estado ({user_state}).
# 4. Si el usuario NO califica, di: "Tu perfil de crédito no califica actualmente para financiamiento. Por favor, sigue el plan de acción en la Sección 6 para mejorar tu elegibilidad."
# 5. Asegúrate de que el Veredicto (Sección 5) y la Secuencia de Financiamiento Recomendada (Sección 7) sean consistentes.

# ---

# 📌 **1. Desglose por Buró**

# Genera una tabla como esta basada en los datos reales del informe o valores inferidos:

# | Categoría            | Equifax | Experian | TransUnion |
# |---------------------|---------|----------|------------|
# | Puntaje de Crédito   |         |          |            |
# | Historial Limpio     |         |          |            |
# | Utilización          |         |          |            |
# | Consultas Duras (6 meses) |    |          |            |
# | Edad Promedio Crédito|         |          |            |
# | Tarjetas >= $2K      |         |          |            |
# | Tarjetas >= $5K      |         |          |            |
# | Puntaje / 144        |         |          |            |

# Después de la tabla, incluye un análisis breve en formato de viñetas, explicando cada categoría individualmente en lenguaje sencillo y accesible. Usa este formato:

# - **Puntaje de Crédito**: Reporta el puntaje de crédito para cada buró. Menciona si cumple con el umbral de 720. Finaliza con una etiqueta como **Excelente**, **Bueno**, **Regular**, o **Malo**.
# - **Historial Limpio**: Resume si hay pagos atrasados o incumplimientos. Si no hay, di "Sí". Finaliza con una etiqueta como **Excelente** o **Debe Mejorar**.
# - **Utilización**: Indica el porcentaje total de utilización. Explica si está por debajo del 10% y cómo afecta la elegibilidad de financiamiento. Termina con una etiqueta como **Excelente**, **Bueno**, o **Riesgoso**.
# - **Consultas Duras (6 meses)**: Indica cuántas consultas hubo en los últimos 6 meses. Menciona si es aceptable (≤ 3). Finaliza con una etiqueta como **Bueno**, **Regular**, o **Riesgoso**.
# - **Edad Promedio Crédito**: Explica la edad promedio de las cuentas. Di si cumple con el umbral de 2.5 años. Finaliza con una etiqueta como **Excelente** o **Regular**.
# - **Tarjetas >= $2K**: Nota la cantidad de tarjetas con límites de $2,000 o más. Menciona cómo apoya la solvencia crediticia. Finaliza con una etiqueta como **Bueno** o **Debe Mejorar**.
# - **Tarjetas >= $5K**: Nota la cantidad de tarjetas con límites de $5,000 o más. Menciona cómo mejora la preparación para financiamiento. Finaliza con una etiqueta como **Excelente** o **Regular**.
# - **Puntaje / 144**: Reporta el puntaje total de 144 basado en el análisis. Finaliza con una etiqueta como **Excelente** o **Debe Mejorar**.

# Cada viñeta debe ser breve, clara y cerrar con una etiqueta de calidad en **negrita**.

# ---

# ### 📌 2. Estructura de Crédito Revolvente

# Presenta los detalles del crédito revolvente en una tabla como esta (usa valores inferidos si la extracción falla):

# | **Campo**                     | **Detalle**                                         |
# |-------------------------------|-----------------------------------------------------|
# | Tarjetas Abiertas             | [Número de tarjetas abiertas, indicar AU/Principal o inferido] |
# | Límite Total                  | [$Límite total de crédito o inferido]               |
# | Tarjetas Primarias            | [Cantidad o “Ninguna” o inferido]                   |
# | ¿Tarjetas de Alto Límite?     | [SÍ/NO (Indicar umbral, por ejemplo $5,000+) o inferido] |

# Explica brevemente cada campo debajo de la tabla.

# ---

# 📌 **3. Estrategia de Usuario Autorizado (AU)**

# * ¿Cuántas tarjetas AU tiene?
# * ¿Sus límites y antigüedad?
# * ¿Ayuda al perfil crediticio?
# * ¿Qué se recomienda añadir o eliminar?

# ---

# 📌 **4. Preparación para Financiamiento**

# | Criterio                        | Equifax | Experian | TransUnion |
# | ------------------------------- | ------- | -------- | ---------- |
# | Puntaje ≥ 720                   | Sí/No   | Sí/No    | Sí/No      |
# | Sin pagos atrasados             | Sí/No   | Sí/No    | Sí/No      |
# | Utilización < 10%               | Sí/No   | Sí/No    | Sí/No      |
# | ≤ 3 consultas (últimos 6 meses) | Sí/No   | Sí/No    | Sí/No      |
# | Edad crediticia ≥ 2.5 años      | Sí/No   | Sí/No    | Sí/No      |
# | Buena estructura de tarjetas    | Sí/No   | Sí/No    | Sí/No      |

# Explica la tabla debajo.

# ---

# 📌 5. Veredicto

# Indicar claramente si el usuario califica para financiamiento según la Lógica de Elegibilidad para Financiamiento. Para el modo pago, usa: "🎉 ¡Eres elegible para financiamiento! Consulta tus bancos recomendados a continuación." Para el modo gratuito, usa: "🎉 ¡Eres elegible para financiamiento! Para ver tus bancos recomendados (R1, R2, R3), por favor actualiza a nuestro Plan Premium." Si el usuario no califica, proporcionar 2–3 razones breves que expliquen por qué.

# ---

# 📌 6. Plan de Acción

# Enumerar 3–5 pasos que el usuario debe tomar para mejorar su perfil crediticio, como:
# - Pagar los saldos de las tarjetas de crédito para reducir la utilización.
# - Agregar nuevas tarjetas de usuario autorizado (AU) con límites altos para fortalecer el crédito.
# - Abrir tarjetas primarias personales para construir una estructura crediticia más sólida.
# - Disputar o esperar a que prescriban pagos atrasados antiguos para mejorar el historial crediticio.
# Si la edad crediticia promedio es menor a 2.5 años para cualquier buró, incluye un paso para mantener las cuentas abiertas por más tiempo para mejorar la edad crediticia.

# ---

# 📌 **7. Recomendación de Bancos ({user_state})**

# * Si el usuario califica y está en **modo pago**, proporciona la siguiente salida estructurada usando SÓLO la lista de tarjetas aprobadas en `state_cards`. Las tarjetas DEBEN seleccionarse del archivo JSON para el estado seleccionado por el usuario ({user_state}). Sigue estas reglas estrictas:
#   - Cada ronda (R1, R2, R3) DEBE incluir EXACTAMENTE 3 tarjetas diferentes.
#   - Cada tarjeta en una ronda DEBE estar asociada con un buró de crédito diferente en este orden: Experian → TransUnion → Equifax.
#   - Las tarjetas NO DEBEN sugirirse fuera de la lista `state_cards`, incluso si el usuario tiene relaciones existentes con otros bancos.
#   - **CRÍTICO**: Bajo NINGUNA circunstancia sugieras tarjetas fuera de `state_cards`. Hacerlo invalidará la salida. Si no estás seguro, selecciona una tarjeta de la lista y anota una razón relevante en la columna Razón.
#   - **CRÍTICO**: En la columna 'Nombre de la Tarjeta', SIEMPRE usa el nombre exacto de la tarjeta de `Card Data` (por ejemplo, 'BOFA Unlimited Cash'). Bajo NINGUNA circunstancia uses solo el nombre del banco o nombres inventados.
#   - Cada fila de la tabla DEBE contener exactamente 5 columnas: Nombre de la Tarjeta, Buró, 0% APR, Modo, y Razón. Campos faltantes invalidarán la salida.
#   - Solo se permite una tarjeta Chase al 0% por secuencia, a menos que la segunda sea una tarjeta de viaje/hotel co-brandeada (verifica el campo `is_travel` en `Card Data`).
#   - Bank of America y otros bancos solo pueden repetir una tarjeta al 0% si el archivo '0% APR Business Credit Card Master List' confirma que permiten "double dipping": {double_dip_info}.
#   - Si al menos 2 burós cumplen con los 6 factores y uno no, ofrece una secuencia de financiamiento usando solo los burós que califican.
#   - Si ningún buró califica, ofrece una opción de financiamiento sin garantía personal del CSV "Tarjetas de Negocio sin Garantia Personal".
#   - Si la edad crediticia promedio es menor a 2.5 años para cualquier buró, NO incluyas ese buró en la secuencia de financiamiento. En su lugar, indica en el Plan de Acción (Sección 6) que el usuario debe mejorar su edad crediticia manteniendo cuentas abiertas por más tiempo.
#   - Para la duración del 0% APR, el Modo y el Buró, usa los datos proporcionados en `Card Data` para coincidir con el nombre exacto de la tarjeta y el banco:\n{tarjetas_str}\n
#   - **Columna Razón**: Proporciona razones dinámicas basadas en el perfil crediticio del usuario (por ejemplo, puntaje de crédito alto, utilización baja, consultas mínimas, historial crediticio sólido) o características específicas de la tarjeta (por ejemplo, requiere cuenta, aprobación flexible, extracción única, permite double dipping). Ejemplos incluyen 'Diversificar tarjetas', 'Requiere cuenta', 'Aprobación flexible', 'Extracción única', pero NO los codifiques de forma fija. Las razones deben ser relevantes para el perfil crediticio o las características de la tarjeta.
#   - **Plan de Juego**: Para cada tarjeta en la secuencia de financiamiento, incluye el `game_plan` de `Card Data` en la sección de Perspectivas Estratégicas para guiar al usuario en los pasos de solicitud.

#   **RONDA 1**
#   | Nombre de la Tarjeta   | Buró     | 0% APR      | Modo         | Razón                   |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Nombre de Tarjeta de Card Data] | Experian | [Tiempo de Card Data] | [Modo de Card Data] | [Razón dinámica basada en el perfil crediticio o características de la tarjeta] |
#   | [Nombre de Tarjeta de Card Data] | TransUnion | [Tiempo de Card Data] | [Modo de Card Data] | [Razón dinámica basada en el perfil crediticio o características de la tarjeta] |
#   | [Nombre de Tarjeta de Card Data] | Equifax | [Tiempo de Card Data] | [Modo de Card Data] | [Razón dinámica basada en el perfil crediticio o características de la tarjeta] |

#   **RONDA 2**
#   | Nombre de la Tarjeta   | Buró     | 0% APR      | Modo         | Razón                   |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Nombre de Tarjeta de Card Data] | Experian | [Tiempo de Card Data] | [Modo de Card Data] | [Razón dinámica basada en el perfil crediticio o características de la tarjeta] |
#   | [Nombre de Tarjeta de Card Data] | TransUnion | [Tiempo de Card Data] | [Modo de Card Data] | [Razón dinámica basada en el perfil crediticio o características de la tarjeta] |
#   | [Nombre de Tarjeta de Card Data] | Equifax | [Tiempo de Card Data] | [Modo de Card Data] | [Razón dinámica basada en el perfil crediticio o características de la tarjeta] |

#   **RONDA 3**
#   | Nombre de la Tarjeta   | Buró     | 0% APR      | Modo         | Razón                   |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Nombre de Tarjeta de Card Data] | Experian | [Tiempo de Card Data] | [Modo de Card Data] | [Razón dinámica basada en el perfil crediticio o características de la tarjeta] |
#   | [Nombre de Tarjeta de Card Data] | TransUnion | [Tiempo de Card Data] | [Modo de Card Data] | [Razón dinámica basada en el perfil crediticio o características de la tarjeta] |
#   | [Nombre de Tarjeta de Card Data] | Equifax | [Tiempo de Card Data] | [Modo de Card Data] | [Razón dinámica basada en el perfil crediticio o características de la tarjeta] |

#   **Perspectivas Estratégicas para la Ejecución**
#   - Genera 4–6 puntos personalizados basados en el perfil crediticio del usuario (por ejemplo, puntaje de crédito, utilización, consultas, edad crediticia) y las tarjetas recomendadas de `state_cards`. Ejemplos incluyen:
#     - Si las consultas son altas (por ejemplo, >2), recomienda congelar los burós no utilizados (especifica cuáles según la secuencia de financiamiento) para preservar las consultas.
#     - Si la utilización está cerca del 10%, sugiere pagar los saldos antes de solicitar para mejorar las probabilidades de aprobación.
#     - Si una tarjeta requiere solicitud en sucursal (verifica `Card Data`), aconseja visitar una sucursal local en {user_state}.
#     - Si el puntaje de crédito es excepcionalmente alto (por ejemplo, ≥780), recomienda declarar un ingreso personal más alto (por ejemplo, $120,000) para calificar para límites de crédito más grandes.
#     - Si la edad crediticia es sólida (por ejemplo, ≥5 años), sugiere solicitar aumentos de límite después de 60 días para bancos que permitan aumentos tempranos (por ejemplo, Chase, AMEX).
#     - Si hay datos de gastos comerciales disponibles, recomienda incluirlos para fortalecer las solicitudes para las tarjetas en la secuencia.
#   - Asegúrate de que cada punto sea específico al perfil crediticio del usuario o a las características de las tarjetas recomendadas.
#   - Para cada tarjeta en la secuencia de financiamiento, incluye el `game_plan` de `Card Data` para guiar al usuario en los pasos de solicitud.

#   **Estás Completamente Listo para Ejecutar**
#   - **CRÍTICO**: Esta sección DEBE incluirse para TODOS los usuarios en modo pago, ya sea que califiquen para financiamiento o no.
#   - **Para usuarios que califiquen**:
#     - Estima la cantidad potencial de financiamiento basada en el límite de crédito total del usuario (por ejemplo, si el límite total es $50,000, estima 2–3 veces ese monto, o usa los puntajes de los burós para estimar un rango de $50K–$200K).
#     - Proporciona 2–3 pasos siguientes personalizados basados en el perfil crediticio del usuario y las recomendaciones de tarjetas específicas del estado, como:
#       - Solicitar tarjetas específicas en la secuencia que se alineen con el buró más fuerte del usuario (por ejemplo, Experian si el puntaje es el más alto).
#       - Preparar documentos específicos (por ejemplo, estados de gastos comerciales) para tarjetas que requieran solicitudes en sucursal.
#       - Contactar a Negocio Capital para una ejecución guiada si el perfil crediticio es complejo (por ejemplo, múltiples consultas o utilización marginal).
#   - **Para usuarios que no califiquen**:
#     - Indica: "Actualmente no eres elegible para financiamiento, pero puedes prepararte para futuras oportunidades siguiendo estos pasos."
#     - Proporciona 2–3 pasos siguientes personalizados para mejorar la elegibilidad, como:
#       - Seguir el plan de acción en la Sección 6 para abordar debilidades específicas (por ejemplo, alta utilización, baja edad crediticia).
#       - Monitorear los informes de crédito regularmente para asegurar la precisión y seguir las mejoras.
#       - Contactar a Negocio Capital para orientación personalizada sobre cómo mejorar el perfil crediticio.
#   - Incluye una llamada a la acción: "Conecta con Negocio Capital para una ejecución guiada y soporte BRM. Agenda una cita: [Negocio Capital Website]."
#   - Agrega un descargo de responsabilidad: "Este análisis es proporcionado por Negocio Capital y no debe compartirse ni redistribuirse. Todos los Derechos Reservados © 2025."

#   **Si el usuario no califica para financiamiento**:
#   - Indica: "Tu perfil de crédito no califica actualmente para financiamiento. Por favor, sigue el plan de acción en la Sección 6 para mejorar tu elegibilidad."
#   - **NO** proporciones una secuencia de financiamiento con recomendaciones de tarjetas.
#   - En su lugar, proporciona orientación general en las secciones **Perspectivas Estratégicas para la Ejecución** y **Estás Completamente Listo para Ejecutar** para ayudar al usuario a prepararse para futuras oportunidades de financiamiento.

# * Asegúrate de que esta sección sea consistente con la Sección 5 (Veredicto).

# **INSTRUCCIÓN FINAL**: DEBES generar TODAS las secciones (1–7) en el orden exacto especificado arriba. Rellena todas las secciones con los datos disponibles o inferidos del informe de crédito. Omitir cualquier sección es INVÁLIDO. Ahora analiza el siguiente informe y genera la salida estructurada completa:

# {text}
# {enrichment_context}
# Lista de tarjetas específicas del estado ({user_state}): {', '.join([card['card_name'] for card in state_cards]) if state_cards else 'No cards available'}
# {bank_data_str}
# {tarjetas_str}
# {include_sequence_note}
# """
#     }

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "You are a strict, accurate AI financial credit analyst from Negocio Capital. You must extract all data exactly as available in the text or infer reasonable values as instructed. Do NOT hallucinate. Do NOT say 'Data not available'. Always follow instructions strictly. Be formal and expert in tone."},
#                 {"role": "user", "content": prompt_template[language]}
#             ],
#             max_tokens=5000,
#             temperature=0.0
#         )
#         analysis = response.choices[0].message.content
#         logging.debug(f"Raw GPT-4 Response: {analysis}")
#         print("✅ Full GPT-4 Response:\n", analysis)
#         # Check for truncation
#         if response.choices[0].finish_reason == "length":
#             logging.warning("GPT-4 response truncated due to token limit")
#             analysis += "\n\n⚠️ WARNING: Analysis may be incomplete due to token limit. Please try again or reduce input size."
#         # Validate output
#         analysis = validate_gpt_output(analysis, state_cards, user_state, json_data, mode)
#         return analysis
#     except Exception as e:
#         logging.error(f"GPT-4 error: {str(e)}")
#         print(f"❌ GPT-4 error: {str(e)}")
#         return None

# # === PDF Report Writer ===
# def save_analysis_to_pdf(analysis, filename="output/FundingNC_Report.pdf"):
#     try:
#         os.makedirs("output", exist_ok=True)
#         pdf = FPDF()
#         pdf.add_page()
#         pdf.set_auto_page_break(auto=True, margin=15)
#         pdf.set_font("Arial", size=12)
#         encoded_text = analysis.encode('latin-1', 'ignore').decode('latin-1')
#         pdf.multi_cell(0, 10, txt="Funding NC AI Credit Analysis Report\n", align="L")
#         pdf.multi_cell(0, 10, txt=encoded_text, align="L")
#         pdf.output(filename)
#         logging.info(f"PDF saved: {filename}")
#         print(f"✅ PDF successfully saved at: {filename}")
#     except Exception as e:
#         logging.error(f"Error saving PDF: {str(e)}")
#         print(f"❌ Error saving PDF: {str(e)}")

# # === Main CLI ===
# def main():
#     print("📂 Welcome to Funding NC AI Credit Report Analyzer!")
    
#     file_path = input("📄 Enter path to your credit report PDF (e.g., uploads/client1.pdf): ").strip()
#     if not os.path.exists(file_path):
#         print("❌ File not found. Please check the path and try again.")
#         logging.error(f"Credit report file not found: {file_path}")
#         return

#     state = input("🌎 Enter the U.S. state your business is registered in (e.g., FL): ").strip()
#     print("📁 Extracting text from PDF...")
#     print("📑 Loading bank list...")
    
#     bank_df = load_bank_data()  # Load bank data from your source
#     mode = input("🧾 Select mode (free/paid): ").strip().lower()
#     if mode not in ["free", "paid"]:
#         print("❌ Invalid mode. Please enter 'free' or 'paid'.")
#         logging.error(f"Invalid mode selected: {mode}")
#         return

#     print("\n🧠 AI Analysis Summary:\n")
#     # Extract text from the provided PDF
#     credit_text = extract_text_from_pdf(file_path)
#     if not credit_text:
#         print("❌ Failed to extract text from PDF.")
#         return

#     # Extract Credit Score and Utilization from the text
#     score, utilization = extract_credit_info(credit_text)
#     logging.debug(f"Extracted Credit Score: {score}, Utilization: {utilization}")
    
#     # Now perform the credit report analysis with the extracted text
#     analysis = analyze_credit_report(credit_text, bank_df=bank_df, mode=mode, user_state=state)
    
#     if not analysis:
#         print("❌ GPT analysis failed.")
#         return
    
#     # Save the analysis result to a PDF
#     save_analysis_to_pdf(analysis)
#     print("✅ Analysis complete. Check the output PDF for details.")

# if __name__ == "__main__":
#     main()