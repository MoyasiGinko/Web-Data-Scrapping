import json
import itertools
import pandas as pd

def load_product_data(json_file):
    """
    Load product data from JSON file with proper UTF-8 encoding.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except UnicodeDecodeError:
        with open(json_file, 'r', encoding='utf-8-sig') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def generate_variants(product):
    """
    Generate all possible combinations of product variants, handling missing data.
    """
    # Initialize base fields that will always be included
    base_fields = {
        'Product_ID': product.get('product_id', 'NA'),
        'URL': product.get('url', 'NA')
    }

    # Collect all non-empty variant options
    variant_fields = {}

    # Add direct fields if they have values
    finish_options = product.get('finish_options', [])
    color_attributes = product.get('color_attributes', [])
    attributes = product.get('attributes', [])

    if finish_options:
        variant_fields['Finish'] = finish_options
    if color_attributes:
        variant_fields['Color'] = color_attributes
    if attributes:
        variant_fields['Attributes'] = attributes

    # Add category fields if they have values
    categories = product.get('categories', {})
    for category, values in categories.items():
        if values:  # Only add non-empty categories
            variant_fields[category.capitalize()] = values

    # If there are variant fields, generate combinations
    if variant_fields:
        variant_keys = list(variant_fields.keys())
        variant_values = list(variant_fields.values())
        combinations = list(itertools.product(*variant_values))

        # Create variant dictionaries
        variants = []
        for combo in combinations:
            variant = base_fields.copy()
            variant.update(dict(zip(variant_keys, combo)))
            variants.append(variant)
    else:
        # If no variants, just return the base fields
        variants = [base_fields]

    # Convert the dictionary of lists to a list of dictionaries
    result = []
    for variant in variants:
        variant_dict = {key: (value if value else 'NA') for key, value in variant.items()}
        result.append(variant_dict)

    return result

def process_all_products(json_file, output_file):
    """
    Process all products from JSON file and save variants to Excel.
    """
    try:
        # Load product data
        products = load_product_data(json_file)
        if not products:
            print("No valid product data found.")
            return

        # Generate variants for all products
        all_variants = []
        for product in products:
            product_variants = generate_variants(product)
            all_variants.extend(product_variants)

        # Create DataFrame
        df = pd.DataFrame(all_variants)

        # Define the desired column order
        column_order = [
            'Product_ID', 'URL', 'length_of_entry', 'Finish', 'Color', 'Attributes',
            'Sizes', 'Voltages', 'Angles', 'Temperatures', 'Numbers', 'Words', 'Others'
        ]

        # Ensure all columns exist (fill with "NA" if missing)
        for col in column_order:
            if col not in df.columns:
                df[col] = "NA"

        # Reorder columns
        df = df[column_order]

        # Replace NaN values with "NA"
        df.fillna("NA", inplace=True)

        # Count variants per Product_ID
        product_counts = df['Product_ID'].value_counts()

        # Map the counts to categories
        def classify_size(count):
            if count <= 6:
                return "Small"
            elif count <= 16:
                return "Medium"
            elif count <= 40:
                return "Large"
            else:
                return "Very Large"

        # Create `length_of_entry` column based on product variant count
        df['length_of_entry'] = df['Product_ID'].map(product_counts).apply(classify_size)

        # Save to Excel
        df.to_excel(output_file, index=False)

        print(f"Variants saved to {output_file}")
        print(f"Total number of variants generated: {len(all_variants)}")
        print(f"Columns included: {', '.join(df.columns)}")

        # Print first few variants for verification
        print("\nFirst few variants generated:")
        print(df.head().to_string())

    except Exception as e:
        print(f"Error processing products: {str(e)}")
        raise

# Execute the program
if __name__ == "__main__":
    try:
        input_file = "all_products.json"
        output_file = "product_variants.xlsx"
        process_all_products(input_file, output_file)
    except Exception as e:
        print(f"Program failed: {str(e)}")
