import itertools
import pandas as pd

def generate_variants(finish, color_atr, attributes, categories):
    """
    Generate all possible combinations of product variants based on given attribute lists.
    """
    category_lists = {
        'Finish': finish,
        'Color': color_atr,
        'Attributes': attributes,
        'Sizes': categories.get('sizes', []),
        'Voltages': categories.get('voltages', []),
        'Angles': categories.get('angles', []),
        'Temperatures': categories.get('temperatures', []),
        'Numbers': categories.get('numbers', []),
        'Words': categories.get('words', []),
        'Others': categories.get('others', [])
    }

    # Remove empty lists to avoid unnecessary combinations
    valid_categories = {key: values for key, values in category_lists.items() if values}

    # Generate all possible combinations
    all_combinations = list(itertools.product(*valid_categories.values()))

    # Convert combinations into a list of dictionaries for DataFrame
    variant_data = [dict(zip(valid_categories.keys(), combination)) for combination in all_combinations]

    return variant_data

def save_variants_to_excel(variants, output_file):
    """
    Save the generated variants to an Excel file.
    """
    df = pd.DataFrame(variants)
    df.to_excel(output_file, index=False)
    print(f"Variants saved to {output_file}")

# Example Data (Replace with actual scraped data)
finish = ["Matte", "Glossy"]
color_atr = ["Red", "Blue"]
attributes = ["Waterproof", "Scratch-resistant"]
categories = {
    'sizes': ["Small", "Medium", "Large"],
    'voltages': ["110V", "220V"],
    'angles': ["45°", "90°"],
    'temperatures': ["Hot", "Cold"],
    'numbers': ["One", "Two"],
    'words': ["Lightweight", "Durable"],
    'others': ["Special Edition"]
}

# Generate and save variants
variants = generate_variants(finish, color_atr, attributes, categories)
save_variants_to_excel(variants, "product_variants.xlsx")
