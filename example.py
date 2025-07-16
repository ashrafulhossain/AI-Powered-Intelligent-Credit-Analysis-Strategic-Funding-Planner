
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
# STATE_SEQUENCE_PATH = "data/0% Funding Sequence Per State.xlsx"
# TARJETAS_PATH = "data/Tarjetas de crédito de negocio con garantía personal 2025.pdf"
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

# # === Tarjetas Data ===
# TARJETAS_CARDS = {
#     "Chase Ink Unlimited": {"apr": "12 MESES", "mode": "Online", "bank": "Chase"},
#     "Chase Ink Cash": {"apr": "12 MESES", "mode": "Online", "bank": "Chase"},
#     "BOFA Unlimited Cash": {"apr": "9 MESES", "mode": "Online", "bank": "Bank of America"},
#     "BOFA Cash Rewards": {"apr": "9 MESES", "mode": "Online", "bank": "Bank of America"},
#     "BOFA Travel Rewards": {"apr": "9 MESES", "mode": "Online", "bank": "Bank of America"},
#     "BOFA Platinum Plus": {"apr": "9 MESES", "mode": "Online", "bank": "Bank of America"},
#     "PNC Visa Business": {"apr": "12 MESES", "mode": "Online (requires account)", "bank": "PNC"},
#     "US Bank Triple Cash": {"apr": "12 MESES", "mode": "Online", "bank": "US Bank"},
#     "US Bank Business Leverage": {"apr": "12 MESES", "mode": "Online", "bank": "US Bank"},
#     "US Bank Business Platinum": {"apr": "18 MESES", "mode": "Online", "bank": "US Bank"},
#     "Amex Business Gold": {"apr": "6 MESES", "mode": "Online", "bank": "American Express"},
#     "Amex Blue Biz Cash": {"apr": "12 MESES", "mode": "Online", "bank": "American Express"},
#     "Amex Blue Biz Plus": {"apr": "12 MESES", "mode": "Online", "bank": "American Express"},
#     "Wells Fargo Unlimited 2%": {"apr": "12 MESES", "mode": "Online", "bank": "Wells Fargo"},
#     "Citizens Biz Platinum": {"apr": "12 MESES", "mode": "In-branch/Phone", "bank": "Citizens Bank"},
#     "FNBO Evergreen Biz": {"apr": "6 MESES", "mode": "Online (Omaha Zip)", "bank": "FNBO"},
#     "BMO Business Platinum Rewards": {"apr": "9 MESES", "mode": "In-branch", "bank": "BMO Harris"},
#     "BMO Business Platinum": {"apr": "12 MESES", "mode": "In-branch", "bank": "BMO Harris"},
#     "Truist Business Cash": {"apr": "9 MESES", "mode": "Online", "bank": "Truist"},
#     "Truist Business Card": {"apr": "12 MESES", "mode": "Online", "bank": "Truist"},
#     "KeyBank Business Card": {"apr": "6 MESES", "mode": "Phone/In-branch", "bank": "KeyBank"},
#     "KeyBank Business Rewards": {"apr": "6 MESES", "mode": "Phone/In-branch", "bank": "KeyBank"},
#     "KeyBank Business Cash": {"apr": "6 MESES", "mode": "Phone/In-branch", "bank": "KeyBank"},
#     "M&T Bank Business Card": {"apr": "12 MESES", "mode": "Online", "bank": "M&T Bank"},
#     "Valley National Card": {"apr": "12 MESES", "mode": "Online", "bank": "Valley National"}
# }

# # === Text Extractors ===
# def extract_text_from_pdf(pdf_path):
#     try:
#         text = ""
#         with fitz.open(pdf_path) as doc:
#             for page in doc:
#                 text += page.get_text()
#         logging.info(f"Successfully extracted text from PDF: {pdf_path}")
#         logging.debug(f"Extracted credit report text: {text[:1000]}...")
#         return text
#     except Exception as lỗi:
#         logging.error(f"Error extracting PDF text from {pdf_path}: {str(lỗi)}")
#         return None

# def extract_text_from_docx(docx_path):
#     try:
#         doc = Document(docx_path)
#         text = "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])
#         logging.info(f"Successfully extracted text from DOCX: {docx_path}")
#         return text
#     except Exception as lỗi:
#         logging.error(f"Error extracting DOCX text from {docx_path}: {str(lỗi)}")
#         return None

# def extract_text_from_csv(csv_path):
#     try:
#         df = pd.read_csv(csv_path)
#         text = df.to_string(index=False)
#         logging.info(f"Successfully extracted text from CSV: {csv_path}")
#         return text
#     except Exception as lỗi:
#         logging.error(f"Error extracting CSV text from {csv_path}: {str(lỗi)}")
#         return None

# # === Update TARJETAS_CARDS from PDF ===
# def update_tarjetas_from_pdf(pdf_path):
#     try:
#         text = extract_text_from_pdf(pdf_path)
#         if not text:
#             logging.error("Failed to extract text from Tarjetas PDF")
#             return

#         # Assuming PDF format: "Card Name: BOFA Unlimited Cash, Bank: Bank of America, APR: 9 MESES"
#         # Adjust the regex based on the actual PDF format
#         pattern = r"Card Name: (.*?),\s*Bank: (.*?),\s*APR: (\d+ MESES)"
#         matches = re.findall(pattern, text, re.MULTILINE)
        
#         for card_name, bank, apr in matches:
#             TARJETAS_CARDS[card_name.strip()] = {
#                 "apr": apr.strip(),
#                 "mode": "Online",  # Default mode, update if PDF provides mode
#                 "bank": bank.strip()
#             }
#             logging.info(f"Added card from PDF: {card_name}, Bank: {bank}, APR: {apr}")
#         print(f"✅ Updated TARJETAS_CARDS with {len(matches)} new cards from PDF")
#     except Exception as lỗi:
#         logging.error(f"Error updating TARJETAS_CARDS from PDF: {str(lỗi)}")
#         print(f"❌ Error updating TARJETAS_CARDS: {str(lỗi)}")

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
#     except Exception as lỗi:
#         logging.error(f"Failed to load bank list: {str(lỗi)}")
#         print(f"❌ Failed to load bank list: {str(lỗi)}")
#         return None

# def get_state_funding_banks(user_state):
#     try:
#         df = pd.read_excel(STATE_SEQUENCE_PATH, sheet_name="Sheet1")
#         df.columns = df.columns.str.strip()
#         logging.info(f"State sequence file columns: {list(df.columns)}")
#         logging.info(f"First few rows of state sequence file:\n{df.head().to_string()}")

#         if 'STATE' not in df.columns:
#             logging.error("No 'STATE' column found in state sequence file")
#             return None

#         matched = df[df['STATE'].str.lower() == user_state.lower()]
#         if matched.empty:
#             logging.error(f"No state-specific banks found for {user_state}")
#             return None

#         banks = matched.iloc[0, 1:].dropna().tolist()
#         if not banks:
#             logging.error(f"No banks listed for {user_state} after dropping NA")
#             return None

#         cleaned_banks = []
#         for bank in banks:
#             bank_str = str(bank).strip()
#             if bank_str and not bank_str.isspace() and not bank_str.lower() == 'nan':
#                 cleaned_banks.append(bank_str)

#         logging.info(f"Found {len(cleaned_banks)} banks for state {user_state}: {cleaned_banks}")
#         print(f"✅ Found {len(cleaned_banks)} banks for state {user_state}: {cleaned_banks}")
#         return cleaned_banks
#     except Exception as lỗi:
#         logging.error(f"Could not load state funding data: {str(lỗi)}")
#         print(f"❌ Could not load state funding data: {str(lỗi)}")
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
#             except Exception as lỗi:
#                 enrichment += f"\n[Error reading {file}]: {str(lỗi)}\n"
#                 logging.error(f"Error reading enrichment file {file}: {str(lỗi)}")
#         else:
#             enrichment += f"\n[Skipped missing file: {file}]\n"
#             logging.warning(f"Skipped missing enrichment file: {file}")
#     return enrichment

# # === Output Validation ===
# def validate_gpt_output(analysis, state_bank_suggestion, user_state, mode="free"):
#     analysis_lower = analysis.lower()
#     not_qualified = "does not qualify for funding" in analysis_lower
#     eligible_message = "you are eligible for funding" in analysis_lower

#     # Check for missing sections
#     required_sections = [
#         r"📌.*Breakdown by Bureau",
#         r"📌.*Revolving Credit Structure",
#         r"📌.*Authorized User.*Strategy",
#         r"📌.*Funding Readiness by Bureau",
#         r"📌.*Verdict",
#         r"📌.*Action Plan",
#         r"📌.*Recommended Funding Sequence"
#     ]
#     missing_sections = [sec for sec in required_sections if not re.search(sec, analysis, re.IGNORECASE)]
#     if missing_sections:
#         missing_names = [re.search(r"\.\*(.*?)(?=\||\Z)", sec).group(1).strip() for sec in missing_sections]
#         logging.error(f"Missing sections in GPT output: {missing_names}")
#         error_note = f"\n\n⚠️ ERROR: Missing sections in analysis: {', '.join(missing_names)}. Please check the credit report data or API response."
#         logging.debug(f"Before adding missing sections note: {analysis[:500]}...")
#         analysis += error_note
#         logging.debug(f"After adding missing sections note: {analysis[:500]}...")

#     # Fix inconsistent verdict in free mode
#     if mode == "free" and eligible_message and not_qualified:
#         logging.warning("Inconsistent GPT output in free mode: Eligible in Section 5 but not qualified in Section 7.")
#         print("❌ Fixing inconsistent GPT output in free mode.")
#         analysis = re.sub(
#             r"Your credit profile does not currently qualify for funding.*?(?=\*\*Strategic Insights|\Z)",
#             "🎉 You're eligible for funding! To view your matched bank recommendations (R1, R2, R3), please upgrade to our Premium Plan.",
#             analysis,
#             flags=re.DOTALL
#         )
#         logging.info("Fixed inconsistent verdict in free mode.")

#     # Fix inconsistent verdict in paid mode
#     if mode == "paid" and not_qualified and eligible_message:
#         logging.warning("Inconsistent GPT output: Verdict says not qualified, but Funding Sequence says eligible.")
#         print("❌ Fixing inconsistent GPT output.")
#         analysis = re.sub(
#             r"🎉 You are eligible for funding!.*?(?=\*\*Strategic Insights|\Z)",
#             "Your credit profile does not currently qualify for funding. Please follow the action plan in Section 6 to improve your eligibility.",
#             analysis,
#             flags=re.DOTALL
#         )
#         logging.info("Fixed inconsistent verdict in paid mode.")

#     # Fix incorrect verdict message for paid mode
#     if mode == "paid" and "please upgrade to our Premium Plan" in analysis_lower:
#         logging.error("Incorrect verdict message for paid mode")
#         analysis = re.sub(
#             r"🎉 You're eligible for funding! To view your matched bank recommendations.*?Plan\.",
#             "🎉 You're eligible for funding! See your matched bank recommendations below.",
#             analysis
#         )
#         logging.info("Fixed incorrect verdict message for paid mode.")

#     # Validate Section 7 for three different banks and bureaus per round
#     rounds = re.findall(r"\*\*ROUND [1-3]\*\*(.*?)(?=\*\*ROUND|\*\*Strategic Insights|\Z)", analysis, re.DOTALL)
#     valid_modes = ["Online", "In-branch", "Phone", "Online (requires account)", "Online (Omaha Zip)", "Phone/In-branch"]
#     for i, round_content in enumerate(rounds, 1):
#         # Robust parsing for table rows
#         rows = re.findall(r"\|\s*([^\|]+?)\s*\|\s*(Experian|TransUnion|Equifax)\s*\|\s*([0-9]+ MESES|Default [0-9]+ MESES|0%)?\s*\|\s*([^\|]*?)\s*\|\s*([^\|]*?)\s*\|", round_content)
#         bureaus = []
#         banks = []
#         invalid_banks = []
#         apr_mismatches = []
#         mode_mismatches = []
#         default_usage = []
#         invalid_reasons = []

#         for row in rows:
#             card_name, bureau, apr, mode, reason = row
#             card_name_clean = card_name.strip()
#             bureau = bureau.strip()
#             apr = apr.strip() if apr else "12 MESES"  # Default APR
#             mode = mode.strip() if mode else "Online"  # Default Mode
#             reason = reason.strip()
#             bureaus.append(bureau)
#             banks.append(card_name_clean)

#             # Validate card against state_bank_suggestion
#             matched = False
#             card_bank = None
#             for card, card_info in TARJETAS_CARDS.items():
#                 if card.lower() in card_name_clean.lower():
#                     card_bank = card_info['bank']
#                     matched = any(card_bank.lower() in approved_bank.lower() or approved_bank.lower() in card_bank.lower() for approved_bank in state_bank_suggestion)
#                     break
#             if not matched:
#                 invalid_banks.append(card_name_clean)
#                 logging.error(f"Card {card_name_clean} in Round {i} is not in state_bank_suggestion for {user_state}: {state_bank_suggestion}")
#                 error_note = f"\n\n⚠️ ERROR: Card {card_name_clean} in Round {i} is not in the approved bank list for {user_state}. Replacing with a valid card."
#                 if error_note not in analysis:
#                     analysis += error_note
#                 # Replace invalid card with a valid one from state_bank_suggestion
#                 replacement_bank = next((b for b in state_bank_suggestion if b not in [TARJETAS_CARDS.get(c, {}).get('bank', '') for c in banks]), state_bank_suggestion[0])
#                 replacement_card = None
#                 for card, card_info in TARJETAS_CARDS.items():
#                     if replacement_bank.lower() in card_info['bank'].lower():
#                         replacement_card = card
#                         break
#                 if replacement_card:
#                     replacement_apr = TARJETAS_CARDS[replacement_card]['apr']
#                     replacement_mode = TARJETAS_CARDS[replacement_card]['mode']
#                     replacement_reason = "Strong credit history"
#                 else:
#                     replacement_card = f"{replacement_bank} Card"
#                     replacement_apr = "12 MESES"
#                     replacement_mode = "Online"
#                     replacement_reason = f"Default card for {replacement_bank}"
#                 analysis = re.sub(
#                     r"\|\s*" + re.escape(card_name_clean) + r"\s*\|\s*" + bureau + r"\s*\|\s*[^\|]*?\s*\|\s*[^\|]*?\s*\|\s*[^\|]*?\s*\|",
#                     f"| {replacement_card} | {bureau} | {replacement_apr} | {replacement_mode} | {replacement_reason} |",
#                     analysis
#                 )

#             # Validate APR and Mode against Tarjetas data
#             tarjeta_match = None
#             for card, card_info in TARJETAS_CARDS.items():
#                 if card.lower() in card_name_clean.lower():
#                     tarjeta_match = card_info
#                     break
#             if tarjeta_match:
#                 expected_apr = tarjeta_match['apr']
#                 expected_mode = tarjeta_match['mode'].split(' (')[0]  # Remove notes like '(Omaha Zip)'
#                 if apr != expected_apr:
#                     apr_mismatches.append((card_name_clean, expected_apr, apr))
#                     logging.error(f"APR mismatch for {card_name_clean} in Round {i}: Expected {expected_apr}, Got {apr}")
#                     error_note = f"\n\n⚠️ ERROR: APR for {card_name_clean} in Round {i} is incorrect. Expected {expected_apr}, Got {apr}."
#                     if error_note not in analysis:
#                         analysis += error_note
#                     analysis = re.sub(
#                         r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|).*?(\|.*?\|).*?(\|)",
#                         f"|\1{bureau}|{expected_apr}|{mode}|{reason}|",
#                         analysis
#                     )
#                 if mode.lower() != expected_mode.lower():
#                     mode_mismatches.append((card_name_clean, expected_mode, mode))
#                     logging.error(f"Mode mismatch for {card_name_clean} in Round {i}: Expected {expected_mode}, Got {mode}")
#                     error_note = f"\n\n⚠️ ERROR: Mode for {card_name_clean} in Round {i} is incorrect. Expected {expected_mode}, Got {mode}."
#                     if error_note not in analysis:
#                         analysis += error_note
#                     analysis = re.sub(
#                         r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|.*?\|).*?(\|.*?\|)",
#                         f"|\1{bureau}|{apr}|{expected_mode}|{reason}|",
#                         analysis
#                     )
#             else:
#                 # Handle non-listed cards
#                 if card_name_clean.lower() == "pacific premier bank":
#                     replacement_apr = "6 MESES"
#                     replacement_mode = "Online (Omaha Zip)"
#                     replacement_reason = reason
#                 else:
#                     replacement_apr = "12 MESES"
#                     replacement_mode = "Online"
#                     replacement_reason = f"Default card for {card_name_clean}"
#                 default_usage.append(card_name_clean)
#                 logging.warning(f"No Tarjetas data found for {card_name_clean} in Round {i}. Using default APR: {replacement_apr}, Mode: {replacement_mode}")
#                 analysis = re.sub(
#                     r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|).*?(\|.*?\|).*?(\|)",
#                     f"|\1{bureau}|{replacement_apr}|{replacement_mode}|{replacement_reason}|",
#                     analysis
#                 )
#                 # Ensure card name for non-listed banks
#                 if not any(card.lower() in card_name_clean.lower() for card in TARJETAS_CARDS):
#                     new_card_name = f"{card_name_clean} Card"
#                     analysis = re.sub(
#                         r"\|\s*" + re.escape(card_name_clean) + r"\s*\|\s*" + bureau,
#                         f"| {new_card_name} | {bureau}",
#                         analysis
#                     )

#             # Fix invalid APR values (e.g., "0%")
#             if apr == "0%":
#                 logging.error(f"Invalid APR '0%' for {card_name_clean} in Round {i}. Replacing with default '12 MESES'.")
#                 error_note = f"\n\n⚠️ ERROR: Invalid APR '0%' for {card_name_clean} in Round {i}. Replaced with '12 MESES'."
#                 if error_note not in analysis:
#                     analysis += error_note
#                 analysis = re.sub(
#                     r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|).*?(\|.*?\|).*?(\|)",
#                     f"|\1{bureau}|12 MESES|{mode}|{reason}|",
#                     analysis
#                 )

#             # Fix invalid Mode values
#             if mode not in valid_modes:
#                 logging.error(f"Invalid mode '{mode}' for {card_name_clean} in Round {i}. Replacing with 'Online'.")
#                 error_note = f"\n\n⚠️ ERROR: Invalid mode '{mode}' for {card_name_clean} in Round {i}. Replaced with 'Online'."
#                 if error_note not in analysis:
#                     analysis += error_note
#                 analysis = re.sub(
#                     r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|.*?\|).*?(\|.*?\|)",
#                     f"|\1{bureau}|{apr}|Online|{reason}|",
#                     analysis
#                 )

#             # Validate Reason column
#             valid_reasons = [
#                 r"diversify cards",
#                 r"requires account",
#                 r"flexible approval",
#                 r"single pull",
#                 r"high credit score",
#                 r"low utilization",
#                 r"minimal inquiries",
#                 r"strong credit history",
#                 r"supports double dip",
#                 r"strong primary card structure, excellent credit management"
#             ]
#             reason_valid = any(re.search(pattern, reason.lower()) for pattern in valid_reasons)
#             if not reason_valid or "missing credit data" in reason.lower():
#                 invalid_reasons.append((card_name_clean, reason))
#                 logging.warning(f"Invalid or undesired reason for {card_name_clean} in Round {i}: {reason}")
#                 error_note = f"\n\n⚠️ WARNING: Invalid or undesired reason for {card_name_clean} in Round {i}: '{reason}'. Replacing with a dynamic reason."
#                 if error_note not in analysis:
#                     analysis += error_note
#                 replacement_reason = "Diversify cards"
#                 if "requires account" in mode.lower():
#                     replacement_reason = "Requires account"
#                 elif "in-branch" in mode.lower():
#                     replacement_reason = "Flexible approval"
#                 elif "online" in mode.lower():
#                     replacement_reason = "Single pull"
#                 elif "high credit score" in analysis_lower:
#                     replacement_reason = "High credit score"
#                 elif "low utilization" in analysis_lower:
#                     replacement_reason = "Low utilization"
#                 elif "minimal inquiries" in analysis_lower:
#                     replacement_reason = "Minimal inquiries"
#                 else:
#                     replacement_reason = "Strong credit history"
#                 analysis = re.sub(
#                     r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|.*?\|.*?\|).*?(\|)",
#                     f"|\1{bureau}|{apr}|{mode}|{replacement_reason}|",
#                     analysis
#                 )

#         # Check bureau variety
#         if len(set(bureaus)) != 3 or bureaus != ['Experian', 'TransUnion', 'Equifax']:
#             logging.warning(f"Invalid bureau variety in Round {i}: {bureaus}")
#             error_note = f"\n\n⚠️ WARNING: Round {i} does not contain exactly one of each bureau (Experian, TransUnion, Equifax) in order."
#             if error_note not in analysis:
#                 analysis += error_note

#         # Check bank variety
#         if len(set(banks)) != 3 or len(banks) != 3:
#             logging.warning(f"Invalid bank variety in Round {i}: {banks}")
#             error_note = f"\n\n⚠️ WARNING: Round {i} does not contain exactly three different banks."
#             if error_note not in analysis:
#                 analysis += error_note

#         # Log banks and bureaus for this round
#         logging.info(f"Round {i} Cards: {banks}, Bureaus: {bureaus}")

#         # Validation summary
#         analysis += f"\n\n📋 Round {i} Validation Summary:\n"
#         analysis += f"- Total Cards Suggested: {len(banks)}\n"
#         analysis += f"- Invalid Cards: {invalid_banks}\n"
#         analysis += f"- APR Mismatches: {apr_mismatches}\n"
#         analysis += f"- Mode Mismatches: {mode_mismatches}\n"
#         analysis += f"- Cards Using Default Values: {default_usage}\n"
#         analysis += f"- Invalid Reasons: {invalid_reasons}\n"

#     logging.info("GPT output validation completed.")
#     return analysis

# # === Core GPT Analysis ===
# def analyze_credit_report(text, bank_df=None, mode="free", user_state=None):
#     language = "Spanish" if is_spanish(text) else "English"
#     bank_data_str = ""
#     state_bank_suggestion = get_state_funding_banks(user_state) if user_state else []
#     enrichment_context = get_enrichment()

#     # Print state_bank_suggestion for verification
#     print(f"State-specific bank list for {user_state}: {state_bank_suggestion}")

#     # Prepare bank data for paid mode
#     if bank_df is not None and mode == "paid":
#         bank_data_str += "\n\nApproved Bank List (for reference only, do NOT use for suggestions):\n"
#         for _, row in bank_df.head(10).iterrows():
#             row_str = " | ".join(str(x) for x in row.values if pd.notna(x))
#             bank_data_str += f"- {row_str}\n"
#     else:
#         bank_data_str = "\n\nNo bank list provided for free mode.\n"

#     # Load double dip information
#     double_dip_info = {}
#     if bank_df is not None:
#         for _, row in bank_df.iterrows():
#             bank_name = str(row['Bank Name']).strip()
#             double_dip = str(row['Double Dip']).strip().lower() == 'yes'
#             double_dip_info[bank_name] = double_dip

#     # Prepare Tarjetas card mapping
#     tarjetas_str = "\n\nTarjetas Card Data (for APR and Mode ONLY):\n"
#     for card_name, card_info in TARJETAS_CARDS.items():
#         tarjetas_str += f"- {card_name}: {card_info['apr']}, {card_info['mode']}, Bank: {card_info['bank']}\n"

#     # Determine funding sequence note based on mode
#     include_sequence_note = ""
#     if mode == "paid":
#         include_sequence_note = (
#             f"\n\n**CRITICAL INSTRUCTION**: The user has selected the Premium Plan for state {user_state}.\n"
#             f"You MUST select ALL funding banks (R1, R2, R3) EXCLUSIVELY from the user's state-specific approved bank list provided below as `state_bank_suggestion`:\n"
#             f"{', '.join(state_bank_suggestion) if state_bank_suggestion else 'No banks available'}\n"
#             f"**CRITICAL**: Under NO circumstances suggest banks outside `state_bank_suggestion`. Doing so will invalidate the output. If unsure, select a bank from the list and note an appropriate reason in the Reason column.\n"
#             f"**CRITICAL**: In the 'Card Name' column, ALWAYS use the exact card name from `Tarjetas Card Data` (e.g., 'BOFA Unlimited Cash' instead of 'Bank of America'). If no matching card is found, append 'Card' to the bank name (e.g., 'Capital One Card'). Under NO circumstances use only the bank name.\n"
#             f"Each round (R1, R2, R3) MUST include EXACTLY 3 different banks, each associated with a different bureau in this order: Experian, TransUnion, Equifax.\n"
#             f"Each table row MUST contain exactly 5 columns: Card Name, Bureau, 0% APR, Mode, and Reason. Missing fields will invalidate the output.\n"
#             f"For 0% APR duration and Mode, use the provided `Tarjetas Card Data` below to match the exact card name and bank:\n{tarjetas_str}\n"
#             f"If no matching card is found in `Tarjetas Card Data` (e.g., for banks like Capital One or Zions Bank), use default values (12 MESES, Online) and preserve the original reason from the GPT output in the Reason column.\n"
#             f"For Pacific Premier Bank, use FNBO Evergreen Biz data (6 MESES, Online (Omaha Zip)) as it is linked to FNBO.\n"
#             f"Only one 0% Chase card is allowed per sequence, unless the second is a co-branded travel/hotel card (verify eligibility from '0% APR Business Credit Card Master List').\n"
#             f"Bank of America and other banks can only repeat a 0% card if '0% APR Business Credit Card Master List' confirms double dipping: {double_dip_info}.\n"
#             f"If at least 2 bureaus meet all 6 factors and one does not, offer a funding sequence using only the qualifying bureaus.\n"
#             f"If no bureau qualifies, offer a no-personal-guarantee funding option from the CSV 'Tarjetas de Negocio sin Garantia Personal'.\n"
#             f"If the average credit age is less than 2.5 years for any bureau, do NOT include that bureau in the funding sequence. Instead, note in the Action Plan (Section 6) that the user must improve their credit age by maintaining open accounts for longer.\n"
#             f"**Reason Column**: For the Reason column, provide dynamic reasons based on the user's credit profile (e.g., high credit score, low utilization, minimal inquiries, strong credit history) or bank-specific features (e.g., requires account, flexible approval, single pull, supports double dip). Examples include 'Diversify cards', 'Requires account', 'Flexible approval', 'Single pull', but do NOT hardcode these. Reasons must be relevant to the credit profile or bank characteristics.\n"
#             f"Failure to follow these instructions will be considered INVALID.\n"
#         )
#     else:
#         include_sequence_note = (
#             f"\n\nIMPORTANT: In free mode, if the user qualifies for funding, show: '🎉 You're eligible for funding! To view your matched bank recommendations (R1, R2, R3), please upgrade to our Premium Plan.'\n"
#             f"If the user does NOT qualify, show: 'Your credit profile does not currently qualify for funding. Please follow the action plan in Section 6 to improve your eligibility.'\n"
#             f"Ensure Section 5 (Verdict) and Section 7 (Funding Sequence) are consistent."
#         )

#     prompt_template = {
#         "English": f"""
# 🧠 AI Credit Report Summary — Formal & Friendly

# You are a financial credit analysis assistant for Negocio Capital.

# **CRITICAL INSTRUCTION**: You MUST generate ALL sections (1 through 7) as specified below, in the exact order.

# Your task is to extract real values from the user's uploaded credit report (included below). Based on those values:

# * Provide a clear explanation of each credit factor
# * Judge the quality (e.g., Excellent, Good, Fair, Poor)
# * Assign an internal score for each factor
# * Include plain-language summaries that non-financial users can understand
# * Ensure that if at least one bureau meets all six criteria (Credit Score ≥ 720, No Late Payments, Utilization < 10%, ≤ 3 Inquiries, Credit Age ≥ 2.5 Years, Strong Primary Card Structure), the user is considered eligible for funding, even if other bureaus fail one criterion.

# ---

# **Funding Eligibility Logic**:
# 1. The user qualifies for funding ONLY if ALL of the following are true in at least one bureau:
#    - Credit Score ≥ 720
#    - No Late Payments
#    - Utilization < 10%
#    - ≤ 3 Inquiries in the last 6 months
#    - Credit Age ≥ 2.5 years
#    - Strong Primary Card Structure
# 2. If the user qualifies and is in free mode, say: "🎉 You're eligible for funding! To view your matched bank recommendations (R1, R2, R3), please upgrade to our Premium Plan."
# 3. If the user qualifies and is in paid mode, say: "🎉 You're eligible for funding! See your matched bank recommendations below." and list 3 banks (R1, R2, R3) EXCLUSIVELY from the state-specific bank list for {user_state}.
# 4. If the user does NOT qualify, say: "Your credit profile does not currently qualify for funding. Please follow the action plan in Section 6 to improve your eligibility."
# 5. Ensure the Verdict (Section 5) and Recommended Funding Sequence (Section 7) are consistent. If the user does not qualify in Section 5, Section 7 MUST NOT say they are eligible.

# ---

# 📌 **1. Breakdown by Bureau**

# Generate a table of revolving credit details based on the actual report data. Always extract the data.

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
# - **Cards >= $2K**: Note the number of cards with limits of $2,000 or more . Mention how it supports creditworthiness. End with a label like **Good** or **Needs Improvement**.
# - **Cards >= $5K**: Note the number of cards with limits of $5,000 or more . Mention how it enhances funding readiness. End with a label like **Excellent** or **Fair**.
# - **Score / 144**: Report the total score out of 144 based on the analysis. End with a label like **Excellent** or **Needs Improvement**.

# Each bullet should be brief, clear, and conclude with a bold quality label.

# ---

# ### 📌 2. Revolving Credit Structure

# Always extract the revolving credit details from the report and present them in a structured table. 

# | **Field**                | **Detail**                                  |
# |--------------------------|---------------------------------------------|
# | Open Cards               | [Number of open cards, specify AU/Primary] |
# | Total Limit              | [$Total credit limit']                       |
# | Primary Cards            | [Count or “None”]                           |
# | High-Limit Card Present? | [YES/NO (Mention limit threshold, e.g. $5k+)']|

# Explain each field briefly below the table if needed.

# ---

# 📌 **3. Authorized User (AU) Strategy**

# * How many AU cards are there?
# * What are their limits and ages?
# * Do they help with funding?
# * Recommendation: what AU cards to add or remove.

# ---

# 📌 **4. Funding Readiness by Bureau**

# Ensure all available revolving credit data is extracted from the report and displayed in a table.

# | Criteria                      | Equifax | Experian | TransUnion |
# | ----------------------------- | ------- | -------- | ---------- |
# | Score ≥ 720                   | Yes/No  | Yes/No   | Yes/No    |
# | No Late Payments              | Yes/No  | Yes/No   | Yes/No    |
# | Utilization < 10%             | Yes/No  | Yes/No   | Yes/No    |
# | ≤ 3 Inquiries (last 6 months) | Yes/No  | Yes/No   | Yes/No    |
# | Credit Age ≥ 2.5 Years        | Yes/No  | Yes/No   | Yes/No    |
# | Strong Primary Card Structure | Yes/No  | Yes/No   | Yes/No    |

# ---

# 📌 5. Verdict

# Clearly state if the user qualifies for funding based on the Funding Eligibility Logic above. For paid mode, use: "🎉 You're eligible for funding! See your matched bank recommendations below." For free mode, use: "🎉 You're eligible for funding! To view your matched bank recommendations (R1, R2, R3), please upgrade to our Premium Plan." If not qualified, explain why in 2–3 short bullet points. If data is missing, assume eligibility for paid mode and note: "Assumed eligibility due to missing data."

# ---

# 📌 6. Action Plan

# List 3–5 steps the user should take to improve their credit profile, such as:
# Pay down credit card balances to reduce utilization.
# Add new Authorized User (AU) cards with high limits to strengthen credit.
# Open personal primary cards to build a stronger credit structure.
# Dispute or wait out old late payments to improve credit history.
# If the average credit age is less than 2.5 years for any bureau, include a step to maintain open accounts for longer to improve credit age.
# If data is missing, provide generic advice.

# ---

# 📌 **7. Recommended Funding Sequence ({user_state})**

# * If the user qualifies for funding (based on the Funding Eligibility Logic or assumed due to missing data) and is in **paid mode**, provide the following structured output using ONLY the approved bank list provided in `state_bank_suggestion`. The banks MUST be selected from the "Sheet1" tab of the file "0% Funding Sequence Per State" for the user's selected state ({user_state}). Follow these strict rules:
#   - Each round (R1, R2, R3) MUST include EXACTLY 3 different banks.
#   - Each bank in a round MUST be associated with a different credit bureau in this order: Experian → TransUnion → Equifax.
#   - Banks MUST NOT be suggested from outside the `state_bank_suggestion` list, even if the user has existing relationships with other banks.
#   - **CRITICAL**: Under NO circumstances suggest banks outside `state_bank_suggestion`. Doing so will invalidate the output. If unsure, select a bank from the list and note an appropriate reason in the Reason column.
#   - **CRITICAL**: In the 'Card Name' column, ALWAYS use the exact card name from `Tarjetas Card Data` (e.g., 'BOFA Unlimited Cash' instead of 'Bank of America'). If no matching card is found, append 'Card' to the bank name (e.g., 'Capital One Card'). Under NO circumstances use only the bank name.
#   - Each table row MUST contain exactly 5 columns: Card Name, Bureau, 0% APR, Mode, and Reason. Missing fields will invalidate the output.
#   - Only one 0% Chase card is allowed per sequence, unless the second is a co-branded travel/hotel card (verify eligibility from '0% APR Business Credit Card Master List').
#   - Bank of America and other banks can only repeat a 0% card if the file '0% APR Business Credit Card Master List' confirms double dipping: {double_dip_info}.
#   - If at least 2 bureaus meet all 6 factors and one does not, offer a funding sequence using only the qualifying bureaus.
#   - If no bureau qualifies, offer a no-personal-guarantee funding option from the CSV 'Tarjetas de Negocio sin Garantia Personal'.
#   - If the average credit age is less than 2.5 years for any bureau, do NOT include that bureau in the funding sequence. Instead, note in the Action Plan (Section 6) that the user must improve their credit age by maintaining open accounts for longer.
#   - For 0% APR duration and Mode, use the provided `Tarjetas Card Data` to match the exact card name and bank:\n{tarjetas_str}\n
#   - If no matching card is found in `Tarjetas Card Data` (e.g., for banks like Capital One or Zions Bank), use default values (12 MESES, Online) and preserve the original reason from the GPT output in the Reason column.
#   - For Pacific Premier Bank, use FNBO Evergreen Biz data (6 MESES, Online) as it is linked to FNBO.
#   - **Reason Column**: Provide dynamic reasons based on the user's credit profile (e.g., high credit score, low utilization, minimal inquiries, strong credit history) or bank-specific features (e.g., requires account, flexible approval, single pull, supports double dip). Examples include 'Diversify cards', 'Requires account', 'Flexible approval', 'Single pull', but do NOT hardcode these. Reasons must be relevant to the credit profile or bank characteristics.

#   **ROUND 1**
#   | Card Name          | Bureau   | 0% APR      | Mode         | Reason                  |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | Experian | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | TransUnion | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | Equifax | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |

#   **ROUND 2**
#   | Card Name          | Bureau   | 0% APR      | Mode         | Reason                  |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | Experian | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | TransUnion | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | Equifax | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |

#   **ROUND 3**
#   | Card Name          | Bureau   | 0% APR      | Mode         | Reason                  |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | Experian | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | TransUnion | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | Equifax | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |

#   **Strategic Insights for Execution**
#   - Generate 4–6 tailored bullet points based on the user's credit profile (e.g., credit score, utilization, inquiries, credit age) and the recommended banks from `state_bank_suggestion`. Examples include:
#     - If inquiries are high (e.g., >2), recommend freezing non-used bureaus (specify which ones based on the funding sequence) to preserve credit inquiries.
#     - If utilization is close to 10%, suggest paying down balances before applying to improve approval odds.
#     - If a bank requires in-branch application (check `Tarjetas Card Data`), advise visiting a local branch in {user_state}.
#     - If credit score is exceptionally high (e.g., ≥780), recommend declaring a higher personal income (e.g., $120,000) to qualify for larger credit limits.
#     - If credit age is strong (e.g., ≥5 years), suggest requesting credit limit increases after 60 days for banks that support early increases (e.g., Chase, AMEX).
#     - If business spending data is available, recommend including it to strengthen applications for banks in the sequence.
#   - Ensure each bullet is specific to the user's credit profile or the characteristics of the recommended banks (e.g., application mode, double-dip eligibility).
#   - Do NOT use generic or hardcoded advice. Each point must be relevant and actionable based on the provided data.

#   **You Are Fully Ready to Execute**
#   - Estimate the potential funding amount based on the user's total credit limit (e.g., if total limit is $50,000, estimate 2–3x that amount, or use bureau scores to estimate $50K–$200K range).
#   - Provide 2–3 tailored next steps based on the user's credit profile and state-specific bank recommendations, such as:
#     - Applying to specific banks in the sequence that align with the user's strongest bureau (e.g., Experian if score is highest).
#     - Preparing specific documents (e.g., business spending statements) for banks requiring in-branch applications.
#     - Contacting Negocio Capital for guided execution if the credit profile is complex (e.g., multiple inquiries or marginal utilization).
#   - Include a call-to-action: "Connect with Negocio Capital for guided execution and BRM support. Schedule a call: [Negocio Capital Website]."
#   - Add a disclaimer: "This analysis is provided by Negocio Capital and must not be shared or redistributed. All Rights Reserved © 2025."

# * If the user qualifies for funding and is in **free mode**, say: "🎉 You're eligible for funding! To view your matched bank recommendations (R1, R2, R3), please upgrade to our Premium Plan."
# * If the user does not qualify for funding, say: "Your credit profile does not currently qualify for funding. Please follow the action plan in Section 6 to improve your eligibility."
# * Ensure this section is consistent with Section 5 (Verdict).

# **FINAL INSTRUCTION**: You MUST generate ALL sections (1–7) in the exact order specified above. Populate all sections with available data from the credit report. If specific data (e.g., Utilization, Avg. Credit Age) is missing, use 'Data not available' only after attempting to extract all relevant information. Skipping any section is INVALID. Now analyze the following report and generate the complete structured output:

# {text}
# {enrichment_context}
# State-specific bank list for {user_state}: {', '.join(state_bank_suggestion) if state_bank_suggestion else 'No banks available'}
# {bank_data_str}
# {tarjetas_str}
# {include_sequence_note}
# """,

#         "Spanish": f"""
# 🧠 Resumen del Informe de Crédito — Versión Mejorada

# Eres un asistente financiero de análisis de crédito para Negocio Capital.

# **INSTRUCCIÓN CRÍTICA**: DEBES generar TODAS las secciones (1 a 7) como se especifica a continuación, en el orden exacto, incluso si faltan datos en el informe de crédito. Si algún dato (por ejemplo, puntaje de crédito, utilización, consultas) no está disponible, usa texto de marcador como 'Datos no disponibles' solo como último recurso después de intentar extraer toda la información relevante del informe de crédito proporcionado. Omitir cualquier sección es INVÁLIDO.

# Tu tarea es extraer los valores reales del informes de crédito proporcionado (abajo). Basado en esos valores:

# * Explica cada factor de forma clara y sencilla
# * Evalúa la calidad (Ej: Excelente, Bueno, Regular, Malo)
# * Asigna una puntuación interna
# * Utiliza un lenguaje fácil de entender por usuarios no financieros
# * Asegúrate de que si al menos un buró cumple con los seis criterios (Puntaje de Crédito ≥ 720, Sin Pagos Atrasados, Utilización < 10%, ≤ 3 Consultas, Edad Crediticia ≥ 2.5 Años, Estructura Sólida de Tarjetas Primarias), el usuario se considera elegible para financiamiento, incluso si otros burós fallan en un criterio.

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
# 3. Si el usuario califica y está en modo pago, di: "🎉 ¡Eres elegible para financiamiento! Consulta tus bancos recomendados a continuación." y lista 3 bancos (R1, R2, R3) EXCLUSIVAMENTE de la lista de bancos aprobados específica del estado ({user_state}).
# 4. Si el usuario NO califica, di: "Tu perfil de crédito no califica actualmente para financiamiento. Por favor, sigue el plan de acción en la Sección 6 para mejorar tu elegibilidad."
# 5. Asegúrate de que el Veredicto (Sección 5) y la Secuencia de Financiamiento Recomendada (Sección 7) sean consistentes. Si el usuario no califica en la Sección 5, la Sección 7 NO DEBE decir que es elegible.

# ---

# 📌 **1. Desglose por Buró**

# Genera una tabla como esta basada en los datos reales del informe o 'Datos no disponibles' si la extracción falla:

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

# Después de la tabla, incluye un análisis breve en formato de viñetas (puntos), explicando cada categoría individualmente en lenguaje sencillo y accesible. Usa este formato:

# - **Puntaje de Crédito**: Reporta el puntaje de crédito para cada buró o 'Datos no disponibles'. Menciona si cumple con el umbral de 720. Finaliza con una etiqueta como **Excelente**, **Bueno**, **Regular**, o **Malo**.
# - **Historial Limpio**: Resume si hay pagos atrasados o incumplimientos o 'Datos no disponibles'. Si no hay, di "Sí". Finaliza con una etiqueta como **Excelente** o **Debe Mejorar**.
# - **Utilización**: Indica el porcentaje total de utilización o 'Datos no disponibles'. Explica si está por debajo del 10% y cómo afecta la elegibilidad de financiamiento. Termina con una etiqueta como **Excelente**, **Bueno**, o **Riesgoso**.
# - **Consultas Duras (6 meses)**: Indica cuántas consultas hubo en los últimos 6 meses o 'Datos no disponibles'. Menciona si es aceptable (≤ 3). Finaliza con una etiqueta como **Bueno**, **Regular**, o **Riesgoso**.
# - **Edad Promedio Crédito**: Explica la edad promedio de las cuentas o 'Datos no disponibles'. Di si cumple con el umbral de 2.5 años. Finaliza con una etiqueta como **Excelente** o **Regular**.
# - **Tarjetas >= $2K**: Nota la cantidad de tarjetas con límites de $2,000 o más o 'Datos no disponibles'. Menciona cómo apoya la solvencia crediticia. Finaliza con una etiqueta como **Bueno** o **Debe Mejorar**.
# - **Tarjetas >= $5K**: Nota la cantidad de tarjetas con límites de $5,000 o más o 'Datos no disponibles'. Menciona cómo mejora la preparación para financiamiento. Finaliza con una etiqueta como **Excelente** o **Regular**.
# - **Puntaje / 144**: Reporta el puntaje total de 144 basado en el análisis o 'Datos no disponibles'. Finaliza con una etiqueta como **Excelente** o **Debe Mejorar**.

# Cada viñeta debe ser breve, clara y cerrar con una etiqueta de calidad en **negrita**.

# ---

# ### 📌 2. Estructura de Crédito Revolvente

# Presenta los detalles del crédito revolvente en una tabla como esta (usa 'Datos no disponibles' si la extracción falla):

# | **Campo**                     | **Detalle**                                         |
# |-------------------------------|-----------------------------------------------------|
# | Tarjetas Abiertas             | [Número de tarjetas abiertas, indicar AU/Principal o 'Datos no disponibles'] |
# | Límite Total                  | [$Límite total de crédito o 'Datos no disponibles']                          |
# | Tarjetas Primarias            | [Cantidad o “Ninguna” o 'Datos no disponibles']                              |
# | ¿Tarjetas de Alto Límite?     | [SÍ/NO (Indicar umbral, por ejemplo $5,000+) o 'Datos no disponibles']       |

# Explica brevemente cada campo debajo de la tabla si es necesario.

# ---

# 📌 **3. Estrategia de Usuario Autorizado (AU)**

# * ¿Cuántas tarjetas AU tiene o 'Datos no disponibles'?
# * ¿Sus límites y antigüedad o 'Datos no disponibles'?
# * ¿Ayuda al perfil crediticio?
# * ¿Qué se recomienda añadir o eliminar? (Proporciona consejos genéricos si faltan datos)

# ---

# 📌 **4. Preparación para Financiamiento**

# | Criterio                        | Equifax | Experian | TransUnion |
# | ------------------------------- | ------- | -------- | ---------- |
# | Puntaje ≥ 720                   | Sí/No/Datos no disponibles   | Sí/No/Datos no disponibles    | Sí/No/Datos no disponibles      |
# | Sin pagos atrasados             | Sí/No/Datos no disponibles   | Sí/No/Datos no disponibles    | Sí/No/Datos no disponibles      |
# | Utilización < 10%               | Sí/No/Datos no disponibles   | Sí/No/Datos no disponibles    | Sí/No/Datos no disponibles      |
# | ≤ 3 consultas (últimos 6 meses) | Sí/No/Datos no disponibles   | Sí/No/Datos no disponibles    | Sí/No/Datos no disponibles      |
# | Edad crediticia ≥ 2.5 años      | Sí/No/Datos no disponibles   | Sí/No/Datos no disponibles    | Sí/No/Datos no disponibles      |
# | Buena estructura de tarjetas    | Sí/No/Datos no disponibles   | Sí/No/Datos no disponibles    | Sí/No/Datos no disponibles      |

# ---

# 📌 5. Veredicto

# Indicar claramente si el usuario califica para financiamiento según la Lógica de Elegibilidad para Financiamiento. Para el modo pago, usa: "🎉 ¡Eres elegible para financiamiento! Consulta tus bancos recomendados a continuación." Para el modo gratuito, usa: "🎉 ¡Eres elegible para financiamiento! Para ver tus bancos recomendados (R1, R2, R3), por favor actualiza a nuestro Plan Premium." Si el usuario no califica, proporcionar 2–3 razones breves que expliquen por qué. Si faltan datos, asume elegibilidad para el modo pago y anota: "Elegibilidad asumida debido a datos faltantes."

# ---

# 📌 6. Plan de Acción

# Enumerar 3–5 pasos que el usuario debe tomar para mejorar su perfil crediticio, como:
# Pagar los saldos de las tarjetas de crédito para reducir la utilización.
# Agregar nuevas tarjetas de usuario autorizado (AU) con límites altos para fortalecer el crédito
# Abrir tarjetas primarias personales para construir una estructura crediticia más sólida.
# Disputar o esperar a que prescriban pagos atrasados antiguos para mejorar el historial crediticio.
# Si la edad crediticia promedio es menor a 2.5 años para cualquier buró, incluye un paso para mantener las cuentas abiertas por más tiempo para mejorar la edad crediticia.
# Si faltan datos, proporciona consejos genéricos.

# ---

# 📌 **7. Recomendación de Bancos ({user_state})**

# * Si el usuario califica y está en **modo pago**, proporciona la siguiente salida estructurada usando SÓLO la lista de bancos aprobados en `state_bank_suggestion`. Los bancos DEBEN seleccionarse del "Sheet1" del archivo "0% Funding Sequence Per State" para el estado seleccionado por el usuario ({user_state}). Sigue estas reglas estrictas:
#   - Cada ronda (R1, R2, R3) DEBE incluir EXACTAMENTE 3 bancos diferentes.
#   - Cada banco en una ronda DEBE estar asociado con un buró de crédito diferente en este orden: Experian → TransUnion → Equifax.
#   - Los bancos NO DEBEN sugirirse fuera de la lista `state_bank_suggestion`, incluso si el usuario tiene relaciones existentes con otros bancos.
#   - **CRÍTICO**: Bajo NINGUNA circunstancia sugieras bancos fuera de `state_bank_suggestion`. Hacerlo invalidará la salida. Si no estás seguro, selecciona un banco de la lista y anota una razón relevante en la columna Razón.
#   - **CRÍTICO**: En la columna 'Nombre de la Tarjeta', SIEMPRE usa el nombre exacto de la tarjeta de `Tarjetas Card Data` (por ejemplo, 'BOFA Unlimited Cash' en lugar de 'Bank of America'). Si no se encuentra una tarjeta coincidente, agrega 'Card' al nombre del banco (por ejemplo, 'Capital One Card'). Bajo NINGUNA circunstancia uses solo el nombre del banco.
#   - Cada fila de la tabla DEBE contener exactamente 5 columnas: Nombre de la Tarjeta, Buró, 0% APR, Modo, y Razón. Campos faltantes invalidarán la salida.
#   - Solo se permite una tarjeta Chase al 0% por secuencia, a menos que la segunda sea una tarjeta de viaje/hotel co-brandeada (verifica la elegibilidad en '0% APR Business Credit Card Master List').
#   - Bank of America y otros bancos solo pueden repetir una tarjeta al 0% si el archivo '0% APR Business Credit Card Master List' confirma que permiten "double dipping": {double_dip_info}.
#   - Si al menos 2 burós cumplen con los 6 factores y uno no, ofrece una secuencia de financiamiento usando solo los burós que califican.
#   - Si ningún buró califica, ofrece una opción de financiamiento sin garantía personal del CSV "Tarjetas de Negocio sin Garantia Personal".
#   - Si la edad crediticia promedio es menor a 2.5 años para cualquier buró, NO incluyas ese buró en la secuencia de financiamiento. En su lugar, indica en el Plan de Acción (Sección 6) que el usuario debe mejorar su edad crediticia manteniendo cuentas abiertas por más tiempo.
#   - La selección de bancos DEBE coincidir con el perfil crediticio del usuario (por ejemplo, puntaje de crédito, utilización, historial crediticio) y la secuencia de bancos específica del estado. Si faltan datos, selecciona bancos basados en la lista del estado y anota: "Seleccionado de la lista del estado debido a datos faltantes."
#   - Para la duración del 0% APR y el Modo, usa los datos proporcionados en `Tarjetas Card Data` para coincidir con el nombre exacto de la tarjeta y el banco:\n{tarjetas_str}\n
#   - Si no se encuentra una tarjeta coincidente en `Tarjetas Card Data` (por ejemplo, para bancos como Capital One o Zions Bank), usa valores predeterminados (12 MESES, Online) y anótalo en la columna Razón como 'Valores predeterminados usados debido a datos faltantes en Tarjetas'. Bajo NINGUNA circunstancia uses '0%' como valor de APR.
#   - Para Pacific Premier Bank, usa los datos de FNBO Evergreen Biz (6 MESES, Online (Omaha Zip)) ya que está vinculado a FNBO.
#   - **Columna Razón**: Proporciona razones dinámicas basadas en el perfil crediticio del usuario (por ejemplo, puntaje de crédito alto, utilización baja, consultas mínimas, historial crediticio sólido) o características específicas del banco (por ejemplo, requiere cuenta, aprobación flexible, extracción única, permite double dipping). Ejemplos incluyen 'Diversificar tarjetas', 'Requiere cuenta', 'Aprobación flexible', 'Extracción única', pero NO los codifiques de forma fija. Las razones deben ser relevantes para el perfil crediticio o las características del banco.

#   **RONDA 1**
#   | Nombre de la Tarjeta   | Buró     | 0% APR      | Modo         | Razón                   |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | Experian | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | TransUnion | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | Equifax | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |

#   **RONDA 2**
#   | Nombre de la Tarjeta   | Buró     | 0% APR      | Modo         | Razón                   |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | Experian | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | TransUnion | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | Equifax | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |

#   **RONDA 3**
#   | Nombre de la Tarjeta   | Buró     | 0% APR      | Modo         | Reason                  |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | Experian | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | TransUnion | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | Equifax | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |

#   **Perspectivas Estratégicas para la Ejecución**
#   - Genera 4–6 puntos personalizados basados en el perfil crediticio del usuario (por ejemplo, puntaje de crédito, utilización, consultas, edad crediticia) y los bancos recomendados de `state_bank_suggestion`. Ejemplos incluyen:
#     - Si las consultas son altas (por ejemplo, >2), recomienda congelar los burós no utilizados (especifica cuáles según la secuencia de financiamiento) para preservar las consultas.
#     - Si la utilización está cerca del 10%, sugiere pagar los saldos antes de solicitar para mejorar las probabilidades de aprobación.
#     - Si un banco requiere solicitud en sucursal (verifica `Tarjetas Card Data`), aconseja visitar una sucursal local en {user_state}.
#     - Si el puntaje de crédito es excepcionalmente alto (por ejemplo, ≥780), recomienda declarar un ingreso personal más alto (por ejemplo, $120,000) para calificar para límites de crédito más grandes.
#     - Si la edad crediticia es sólida (por ejemplo, ≥5 años), sugiere solicitar aumentos de límite después de 60 días para bancos que permitan aumentos tempranos (por ejemplo, Chase, AMEX).
#     - Si hay datos de gastos comerciales disponibles, recomienda incluirlos para fortalecer las solicitudes para los bancos en la secuencia.
#   - Asegúrate de que cada punto sea específico al perfil crediticio del usuario o a las características de los bancos recomendados (por ejemplo, modo de solicitud, elegibilidad para double dipping).
#   - NO uses consejos genéricos o codificados. Cada punto debe ser relevante y accionable basado en los datos proporcionados.

#   **Estás Completamente Listo para Ejecutar**
#   - Estima la cantidad potencial de financiamiento basada en el límite total de crédito del usuario (por ejemplo, si el límite total es $50,000, estima 2–3 veces esa cantidad, o usa los puntajes de los burós para estimar un rango de $50K–$200K).
#   - Proporciona 2–3 pasos siguientes personalizados basados en el perfil crediticio del usuario y las recomendaciones de bancos específicas del estado, como:
#     - Solicitar a bancos específicos en la secuencia que se alineen con el buró más fuerte del usuario (por ejemplo, Experian si el puntaje es el más alto).
#     - Preparar documentos específicos (por ejemplo, estados de gastos comerciales) para bancos que requieran solicitudes en sucursal.
#     - Contactar a Negocio Capital para una ejecución guiada si el perfil crediticio es complejo (por ejemplo, múltiples consultas o utilización marginal).
#   - Incluye una llamada a la acción: "Conecta con Negocio Capital para una ejecución guiada y soporte BRM. Agenda una llamada: [Negocio Capital Website]."
#   - Agrega un descargo de responsabilidad: "Este análisis es proporcionado por Negocio Capital y no debe compartirse ni redistribuirse. Todos los derechos reservados © 2025."
#   - Proporciona un marcador para el informe en PDF: "Descarga el informe en PDF con el logo: [file-Qn75Jt2kS9XtYnggLMzajL]."

# * Si el usuario califica y está en **modo gratuito**, di: "🎉 ¡Eres elegible para financiamiento! Para ver tus bancos recomendados (R1, R2, R3), por favor actualiza a nuestro Plan Premium."
# * Si el usuario NO califica, di: "Tu perfil de crédito no califica actualmente para financiamiento. Por favor, sigue el plan de acción en la Sección 6 para mejorar tu elegibilidad."
# * Asegúrate de que esta sección sea consistente con la Sección 5 (Veredicto).

# **INSTRUCCIÓN FINAL**: DEBES generar TODAS las secciones (1–7) en el orden exacto especificado arriba. Rellena todas las secciones con los datos disponibles del informe de crédito. Si faltan datos específicos (por ejemplo, Utilización, Edad Promedio del Crédito), usa 'Datos no disponibles' solo después de intentar extraer toda la información relevante. Omitir cualquier sección es INVÁLIDO. Ahora analiza el siguiente informe y genera la salida estructurada completa:

# {text}
# {enrichment_context}
# Lista de bancos específicos del estado ({user_state}): {', '.join(state_bank_suggestion) if state_bank_suggestion else 'No banks available'}
# {bank_data_str}
# {tarjetas_str}
# {include_sequence_note}
# """
#     }

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a strict, accurate AI financial credit analyst from Negocio Capital. You must extract all data exactly as available in the text. Do NOT hallucinate. Do NOT say 'Data not available'. Always follow instructions strictly. Be formal and expert in tone."},
#                 {"role": "user", "content": prompt_template[language]}
#             ],
#             max_tokens=3900,
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
#         analysis = validate_gpt_output(analysis, state_bank_suggestion, user_state, mode)
#         return analysis
#     except Exception as lỗi:
#         logging.error(f"GPT-4 error: {str(lỗi)}")
#         print(f"❌ GPT-4 error: {str(lỗi)}")
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
#     except Exception as lỗi:
#         logging.error(f"Error saving PDF: {str(lỗi)}")
#         print(f"❌ Error saving PDF: {str(lỗi)}")

# # === Main CLI ===
# def main():
#     print("📂 Welcome to Funding NC AI Credit Report Analyzer!")
#     # Update TARJETAS_CARDS from PDF
#     update_tarjetas_from_pdf(TARJETAS_PATH)
#     file_path = input("📄 Enter path to your credit report PDF (e.g., uploads/client1.pdf): ").strip()
#     if not os.path.exists(file_path):
#         print("❌ File not found. Please check the path and try again.")
#         logging.error(f"Credit report file not found: {file_path}")
#         return

#     state = input("🌎 Enter the U.S. state your business is registered in (e.g., FL): ").strip()
#     print("📁 Extracting text from PDF...")
#     print("📑 Loading bank list...")
#     bank_df = load_bank_data()
#     mode = input("🧾 Select mode (free/paid): ").strip().lower()
#     if mode not in ["free", "paid"]:
#         print("❌ Invalid mode. Please enter 'free' or 'paid'.")
#         logging.error(f"Invalid mode selected: {mode}")
#         return

#     print("\n🧠 AI Analysis Summary:\n")
#     credit_text = extract_text_from_pdf(file_path)
#     if not credit_text:
#         print("❌ Failed to extract text from PDF.")
#         return
#     analysis = analyze_credit_report(credit_text, bank_df=bank_df, mode=mode, user_state=state)
#     if not analysis:
#         print("❌ GPT analysis failed.")
#         return
#     save_analysis_to_pdf(analysis)
#     print("✅ Analysis complete. Check the output PDF for details.")


# if __name__ == "__main__":
#     main()





















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
# STATE_SEQUENCE_PATH = "data/0% Funding Sequence Per State.xlsx"
# TARJETAS_PATH = "data/Tarjetas de crédito de negocio con garantía personal 2025.pdf"
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

# # === Tarjetas Data ===
# TARJETAS_CARDS = {
#     "Chase Ink Unlimited": {"apr": "12 MESES", "mode": "Online", "bank": "Chase"},
#     "Chase Ink Cash": {"apr": "12 MESES", "mode": "Online", "bank": "Chase"},
#     "BOFA Unlimited Cash": {"apr": "9 MESES", "mode": "Online", "bank": "Bank of America"},
#     "BOFA Cash Rewards": {"apr": "9 MESES", "mode": "Online", "bank": "Bank of America"},
#     "BOFA Travel Rewards": {"apr": "9 MESES", "mode": "Online", "bank": "Bank of America"},
#     "BOFA Platinum Plus": {"apr": "9 MESES", "mode": "Online", "bank": "Bank of America"},
#     "PNC Visa Business": {"apr": "12 MESES", "mode": "Online (requires account)", "bank": "PNC"},
#     "US Bank Triple Cash": {"apr": "12 MESES", "mode": "Online", "bank": "US Bank"},
#     "US Bank Business Leverage": {"apr": "12 MESES", "mode": "Online", "bank": "US Bank"},
#     "US Bank Business Platinum": {"apr": "18 MESES", "mode": "Online", "bank": "US Bank"},
#     "Amex Business Gold": {"apr": "6 MESES", "mode": "Online", "bank": "American Express"},
#     "Amex Blue Biz Cash": {"apr": "12 MESES", "mode": "Online", "bank": "American Express"},
#     "Amex Blue Biz Plus": {"apr": "12 MESES", "mode": "Online", "bank": "American Express"},
#     "Wells Fargo Unlimited 2%": {"apr": "12 MESES", "mode": "Online", "bank": "Wells Fargo"},
#     "Citizens Biz Platinum": {"apr": "12 MESES", "mode": "In-branch/Phone", "bank": "Citizens Bank"},
#     "FNBO Evergreen Biz": {"apr": "6 MESES", "mode": "Online (Omaha Zip)", "bank": "FNBO"},
#     "BMO Business Platinum Rewards": {"apr": "9 MESES", "mode": "In-branch", "bank": "BMO Harris"},
#     "BMO Business Platinum": {"apr": "12 MESES", "mode": "In-branch", "bank": "BMO Harris"},
#     "Truist Business Cash": {"apr": "9 MESES", "mode": "Online", "bank": "Truist"},
#     "Truist Business Card": {"apr": "12 MESES", "mode": "Online", "bank": "Truist"},
#     "KeyBank Business Card": {"apr": "6 MESES", "mode": "Phone/In-branch", "bank": "KeyBank"},
#     "KeyBank Business Rewards": {"apr": "6 MESES", "mode": "Phone/In-branch", "bank": "KeyBank"},
#     "KeyBank Business Cash": {"apr": "6 MESES", "mode": "Phone/In-branch", "bank": "KeyBank"},
#     "M&T Bank Business Card": {"apr": "12 MESES", "mode": "Online", "bank": "M&T Bank"},
#     "Valley National Card": {"apr": "12 MESES", "mode": "Online", "bank": "Valley National"}
# }

# # Add logging setup
# logging.basicConfig(level=logging.DEBUG)

# # Function to extract text from PDF
# def extract_text_from_pdf(pdf_path):
#     try:
#         text = ""
#         with fitz.open(pdf_path) as doc:
#             for page in doc:
#                 text += page.get_text()
#         logging.info(f"Successfully extracted text from PDF: {pdf_path}")
#         logging.debug(f"Extracted text snippet: {text[:500]}...")  # Log the first 500 chars to see the output
#         return text
#     except Exception as e:
#         logging.error(f"Error extracting PDF text from {pdf_path}: {str(e)}")
#         return None

# # Function to extract Credit Score and Utilization
# def extract_credit_info(text):
#     # Credit Score Regex
#     score_pattern = r"Credit Score\s*[:\-]?\s*(\d{3,4})"
#     score_matches = re.findall(score_pattern, text)
#     score = score_matches[0] if score_matches else "Data not available"
    
#     # Utilization Regex
#     utilization_pattern = r"Utilization\s*[:\-]?\s*(\d{1,3}%?)"
#     utilization_matches = re.findall(utilization_pattern, text)
#     utilization = utilization_matches[0] if utilization_matches else "Data not available"
    
#     return score, utilization

# def extract_text_from_docx(docx_path):
#     try:
#         doc = Document(docx_path)
#         text = "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])
#         logging.info(f"Successfully extracted text from DOCX: {docx_path}")
#         return text
#     except Exception as lỗi:
#         logging.error(f"Error extracting DOCX text from {docx_path}: {str(lỗi)}")
#         return None

# def extract_text_from_csv(csv_path):
#     try:
#         df = pd.read_csv(csv_path)
#         text = df.to_string(index=False)
#         logging.info(f"Successfully extracted text from CSV: {csv_path}")
#         return text
#     except Exception as lỗi:
#         logging.error(f"Error extracting CSV text from {csv_path}: {str(lỗi)}")
#         return None

# # === Update TARJETAS_CARDS from PDF ===
# def update_tarjetas_from_pdf(pdf_path):
#     try:
#         text = extract_text_from_pdf(pdf_path)
#         if not text:
#             logging.error("Failed to extract text from Tarjetas PDF")
#             return

#         # Assuming PDF format: "Card Name: BOFA Unlimited Cash, Bank: Bank of America, APR: 9 MESES"
#         # Adjust the regex based on the actual PDF format
#         pattern = r"Card Name: (.*?),\s*Bank: (.*?),\s*APR: (\d+ MESES)"
#         matches = re.findall(pattern, text, re.MULTILINE)
        
#         for card_name, bank, apr in matches:
#             TARJETAS_CARDS[card_name.strip()] = {
#                 "apr": apr.strip(),
#                 "mode": "Online",  # Default mode, update if PDF provides mode
#                 "bank": bank.strip()
#             }
#             logging.info(f"Added card from PDF: {card_name}, Bank: {bank}, APR: {apr}")
#         print(f"✅ Updated TARJETAS_CARDS with {len(matches)} new cards from PDF")
#     except Exception as lỗi:
#         logging.error(f"Error updating TARJETAS_CARDS from PDF: {str(lỗi)}")
#         print(f"❌ Error updating TARJETAS_CARDS: {str(lỗi)}")

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
#     except Exception as lỗi:
#         logging.error(f"Failed to load bank list: {str(lỗi)}")
#         print(f"❌ Failed to load bank list: {str(lỗi)}")
#         return None

# def get_state_funding_banks(user_state):
#     try:
#         df = pd.read_excel(STATE_SEQUENCE_PATH, sheet_name="Sheet1")
#         df.columns = df.columns.str.strip()
#         logging.info(f"State sequence file columns: {list(df.columns)}")
#         logging.info(f"First few rows of state sequence file:\n{df.head().to_string()}")

#         if 'STATE' not in df.columns:
#             logging.error("No 'STATE' column found in state sequence file")
#             return None

#         matched = df[df['STATE'].str.lower() == user_state.lower()]
#         if matched.empty:
#             logging.error(f"No state-specific banks found for {user_state}")
#             return None

#         banks = matched.iloc[0, 1:].dropna().tolist()
#         if not banks:
#             logging.error(f"No banks listed for {user_state} after dropping NA")
#             return None

#         cleaned_banks = []
#         for bank in banks:
#             bank_str = str(bank).strip()
#             if bank_str and not bank_str.isspace() and not bank_str.lower() == 'nan':
#                 cleaned_banks.append(bank_str)

#         logging.info(f"Found {len(cleaned_banks)} banks for state {user_state}: {cleaned_banks}")
#         print(f"✅ Found {len(cleaned_banks)} banks for state {user_state}: {cleaned_banks}")
#         return cleaned_banks
#     except Exception as lỗi:
#         logging.error(f"Could not load state funding data: {str(lỗi)}")
#         print(f"❌ Could not load state funding data: {str(lỗi)}")
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
#             except Exception as lỗi:
#                 enrichment += f"\n[Error reading {file}]: {str(lỗi)}\n"
#                 logging.error(f"Error reading enrichment file {file}: {str(lỗi)}")
#         else:
#             enrichment += f"\n[Skipped missing file: {file}]\n"
#             logging.warning(f"Skipped missing enrichment file: {file}")
#     return enrichment

# # === Output Validation ===
# def validate_gpt_output(analysis, state_bank_suggestion, user_state, mode="free"):
#     analysis_lower = analysis.lower()
#     not_qualified = "does not qualify for funding" in analysis_lower
#     eligible_message = "you are eligible for funding" in analysis_lower

#     # Check for missing sections
#     required_sections = [
#         r"📌.*Breakdown by Bureau",
#         r"📌.*Revolving Credit Structure",
#         r"📌.*Authorized User.*Strategy",
#         r"📌.*Funding Readiness by Bureau",
#         r"📌.*Verdict",
#         r"📌.*Action Plan",
#         r"📌.*Recommended Funding Sequence"
#     ]
#     missing_sections = [sec for sec in required_sections if not re.search(sec, analysis, re.IGNORECASE)]
#     if missing_sections:
#         missing_names = [re.search(r"\.\*(.*?)(?=\||\Z)", sec).group(1).strip() for sec in missing_sections]
#         logging.error(f"Missing sections in GPT output: {missing_names}")
#         error_note = f"\n\n⚠️ ERROR: Missing sections in analysis: {', '.join(missing_names)}. Please check the credit report data or API response."
#         logging.debug(f"Before adding missing sections note: {analysis[:500]}...")
#         analysis += error_note
#         logging.debug(f"After adding missing sections note: {analysis[:500]}...")

#     # Fix inconsistent verdict in free mode
#     if mode == "free" and eligible_message and not_qualified:
#         logging.warning("Inconsistent GPT output in free mode: Eligible in Section 5 but not qualified in Section 7.")
#         print("❌ Fixing inconsistent GPT output in free mode.")
#         analysis = re.sub(
#             r"Your credit profile does not currently qualify for funding.*?(?=\*\*Strategic Insights|\Z)",
#             "🎉 You're eligible for funding! To view your matched bank recommendations (R1, R2, R3), please upgrade to our Premium Plan.",
#             analysis,
#             flags=re.DOTALL
#         )
#         logging.info("Fixed inconsistent verdict in free mode.")

#     # Fix inconsistent verdict in paid mode
#     if mode == "paid" and not_qualified and eligible_message:
#         logging.warning("Inconsistent GPT output: Verdict says not qualified, but Funding Sequence says eligible.")
#         print("❌ Fixing inconsistent GPT output.")
#         analysis = re.sub(
#             r"🎉 You are eligible for funding!.*?(?=\*\*Strategic Insights|\Z)",
#             "Your credit profile does not currently qualify for funding. Please follow the action plan in Section 6 to improve your eligibility.",
#             analysis,
#             flags=re.DOTALL
#         )
#         logging.info("Fixed inconsistent verdict in paid mode.")

#     # Fix incorrect verdict message for paid mode
#     if mode == "paid" and "please upgrade to our Premium Plan" in analysis_lower:
#         logging.error("Incorrect verdict message for paid mode")
#         analysis = re.sub(
#             r"🎉 You're eligible for funding! To view your matched bank recommendations.*?Plan\.",
#             "🎉 You're eligible for funding! See your matched bank recommendations below.",
#             analysis
#         )
#         logging.info("Fixed incorrect verdict message for paid mode.")

#     # Validate Section 7 for three different banks and bureaus per round
#     rounds = re.findall(r"\*\*ROUND [1-3]\*\*(.*?)(?=\*\*ROUND|\*\*Strategic Insights|\Z)", analysis, re.DOTALL)
#     valid_modes = ["Online", "In-branch", "Phone", "Online (requires account)", "Online (Omaha Zip)", "Phone/In-branch"]
#     for i, round_content in enumerate(rounds, 1):
#         # Robust parsing for table rows
#         rows = re.findall(r"\|\s*([^\|]+?)\s*\|\s*(Experian|TransUnion|Equifax)\s*\|\s*([0-9]+ MESES|Default [0-9]+ MESES|0%)?\s*\|\s*([^\|]*?)\s*\|\s*([^\|]*?)\s*\|", round_content)
#         bureaus = []
#         banks = []
#         invalid_banks = []
#         apr_mismatches = []
#         mode_mismatches = []
#         default_usage = []
#         invalid_reasons = []

#         for row in rows:
#             card_name, bureau, apr, mode, reason = row
#             card_name_clean = card_name.strip()
#             bureau = bureau.strip()
#             apr = apr.strip() if apr else "12 MESES"  # Default APR
#             mode = mode.strip() if mode else "Online"  # Default Mode
#             reason = reason.strip()
#             bureaus.append(bureau)
#             banks.append(card_name_clean)

#             # Validate card against state_bank_suggestion
#             matched = False
#             card_bank = None
#             for card, card_info in TARJETAS_CARDS.items():
#                 if card.lower() in card_name_clean.lower():
#                     card_bank = card_info['bank']
#                     matched = any(card_bank.lower() in approved_bank.lower() or approved_bank.lower() in card_bank.lower() for approved_bank in state_bank_suggestion)
#                     break
#             if not matched:
#                 invalid_banks.append(card_name_clean)
#                 logging.error(f"Card {card_name_clean} in Round {i} is not in state_bank_suggestion for {user_state}: {state_bank_suggestion}")
#                 error_note = f"\n\n⚠️ ERROR: Card {card_name_clean} in Round {i} is not in the approved bank list for {user_state}. Replacing with a valid card."
#                 if error_note not in analysis:
#                     analysis += error_note
#                 # Replace invalid card with a valid one from state_bank_suggestion
#                 replacement_bank = next((b for b in state_bank_suggestion if b not in [TARJETAS_CARDS.get(c, {}).get('bank', '') for c in banks]), state_bank_suggestion[0])
#                 replacement_card = None
#                 for card, card_info in TARJETAS_CARDS.items():
#                     if replacement_bank.lower() in card_info['bank'].lower():
#                         replacement_card = card
#                         break
#                 if replacement_card:
#                     replacement_apr = TARJETAS_CARDS[replacement_card]['apr']
#                     replacement_mode = TARJETAS_CARDS[replacement_card]['mode']
#                     replacement_reason = "Strong credit history"
#                 else:
#                     replacement_card = f"{replacement_bank} Card"
#                     replacement_apr = "12 MESES"
#                     replacement_mode = "Online"
#                     replacement_reason = f"Default card for {replacement_bank}"
#                 analysis = re.sub(
#                     r"\|\s*" + re.escape(card_name_clean) + r"\s*\|\s*" + bureau + r"\s*\|\s*[^\|]*?\s*\|\s*[^\|]*?\s*\|\s*[^\|]*?\s*\|",
#                     f"| {replacement_card} | {bureau} | {replacement_apr} | {replacement_mode} | {replacement_reason} |",
#                     analysis
#                 )

#             # Validate APR and Mode against Tarjetas data
#             tarjeta_match = None
#             for card, card_info in TARJETAS_CARDS.items():
#                 if card.lower() in card_name_clean.lower():
#                     tarjeta_match = card_info
#                     break
#             if tarjeta_match:
#                 expected_apr = tarjeta_match['apr']
#                 expected_mode = tarjeta_match['mode'].split(' (')[0]  # Remove notes like '(Omaha Zip)'
#                 if apr != expected_apr:
#                     apr_mismatches.append((card_name_clean, expected_apr, apr))
#                     logging.error(f"APR mismatch for {card_name_clean} in Round {i}: Expected {expected_apr}, Got {apr}")
#                     error_note = f"\n\n⚠️ ERROR: APR for {card_name_clean} in Round {i} is incorrect. Expected {expected_apr}, Got {apr}."
#                     if error_note not in analysis:
#                         analysis += error_note
#                     analysis = re.sub(
#                         r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|).*?(\|.*?\|).*?(\|)",
#                         f"|\1{bureau}|{expected_apr}|{mode}|{reason}|",
#                         analysis
#                     )
#                 if mode.lower() != expected_mode.lower():
#                     mode_mismatches.append((card_name_clean, expected_mode, mode))
#                     logging.error(f"Mode mismatch for {card_name_clean} in Round {i}: Expected {expected_mode}, Got {mode}")
#                     error_note = f"\n\n⚠️ ERROR: Mode for {card_name_clean} in Round {i} is incorrect. Expected {expected_mode}, Got {mode}."
#                     if error_note not in analysis:
#                         analysis += error_note
#                     analysis = re.sub(
#                         r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|.*?\|).*?(\|.*?\|)",
#                         f"|\1{bureau}|{apr}|{expected_mode}|{reason}|",
#                         analysis
#                     )
#             else:
#                 # Handle non-listed cards
#                 if card_name_clean.lower() == "pacific premier bank":
#                     replacement_apr = "6 MESES"
#                     replacement_mode = "Online (Omaha Zip)"
#                     replacement_reason = reason
#                 else:
#                     replacement_apr = "12 MESES"
#                     replacement_mode = "Online"
#                     replacement_reason = f"Default card for {card_name_clean}"
#                 default_usage.append(card_name_clean)
#                 logging.warning(f"No Tarjetas data found for {card_name_clean} in Round {i}. Using default APR: {replacement_apr}, Mode: {replacement_mode}")
#                 analysis = re.sub(
#                     r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|).*?(\|.*?\|).*?(\|)",
#                     f"|\1{bureau}|{replacement_apr}|{replacement_mode}|{replacement_reason}|",
#                     analysis
#                 )
#                 # Ensure card name for non-listed banks
#                 if not any(card.lower() in card_name_clean.lower() for card in TARJETAS_CARDS):
#                     new_card_name = f"{card_name_clean} Card"
#                     analysis = re.sub(
#                         r"\|\s*" + re.escape(card_name_clean) + r"\s*\|\s*" + bureau,
#                         f"| {new_card_name} | {bureau}",
#                         analysis
#                     )

#             # Fix invalid APR values (e.g., "0%")
#             if apr == "0%":
#                 logging.error(f"Invalid APR '0%' for {card_name_clean} in Round {i}. Replacing with default '12 MESES'.")
#                 error_note = f"\n\n⚠️ ERROR: Invalid APR '0%' for {card_name_clean} in Round {i}. Replaced with '12 MESES'."
#                 if error_note not in analysis:
#                     analysis += error_note
#                 analysis = re.sub(
#                     r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|).*?(\|.*?\|).*?(\|)",
#                     f"|\1{bureau}|12 MESES|{mode}|{reason}|",
#                     analysis
#                 )

#             # Fix invalid Mode values
#             if mode not in valid_modes:
#                 logging.error(f"Invalid mode '{mode}' for {card_name_clean} in Round {i}. Replacing with 'Online'.")
#                 error_note = f"\n\n⚠️ ERROR: Invalid mode '{mode}' for {card_name_clean} in Round {i}. Replaced with 'Online'."
#                 if error_note not in analysis:
#                     analysis += error_note
#                 analysis = re.sub(
#                     r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|.*?\|).*?(\|.*?\|)",
#                     f"|\1{bureau}|{apr}|Online|{reason}|",
#                     analysis
#                 )

#             # Validate Reason column
#             valid_reasons = [
#                 r"diversify cards",
#                 r"requires account",
#                 r"flexible approval",
#                 r"single pull",
#                 r"high credit score",
#                 r"low utilization",
#                 r"minimal inquiries",
#                 r"strong credit history",
#                 r"supports double dip",
#                 r"strong primary card structure, excellent credit management"
#             ]
#             reason_valid = any(re.search(pattern, reason.lower()) for pattern in valid_reasons)
#             if not reason_valid or "missing credit data" in reason.lower():
#                 invalid_reasons.append((card_name_clean, reason))
#                 logging.warning(f"Invalid or undesired reason for {card_name_clean} in Round {i}: {reason}")
#                 error_note = f"\n\n⚠️ WARNING: Invalid or undesired reason for {card_name_clean} in Round {i}: '{reason}'. Replacing with a dynamic reason."
#                 if error_note not in analysis:
#                     analysis += error_note
#                 replacement_reason = "Diversify cards"
#                 if "requires account" in mode.lower():
#                     replacement_reason = "Requires account"
#                 elif "in-branch" in mode.lower():
#                     replacement_reason = "Flexible approval"
#                 elif "online" in mode.lower():
#                     replacement_reason = "Single pull"
#                 elif "high credit score" in analysis_lower:
#                     replacement_reason = "High credit score"
#                 elif "low utilization" in analysis_lower:
#                     replacement_reason = "Low utilization"
#                 elif "minimal inquiries" in analysis_lower:
#                     replacement_reason = "Minimal inquiries"
#                 else:
#                     replacement_reason = "Strong credit history"
#                 analysis = re.sub(
#                     r"\|(\s*" + re.escape(card_name_clean) + r"\s*\|.*?\|.*?\|.*?\|).*?(\|)",
#                     f"|\1{bureau}|{apr}|{mode}|{replacement_reason}|",
#                     analysis
#                 )

#         # Check bureau variety
#         if len(set(bureaus)) != 3 or bureaus != ['Experian', 'TransUnion', 'Equifax']:
#             logging.warning(f"Invalid bureau variety in Round {i}: {bureaus}")
#             error_note = f"\n\n⚠️ WARNING: Round {i} does not contain exactly one of each bureau (Experian, TransUnion, Equifax) in order."
#             if error_note not in analysis:
#                 analysis += error_note

#         # Check bank variety
#         if len(set(banks)) != 3 or len(banks) != 3:
#             logging.warning(f"Invalid bank variety in Round {i}: {banks}")
#             error_note = f"\n\n⚠️ WARNING: Round {i} does not contain exactly three different banks."
#             if error_note not in analysis:
#                 analysis += error_note

#         # Log banks and bureaus for this round
#         logging.info(f"Round {i} Cards: {banks}, Bureaus: {bureaus}")

#         # Validation summary
#         analysis += f"\n\n📋 Round {i} Validation Summary:\n"
#         analysis += f"- Total Cards Suggested: {len(banks)}\n"
#         analysis += f"- Invalid Cards: {invalid_banks}\n"
#         analysis += f"- APR Mismatches: {apr_mismatches}\n"
#         analysis += f"- Mode Mismatches: {mode_mismatches}\n"
#         analysis += f"- Cards Using Default Values: {default_usage}\n"
#         analysis += f"- Invalid Reasons: {invalid_reasons}\n"

#     logging.info("GPT output validation completed.")
#     return analysis

# # === Core GPT Analysis ===
# def analyze_credit_report(text, bank_df=None, mode="free", user_state=None):
#     language = "Spanish" if is_spanish(text) else "English"
#     bank_data_str = ""
#     state_bank_suggestion = get_state_funding_banks(user_state) if user_state else []
#     enrichment_context = get_enrichment()

#     # Print state_bank_suggestion for verification
#     print(f"State-specific bank list for {user_state}: {state_bank_suggestion}")

#     # Prepare bank data for paid mode
#     if bank_df is not None and mode == "paid":
#         bank_data_str += "\n\nApproved Bank List (for reference only, do NOT use for suggestions):\n"
#         for _, row in bank_df.head(10).iterrows():
#             row_str = " | ".join(str(x) for x in row.values if pd.notna(x))
#             bank_data_str += f"- {row_str}\n"
#     else:
#         bank_data_str = "\n\nNo bank list provided for free mode.\n"

#     # Load double dip information
#     double_dip_info = {}
#     if bank_df is not None:
#         for _, row in bank_df.iterrows():
#             bank_name = str(row['Bank Name']).strip()
#             double_dip = str(row['Double Dip']).strip().lower() == 'yes'
#             double_dip_info[bank_name] = double_dip

#     # Prepare Tarjetas card mapping
#     tarjetas_str = "\n\nTarjetas Card Data (for APR and Mode ONLY):\n"
#     for card_name, card_info in TARJETAS_CARDS.items():
#         tarjetas_str += f"- {card_name}: {card_info['apr']}, {card_info['mode']}, Bank: {card_info['bank']}\n"

#     # Determine funding sequence note based on mode
#     include_sequence_note = ""
#     if mode == "paid":
#         include_sequence_note = (
#             f"\n\n**CRITICAL INSTRUCTION**: The user has selected the Premium Plan for state {user_state}.\n"
#             f"You MUST select ALL funding banks (R1, R2, R3) EXCLUSIVELY from the user's state-specific approved bank list provided below as `state_bank_suggestion`:\n"
#             f"{', '.join(state_bank_suggestion) if state_bank_suggestion else 'No banks available'}\n"
#             f"**CRITICAL**: Under NO circumstances suggest banks outside `state_bank_suggestion`. Doing so will invalidate the output. If unsure, select a bank from the list and note an appropriate reason in the Reason column.\n"
#             f"**CRITICAL**: In the 'Card Name' column, ALWAYS use the exact card name from `Tarjetas Card Data` (e.g., 'BOFA Unlimited Cash' instead of 'Bank of America'). If no matching card is found, append 'Card' to the bank name (e.g., 'Capital One Card'). Under NO circumstances use only the bank name.\n"
#             f"Each round (R1, R2, R3) MUST include EXACTLY 3 different banks, each associated with a different bureau in this order: Experian, TransUnion, Equifax.\n"
#             f"Each table row MUST contain exactly 5 columns: Card Name, Bureau, 0% APR, Mode, and Reason. Missing fields will invalidate the output.\n"
#             f"For 0% APR duration and Mode, use the provided `Tarjetas Card Data` below to match the exact card name and bank:\n{tarjetas_str}\n"
#             f"If no matching card is found in `Tarjetas Card Data` (e.g., for banks like Capital One or Zions Bank), use default values (12 MESES, Online) and preserve the original reason from the GPT output in the Reason column.\n"
#             f"For Pacific Premier Bank, use FNBO Evergreen Biz data (6 MESES, Online (Omaha Zip)) as it is linked to FNBO.\n"
#             f"Only one 0% Chase card is allowed per sequence, unless the second is a co-branded travel/hotel card (verify eligibility from '0% APR Business Credit Card Master List').\n"
#             f"Bank of America and other banks can only repeat a 0% card if '0% APR Business Credit Card Master List' confirms double dipping: {double_dip_info}.\n"
#             f"If at least 2 bureaus meet all 6 factors and one does not, offer a funding sequence using only the qualifying bureaus.\n"
#             f"If no bureau qualifies, offer a no-personal-guarantee funding option from the CSV 'Tarjetas de Negocio sin Garantia Personal'.\n"
#             f"If the average credit age is less than 2.5 years for any bureau, do NOT include that bureau in the funding sequence. Instead, note in the Action Plan (Section 6) that the user must improve their credit age by maintaining open accounts for longer.\n"
#             f"**Reason Column**: For the Reason column, provide dynamic reasons based on the user's credit profile (e.g., high credit score, low utilization, minimal inquiries, strong credit history) or bank-specific features (e.g., requires account, flexible approval, single pull, supports double dip). Examples include 'Diversify cards', 'Requires account', 'Flexible approval', 'Single pull', but do NOT hardcode these. Reasons must be relevant to the credit profile or bank characteristics.\n"
#             f"Failure to follow these instructions will be considered INVALID.\n"
#         )
#     else:
#         include_sequence_note = (
#             f"\n\nIMPORTANT: In free mode, if the user qualifies for funding, show: '🎉 You're eligible for funding! To view your matched bank recommendations (R1, R2, R3), please upgrade to our Premium Plan.'\n"
#             f"If the user does NOT qualify, show: 'Your credit profile does not currently qualify for funding. Please follow the action plan in Section 6 to improve your eligibility.'\n"
#             f"Ensure Section 5 (Verdict) and Section 7 (Funding Sequence) are consistent."
#         )

#     prompt_template = {
#         "English": f"""
# 🧠 AI Credit Report Summary — Formal & Friendly

# You are a financial credit analysis assistant for Negocio Capital.

# **CRITICAL INSTRUCTION**: You MUST generate ALL sections (1 through 7) as specified below, in the exact order.

# Your task is to extract real values from the user's uploaded credit report (included below). Based on those values:

# * Provide a clear explanation of each credit factor
# * Judge the quality (e.g., Excellent, Good, Fair, Poor)
# * Assign an internal score for each factor
# * Include plain-language summaries that non-financial users can understand
# * Ensure that if at least one bureau meets all six criteria (Credit Score ≥ 720, No Late Payments, Utilization < 10%, ≤ 3 Inquiries, Credit Age ≥ 2.5 Years, Strong Primary Card Structure), the user is considered eligible for funding, even if other bureaus fail one criterion.

# ---

# **Funding Eligibility Logic**:
# 1. The user qualifies for funding ONLY if ALL of the following are true in at least one bureau:
#    - Credit Score ≥ 720
#    - No Late Payments
#    - Utilization < 10%
#    - ≤ 3 Inquiries in the last 6 months
#    - Credit Age ≥ 2.5 years
#    - Strong Primary Card Structure
# 2. If the user qualifies and is in free mode, say: "🎉 You're eligible for funding! To view your matched bank recommendations (R1, R2, R3), please upgrade to our Premium Plan."
# 3. If the user qualifies and is in paid mode, say: "🎉 You're eligible for funding! See your matched bank recommendations below." and list 3 banks (R1, R2, R3) EXCLUSIVELY from the state-specific bank list for {user_state}.
# 4. If the user does NOT qualify, say: "Your credit profile does not currently qualify for funding. Please follow the action plan in Section 6 to improve your eligibility."
# 5. Ensure the Verdict (Section 5) and Recommended Funding Sequence (Section 7) are consistent. If the user does not qualify in Section 5, Section 7 MUST NOT say they are eligible.

# ---

# 📌 **1. Breakdown by Bureau**

# Generate a table of revolving credit details based on the actual report data. Always extract the data.

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
# - **Cards >= $2K**: Note the number of cards with limits of $2,000 or more . Mention how it supports creditworthiness. End with a label like **Good** or **Needs Improvement**.
# - **Cards >= $5K**: Note the number of cards with limits of $5,000 or more . Mention how it enhances funding readiness. End with a label like **Excellent** or **Fair**.
# - **Score / 144**: Report the total score out of 144 based on the analysis. End with a label like **Excellent** or **Needs Improvement**.

# Each bullet should be brief, clear, and conclude with a bold quality label.

# ---

# ### 📌 2. Revolving Credit Structure

# Always extract the revolving credit details from the report and present them in a structured table. 

# | **Field**                | **Detail**                                  |
# |--------------------------|---------------------------------------------|
# | Open Cards               | [Number of open cards, specify AU/Primary] |
# | Total Limit              | [$Total credit limit']                       |
# | Primary Cards            | [Count or “None”]                           |
# | High-Limit Card Present? | [YES/NO (Mention limit threshold, e.g. $5k+)']|

# Explain each field briefly below the table if needed.

# ---

# 📌 **3. Authorized User (AU) Strategy**

# * How many AU cards are there?
# * What are their limits and ages?
# * Do they help with funding?
# * Recommendation: what AU cards to add or remove.

# ---

# 📌 **4. Funding Readiness by Bureau**

# Ensure all available revolving credit data is extracted from the report and displayed in a table.

# | Criteria                      | Equifax | Experian | TransUnion |
# | ----------------------------- | ------- | -------- | ---------- |
# | Score ≥ 720                   | Yes/No  | Yes/No   | Yes/No    |
# | No Late Payments              | Yes/No  | Yes/No   | Yes/No    |
# | Utilization < 10%             | Yes/No  | Yes/No   | Yes/No    |
# | ≤ 3 Inquiries (last 6 months) | Yes/No  | Yes/No   | Yes/No    |
# | Credit Age ≥ 2.5 Years        | Yes/No  | Yes/No   | Yes/No    |
# | Strong Primary Card Structure | Yes/No  | Yes/No   | Yes/No    |

# ---

# 📌 5. Verdict

# Clearly state if the user qualifies for funding based on the Funding Eligibility Logic above. For paid mode, use: "🎉 You're eligible for funding! See your matched bank recommendations below." For free mode, use: "🎉 You're eligible for funding! To view your matched bank recommendations (R1, R2, R3), please upgrade to our Premium Plan." If not qualified, explain why in 2–3 short bullet points. If data is missing, assume eligibility for paid mode and note: "Assumed eligibility due to missing data."

# ---

# 📌 6. Action Plan

# List 3–5 steps the user should take to improve their credit profile, such as:
# Pay down credit card balances to reduce utilization.
# Add new Authorized User (AU) cards with high limits to strengthen credit.
# Open personal primary cards to build a stronger credit structure.
# Dispute or wait out old late payments to improve credit history.
# If the average credit age is less than 2.5 years for any bureau, include a step to maintain open accounts for longer to improve credit age.
# If data is missing, provide generic advice.

# ---

# 📌 **7. Recommended Funding Sequence ({user_state})**

# * If the user qualifies for funding (based on the Funding Eligibility Logic or assumed due to missing data) and is in **paid mode**, provide the following structured output using ONLY the approved bank list provided in `state_bank_suggestion`. The banks MUST be selected from the "Sheet1" tab of the file "0% Funding Sequence Per State" for the user's selected state ({user_state}). Follow these strict rules:
#   - Each round (R1, R2, R3) MUST include EXACTLY 3 different banks.
#   - Each bank in a round MUST be associated with a different credit bureau in this order: Experian → TransUnion → Equifax.
#   - Banks MUST NOT be suggested from outside the `state_bank_suggestion` list, even if the user has existing relationships with other banks.
#   - **CRITICAL**: Under NO circumstances suggest banks outside `state_bank_suggestion`. Doing so will invalidate the output. If unsure, select a bank from the list and note an appropriate reason in the Reason column.
#   - **CRITICAL**: In the 'Card Name' column, ALWAYS use the exact card name from `Tarjetas Card Data` (e.g., 'BOFA Unlimited Cash' instead of 'Bank of America'). If no matching card is found, append 'Card' to the bank name (e.g., 'Capital One Card'). Under NO circumstances use only the bank name.
#   - Each table row MUST contain exactly 5 columns: Card Name, Bureau, 0% APR, Mode, and Reason. Missing fields will invalidate the output.
#   - Only one 0% Chase card is allowed per sequence, unless the second is a co-branded travel/hotel card (verify eligibility from '0% APR Business Credit Card Master List').
#   - Bank of America and other banks can only repeat a 0% card if the file '0% APR Business Credit Card Master List' confirms double dipping: {double_dip_info}.
#   - If at least 2 bureaus meet all 6 factors and one does not, offer a funding sequence using only the qualifying bureaus.
#   - If no bureau qualifies, offer a no-personal-guarantee funding option from the CSV 'Tarjetas de Negocio sin Garantia Personal'.
#   - If the average credit age is less than 2.5 years for any bureau, do NOT include that bureau in the funding sequence. Instead, note in the Action Plan (Section 6) that the user must improve their credit age by maintaining open accounts for longer.
#   - For 0% APR duration and Mode, use the provided `Tarjetas Card Data` to match the exact card name and bank:\n{tarjetas_str}\n
#   - If no matching card is found in `Tarjetas Card Data` (e.g., for banks like Capital One or Zions Bank), use default values (12 MESES, Online) and preserve the original reason from the GPT output in the Reason column.
#   - For Pacific Premier Bank, use FNBO Evergreen Biz data (6 MESES, Online) as it is linked to FNBO.
#   - **Reason Column**: Provide dynamic reasons based on the user's credit profile (e.g., high credit score, low utilization, minimal inquiries, strong credit history) or bank-specific features (e.g., requires account, flexible approval, single pull, supports double dip). Examples include 'Diversify cards', 'Requires account', 'Flexible approval', 'Single pull', but do NOT hardcode these. Reasons must be relevant to the credit profile or bank characteristics.

#   **ROUND 1**
#   | Card Name          | Bureau   | 0% APR      | Mode         | Reason                  |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | Experian | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | TransUnion | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | Equifax | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |

#   **ROUND 2**
#   | Card Name          | Bureau   | 0% APR      | Mode         | Reason                  |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | Experian | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | TransUnion | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | Equifax | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |

#   **ROUND 3**
#   | Card Name          | Bureau   | 0% APR      | Mode         | Reason                  |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | Experian | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | TransUnion | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |
#   | [Card Name from Tarjetas or append 'Card' to state_bank_suggestion] | Equifax | [Time from Tarjetas or 12 MESES] | [Mode from Tarjetas or Online] | [Dynamic reason based on credit profile or bank characteristics] |

#   **Strategic Insights for Execution**
#   - Generate 4–6 tailored bullet points based on the user's credit profile (e.g., credit score, utilization, inquiries, credit age) and the recommended banks from `state_bank_suggestion`. Examples include:
#     - If inquiries are high (e.g., >2), recommend freezing non-used bureaus (specify which ones based on the funding sequence) to preserve credit inquiries.
#     - If utilization is close to 10%, suggest paying down balances before applying to improve approval odds.
#     - If a bank requires in-branch application (check `Tarjetas Card Data`), advise visiting a local branch in {user_state}.
#     - If credit score is exceptionally high (e.g., ≥780), recommend declaring a higher personal income (e.g., $120,000) to qualify for larger credit limits.
#     - If credit age is strong (e.g., ≥5 years), suggest requesting credit limit increases after 60 days for banks that support early increases (e.g., Chase, AMEX).
#     - If business spending data is available, recommend including it to strengthen applications for banks in the sequence.
#   - Ensure each bullet is specific to the user's credit profile or the characteristics of the recommended banks (e.g., application mode, double-dip eligibility).
#   - Do NOT use generic or hardcoded advice. Each point must be relevant and actionable based on the provided data.

#   **You Are Fully Ready to Execute**
#   - Estimate the potential funding amount based on the user's total credit limit (e.g., if total limit is $50,000, estimate 2–3x that amount, or use bureau scores to estimate $50K–$200K range).
#   - Provide 2–3 tailored next steps based on the user's credit profile and state-specific bank recommendations, such as:
#     - Applying to specific banks in the sequence that align with the user's strongest bureau (e.g., Experian if score is highest).
#     - Preparing specific documents (e.g., business spending statements) for banks requiring in-branch applications.
#     - Contacting Negocio Capital for guided execution if the credit profile is complex (e.g., multiple inquiries or marginal utilization).
#   - Include a call-to-action: "Connect with Negocio Capital for guided execution and BRM support. Schedule a call: [Negocio Capital Website]."
#   - Add a disclaimer: "This analysis is provided by Negocio Capital and must not be shared or redistributed. All Rights Reserved © 2025."

# * If the user qualifies for funding and is in **free mode**, say: "🎉 You're eligible for funding! To view your matched bank recommendations (R1, R2, R3), please upgrade to our Premium Plan."
# * If the user does not qualify for funding, say: "Your credit profile does not currently qualify for funding. Please follow the action plan in Section 6 to improve your eligibility."
# * Ensure this section is consistent with Section 5 (Verdict).

# **FINAL INSTRUCTION**: You MUST generate ALL sections (1–7) in the exact order specified above. Populate all sections with available data from the credit report. If specific data (e.g., Utilization, Avg. Credit Age) is missing, use 'Data not available' only after attempting to extract all relevant information. Skipping any section is INVALID. Now analyze the following report and generate the complete structured output:

# {text}
# {enrichment_context}
# State-specific bank list for {user_state}: {', '.join(state_bank_suggestion) if state_bank_suggestion else 'No banks available'}
# {bank_data_str}
# {tarjetas_str}
# {include_sequence_note}
# """,

#         "Spanish": f"""
# 🧠 Resumen del Informe de Crédito — Versión Mejorada

# Eres un asistente financiero de análisis de crédito para Negocio Capital.

# **INSTRUCCIÓN CRÍTICA**: DEBES generar TODAS las secciones (1 a 7) como se especifica a continuación, en el orden exacto, incluso si faltan datos en el informe de crédito. Si algún dato (por ejemplo, puntaje de crédito, utilización, consultas) no está disponible, usa texto de marcador como 'Datos no disponibles' solo como último recurso después de intentar extraer toda la información relevante del informe de crédito proporcionado. Omitir cualquier sección es INVÁLIDO.

# Tu tarea es extraer los valores reales del informes de crédito proporcionado (abajo). Basado en esos valores:

# * Explica cada factor de forma clara y sencilla
# * Evalúa la calidad (Ej: Excelente, Bueno, Regular, Malo)
# * Asigna una puntuación interna
# * Utiliza un lenguaje fácil de entender por usuarios no financieros
# * Asegúrate de que si al menos un buró cumple con los seis criterios (Puntaje de Crédito ≥ 720, Sin Pagos Atrasados, Utilización < 10%, ≤ 3 Consultas, Edad Crediticia ≥ 2.5 Años, Estructura Sólida de Tarjetas Primarias), el usuario se considera elegible para financiamiento, incluso si otros burós fallan en un criterio.

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
# 3. Si el usuario califica y está en modo pago, di: "🎉 ¡Eres elegible para financiamiento! Consulta tus bancos recomendados a continuación." y lista 3 bancos (R1, R2, R3) EXCLUSIVAMENTE de la lista de bancos aprobados específica del estado ({user_state}).
# 4. Si el usuario NO califica, di: "Tu perfil de crédito no califica actualmente para financiamiento. Por favor, sigue el plan de acción en la Sección 6 para mejorar tu elegibilidad."
# 5. Asegúrate de que el Veredicto (Sección 5) y la Secuencia de Financiamiento Recomendada (Sección 7) sean consistentes. Si el usuario no califica en la Sección 5, la Sección 7 NO DEBE decir que es elegible.

# ---

# 📌 **1. Desglose por Buró**

# Genera una tabla como esta basada en los datos reales del informe o 'Datos no disponibles' si la extracción falla:

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

# Después de la tabla, incluye un análisis breve en formato de viñetas (puntos), explicando cada categoría individualmente en lenguaje sencillo y accesible. Usa este formato:

# - **Puntaje de Crédito**: Reporta el puntaje de crédito para cada buró o 'Datos no disponibles'. Menciona si cumple con el umbral de 720. Finaliza con una etiqueta como **Excelente**, **Bueno**, **Regular**, o **Malo**.
# - **Historial Limpio**: Resume si hay pagos atrasados o incumplimientos o 'Datos no disponibles'. Si no hay, di "Sí". Finaliza con una etiqueta como **Excelente** o **Debe Mejorar**.
# - **Utilización**: Indica el porcentaje total de utilización o 'Datos no disponibles'. Explica si está por debajo del 10% y cómo afecta la elegibilidad de financiamiento. Termina con una etiqueta como **Excelente**, **Bueno**, o **Riesgoso**.
# - **Consultas Duras (6 meses)**: Indica cuántas consultas hubo en los últimos 6 meses o 'Datos no disponibles'. Menciona si es aceptable (≤ 3). Finaliza con una etiqueta como **Bueno**, **Regular**, o **Riesgoso**.
# - **Edad Promedio Crédito**: Explica la edad promedio de las cuentas o 'Datos no disponibles'. Di si cumple con el umbral de 2.5 años. Finaliza con una etiqueta como **Excelente** o **Regular**.
# - **Tarjetas >= $2K**: Nota la cantidad de tarjetas con límites de $2,000 o más o 'Datos no disponibles'. Menciona cómo apoya la solvencia crediticia. Finaliza con una etiqueta como **Bueno** o **Debe Mejorar**.
# - **Tarjetas >= $5K**: Nota la cantidad de tarjetas con límites de $5,000 o más o 'Datos no disponibles'. Menciona cómo mejora la preparación para financiamiento. Finaliza con una etiqueta como **Excelente** o **Regular**.
# - **Puntaje / 144**: Reporta el puntaje total de 144 basado en el análisis o 'Datos no disponibles'. Finaliza con una etiqueta como **Excelente** o **Debe Mejorar**.

# Cada viñeta debe ser breve, clara y cerrar con una etiqueta de calidad en **negrita**.

# ---

# ### 📌 2. Estructura de Crédito Revolvente

# Presenta los detalles del crédito revolvente en una tabla como esta (usa 'Datos no disponibles' si la extracción falla):

# | **Campo**                     | **Detalle**                                         |
# |-------------------------------|-----------------------------------------------------|
# | Tarjetas Abiertas             | [Número de tarjetas abiertas, indicar AU/Principal o 'Datos no disponibles'] |
# | Límite Total                  | [$Límite total de crédito o 'Datos no disponibles']                          |
# | Tarjetas Primarias            | [Cantidad o “Ninguna” o 'Datos no disponibles']                              |
# | ¿Tarjetas de Alto Límite?     | [SÍ/NO (Indicar umbral, por ejemplo $5,000+) o 'Datos no disponibles']       |

# Explica brevemente cada campo debajo de la tabla si es necesario.

# ---

# 📌 **3. Estrategia de Usuario Autorizado (AU)**

# * ¿Cuántas tarjetas AU tiene o 'Datos no disponibles'?
# * ¿Sus límites y antigüedad o 'Datos no disponibles'?
# * ¿Ayuda al perfil crediticio?
# * ¿Qué se recomienda añadir o eliminar? (Proporciona consejos genéricos si faltan datos)

# ---

# 📌 **4. Preparación para Financiamiento**

# | Criterio                        | Equifax | Experian | TransUnion |
# | ------------------------------- | ------- | -------- | ---------- |
# | Puntaje ≥ 720                   | Sí/No/Datos no disponibles   | Sí/No/Datos no disponibles    | Sí/No/Datos no disponibles      |
# | Sin pagos atrasados             | Sí/No/Datos no disponibles   | Sí/No/Datos no disponibles    | Sí/No/Datos no disponibles      |
# | Utilización < 10%               | Sí/No/Datos no disponibles   | Sí/No/Datos no disponibles    | Sí/No/Datos no disponibles      |
# | ≤ 3 consultas (últimos 6 meses) | Sí/No/Datos no disponibles   | Sí/No/Datos no disponibles    | Sí/No/Datos no disponibles      |
# | Edad crediticia ≥ 2.5 años      | Sí/No/Datos no disponibles   | Sí/No/Datos no disponibles    | Sí/No/Datos no disponibles      |
# | Buena estructura de tarjetas    | Sí/No/Datos no disponibles   | Sí/No/Datos no disponibles    | Sí/No/Datos no disponibles      |

# ---

# 📌 5. Veredicto

# Indicar claramente si el usuario califica para financiamiento según la Lógica de Elegibilidad para Financiamiento. Para el modo pago, usa: "🎉 ¡Eres elegible para financiamiento! Consulta tus bancos recomendados a continuación." Para el modo gratuito, usa: "🎉 ¡Eres elegible para financiamiento! Para ver tus bancos recomendados (R1, R2, R3), por favor actualiza a nuestro Plan Premium." Si el usuario no califica, proporcionar 2–3 razones breves que expliquen por qué. Si faltan datos, asume elegibilidad para el modo pago y anota: "Elegibilidad asumida debido a datos faltantes."

# ---

# 📌 6. Plan de Acción

# Enumerar 3–5 pasos que el usuario debe tomar para mejorar su perfil crediticio, como:
# Pagar los saldos de las tarjetas de crédito para reducir la utilización.
# Agregar nuevas tarjetas de usuario autorizado (AU) con límites altos para fortalecer el crédito
# Abrir tarjetas primarias personales para construir una estructura crediticia más sólida.
# Disputar o esperar a que prescriban pagos atrasados antiguos para mejorar el historial crediticio.
# Si la edad crediticia promedio es menor a 2.5 años para cualquier buró, incluye un paso para mantener las cuentas abiertas por más tiempo para mejorar la edad crediticia.
# Si faltan datos, proporciona consejos genéricos.

# ---

# 📌 **7. Recomendación de Bancos ({user_state})**

# * Si el usuario califica y está en **modo pago**, proporciona la siguiente salida estructurada usando SÓLO la lista de bancos aprobados en `state_bank_suggestion`. Los bancos DEBEN seleccionarse del "Sheet1" del archivo "0% Funding Sequence Per State" para el estado seleccionado por el usuario ({user_state}). Sigue estas reglas estrictas:
#   - Cada ronda (R1, R2, R3) DEBE incluir EXACTAMENTE 3 bancos diferentes.
#   - Cada banco en una ronda DEBE estar asociado con un buró de crédito diferente en este orden: Experian → TransUnion → Equifax.
#   - Los bancos NO DEBEN sugirirse fuera de la lista `state_bank_suggestion`, incluso si el usuario tiene relaciones existentes con otros bancos.
#   - **CRÍTICO**: Bajo NINGUNA circunstancia sugieras bancos fuera de `state_bank_suggestion`. Hacerlo invalidará la salida. Si no estás seguro, selecciona un banco de la lista y anota una razón relevante en la columna Razón.
#   - **CRÍTICO**: En la columna 'Nombre de la Tarjeta', SIEMPRE usa el nombre exacto de la tarjeta de `Tarjetas Card Data` (por ejemplo, 'BOFA Unlimited Cash' en lugar de 'Bank of America'). Si no se encuentra una tarjeta coincidente, agrega 'Card' al nombre del banco (por ejemplo, 'Capital One Card'). Bajo NINGUNA circunstancia uses solo el nombre del banco.
#   - Cada fila de la tabla DEBE contener exactamente 5 columnas: Nombre de la Tarjeta, Buró, 0% APR, Modo, y Razón. Campos faltantes invalidarán la salida.
#   - Solo se permite una tarjeta Chase al 0% por secuencia, a menos que la segunda sea una tarjeta de viaje/hotel co-brandeada (verifica la elegibilidad en '0% APR Business Credit Card Master List').
#   - Bank of America y otros bancos solo pueden repetir una tarjeta al 0% si el archivo '0% APR Business Credit Card Master List' confirma que permiten "double dipping": {double_dip_info}.
#   - Si al menos 2 burós cumplen con los 6 factores y uno no, ofrece una secuencia de financiamiento usando solo los burós que califican.
#   - Si ningún buró califica, ofrece una opción de financiamiento sin garantía personal del CSV "Tarjetas de Negocio sin Garantia Personal".
#   - Si la edad crediticia promedio es menor a 2.5 años para cualquier buró, NO incluyas ese buró en la secuencia de financiamiento. En su lugar, indica en el Plan de Acción (Sección 6) que el usuario debe mejorar su edad crediticia manteniendo cuentas abiertas por más tiempo.
#   - La selección de bancos DEBE coincidir con el perfil crediticio del usuario (por ejemplo, puntaje de crédito, utilización, historial crediticio) y la secuencia de bancos específica del estado. Si faltan datos, selecciona bancos basados en la lista del estado y anota: "Seleccionado de la lista del estado debido a datos faltantes."
#   - Para la duración del 0% APR y el Modo, usa los datos proporcionados en `Tarjetas Card Data` para coincidir con el nombre exacto de la tarjeta y el banco:\n{tarjetas_str}\n
#   - Si no se encuentra una tarjeta coincidente en `Tarjetas Card Data` (por ejemplo, para bancos como Capital One o Zions Bank), usa valores predeterminados (12 MESES, Online) y anótalo en la columna Razón como 'Valores predeterminados usados debido a datos faltantes en Tarjetas'. Bajo NINGUNA circunstancia uses '0%' como valor de APR.
#   - Para Pacific Premier Bank, usa los datos de FNBO Evergreen Biz (6 MESES, Online (Omaha Zip)) ya que está vinculado a FNBO.
#   - **Columna Razón**: Proporciona razones dinámicas basadas en el perfil crediticio del usuario (por ejemplo, puntaje de crédito alto, utilización baja, consultas mínimas, historial crediticio sólido) o características específicas del banco (por ejemplo, requiere cuenta, aprobación flexible, extracción única, permite double dipping). Ejemplos incluyen 'Diversificar tarjetas', 'Requiere cuenta', 'Aprobación flexible', 'Extracción única', pero NO los codifiques de forma fija. Las razones deben ser relevantes para el perfil crediticio o las características del banco.

#   **RONDA 1**
#   | Nombre de la Tarjeta   | Buró     | 0% APR      | Modo         | Razón                   |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | Experian | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | TransUnion | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | Equifax | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |

#   **RONDA 2**
#   | Nombre de la Tarjeta   | Buró     | 0% APR      | Modo         | Razón                   |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | Experian | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | TransUnion | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | Equifax | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |

#   **RONDA 3**
#   | Nombre de la Tarjeta   | Buró     | 0% APR      | Modo         | Reason                  |
#   |--------------------|----------|-------------|--------------|-------------------------|
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | Experian | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | TransUnion | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |
#   | [Nombre de Tarjeta de Tarjetas o agregar 'Card' a state_bank_suggestion] | Equifax | [Tiempo de Tarjetas o 12 MESES] | [Modo de Tarjetas o Online] | [Razón dinámica basada en el perfil crediticio o características del banco] |

#   **Perspectivas Estratégicas para la Ejecución**
#   - Genera 4–6 puntos personalizados basados en el perfil crediticio del usuario (por ejemplo, puntaje de crédito, utilización, consultas, edad crediticia) y los bancos recomendados de `state_bank_suggestion`. Ejemplos incluyen:
#     - Si las consultas son altas (por ejemplo, >2), recomienda congelar los burós no utilizados (especifica cuáles según la secuencia de financiamiento) para preservar las consultas.
#     - Si la utilización está cerca del 10%, sugiere pagar los saldos antes de solicitar para mejorar las probabilidades de aprobación.
#     - Si un banco requiere solicitud en sucursal (verifica `Tarjetas Card Data`), aconseja visitar una sucursal local en {user_state}.
#     - Si el puntaje de crédito es excepcionalmente alto (por ejemplo, ≥780), recomienda declarar un ingreso personal más alto (por ejemplo, $120,000) para calificar para límites de crédito más grandes.
#     - Si la edad crediticia es sólida (por ejemplo, ≥5 años), sugiere solicitar aumentos de límite después de 60 días para bancos que permitan aumentos tempranos (por ejemplo, Chase, AMEX).
#     - Si hay datos de gastos comerciales disponibles, recomienda incluirlos para fortalecer las solicitudes para los bancos en la secuencia.
#   - Asegúrate de que cada punto sea específico al perfil crediticio del usuario o a las características de los bancos recomendados (por ejemplo, modo de solicitud, elegibilidad para double dipping).
#   - NO uses consejos genéricos o codificados. Cada punto debe ser relevante y accionable basado en los datos proporcionados.

#   **Estás Completamente Listo para Ejecutar**
#   - Estima la cantidad potencial de financiamiento basada en el límite total de crédito del usuario (por ejemplo, si el límite total es $50,000, estima 2–3 veces esa cantidad, o usa los puntajes de los burós para estimar un rango de $50K–$200K).
#   - Proporciona 2–3 pasos siguientes personalizados basados en el perfil crediticio del usuario y las recomendaciones de bancos específicas del estado, como:
#     - Solicitar a bancos específicos en la secuencia que se alineen con el buró más fuerte del usuario (por ejemplo, Experian si el puntaje es el más alto).
#     - Preparar documentos específicos (por ejemplo, estados de gastos comerciales) para bancos que requieran solicitudes en sucursal.
#     - Contactar a Negocio Capital para una ejecución guiada si el perfil crediticio es complejo (por ejemplo, múltiples consultas o utilización marginal).
#   - Incluye una llamada a la acción: "Conecta con Negocio Capital para una ejecución guiada y soporte BRM. Agenda una llamada: [Negocio Capital Website]."
#   - Agrega un descargo de responsabilidad: "Este análisis es proporcionado por Negocio Capital y no debe compartirse ni redistribuirse. Todos los derechos reservados © 2025."
#   - Proporciona un marcador para el informe en PDF: "Descarga el informe en PDF con el logo: [file-Qn75Jt2kS9XtYnggLMzajL]."

# * Si el usuario califica y está en **modo gratuito**, di: "🎉 ¡Eres elegible para financiamiento! Para ver tus bancos recomendados (R1, R2, R3), por favor actualiza a nuestro Plan Premium."
# * Si el usuario NO califica, di: "Tu perfil de crédito no califica actualmente para financiamiento. Por favor, sigue el plan de acción en la Sección 6 para mejorar tu elegibilidad."
# * Asegúrate de que esta sección sea consistente con la Sección 5 (Veredicto).

# **INSTRUCCIÓN FINAL**: DEBES generar TODAS las secciones (1–7) en el orden exacto especificado arriba. Rellena todas las secciones con los datos disponibles del informe de crédito. Si faltan datos específicos (por ejemplo, Utilización, Edad Promedio del Crédito), usa 'Datos no disponibles' solo después de intentar extraer toda la información relevante. Omitir cualquier sección es INVÁLIDO. Ahora analiza el siguiente informe y genera la salida estructurada completa:

# {text}
# {enrichment_context}
# Lista de bancos específicos del estado ({user_state}): {', '.join(state_bank_suggestion) if state_bank_suggestion else 'No banks available'}
# {bank_data_str}
# {tarjetas_str}
# {include_sequence_note}
# """
#     }

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "You are a strict, accurate AI financial credit analyst from Negocio Capital. You must extract all data exactly as available in the text. Do NOT hallucinate. Do NOT say 'Data not available'. Always follow instructions strictly. Be formal and expert in tone."},
#                 {"role": "user", "content": prompt_template[language]}
#             ],
#             max_tokens=3900,
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
#         analysis = validate_gpt_output(analysis, state_bank_suggestion, user_state, mode)
#         return analysis
#     except Exception as lỗi:
#         logging.error(f"GPT-4 error: {str(lỗi)}")
#         print(f"❌ GPT-4 error: {str(lỗi)}")
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
#     except Exception as lỗi:
#         logging.error(f"Error saving PDF: {str(lỗi)}")
#         print(f"❌ Error saving PDF: {str(lỗi)}")

# # === Main CLI ===
# def main():
#     print("📂 Welcome to Funding NC AI Credit Report Analyzer!")
#     # Update TARJETAS_CARDS from PDF
#     update_tarjetas_from_pdf(TARJETAS_PATH)
    
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