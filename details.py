import pandas
import re
import glob

# Default import for single file - requires manual editing to target file
# data = pandas.read_csv("tender_test.csv", na_values=['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A', 'NA', '#NA', 'NULL', 'NaN', '-NaN', 'nan', '-nan', ''], keep_default_na=False)

# Grabs list of all files in same folder as script
all_files = glob.glob('*.csv')

# Joins all CSV files together, creates complete DataFrame
df_from_each_file = (pandas.read_csv(f, na_values=['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A', 'NA', '#NA', 'NULL', 'NaN', '-NaN', 'nan', '-nan', ''], keep_default_na=False) for f in all_files)
concat_df = pandas.concat(df_from_each_file, ignore_index=True)

# Iterates through each row of the joined CSV files
# Grabs "Response" column details to extract postcode and account number
for idx, row in concat_df.iterrows():
    details = row["Response"]

    # Postcode Section
    # Finds valid full UK postcode in string

    postcode_ext = re.search(r'(GIR(?=\s*0AA)|(?:[BEGLMNSW]|[A-PR-UWYZ][A-HK-Y])[0-9](?:[0-9]|(?:(?<=N1|E1|W1)|(?<=SE1|SW1|NW1|EC[0-9]|WC[0-9])[A-HJ-NP-Z])?))\s*([0-9][ABD-HJLNP-UW-Z]{2})', str(details), flags=re.I)
    if postcode_ext:
        details.replace(postcode_ext.group(0), "")
        postcode_ext = postcode_ext.group(0).upper()
        if (len(postcode_ext) > 5 and postcode_ext[-4] == " ") or (len(postcode_ext) < 6):
            concat_df.loc[idx,"Postcode"] = postcode_ext
        elif len(postcode_ext) > 5:
            concat_df.loc[idx, "Postcode"] = postcode_ext[:-3] + " " + postcode_ext[-3:]
        else:
            concat_df.loc[idx, "Postcode"] = "Unexpected Behaviour"

    # Account Number Section
    # Finds valid account number in string

    account_ext = re.search(r'([0-2][a-zA-Z][0-9]{3}[a-zA-Z])', str(details))
    if account_ext:
        details.replace(account_ext.group(0), "")
        account_ext = account_ext.group(0).upper()
        concat_df.loc[idx,"Acc No"] = account_ext

    # Remaining Text Section
    # Removes postcode and account number and returns the rest of the string

    concat_df.loc[idx,"Remaining Details"] = details

# Creates output CSV file
concat_df.to_csv("extracted_data.csv")
print("File created")
