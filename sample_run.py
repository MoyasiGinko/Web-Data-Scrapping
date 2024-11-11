import pandas as pd


# Data for the new list of companies
new_company_data = {
    "Company Name": [
        "Regent Zhejiang AUTO Pty Ltd.,Co", "Zhejiang Lan Man Long Car Co., Ltd.", "Zhejiang Hobby Automobile Trading Co., Ltd.",
        "Henan Jishang Automobile Sales Co., LTD", "Specialty Vehicle Division Zhengzhou Yutong Bus Co., LTD",
        "Baoding Livezone Automobile Service Co., Ltd.", "Jiangsu Jinghang Automobile Co., Ltd", "Armadillo",
        "Changsha Xiakele Automobile Manufacturing Company Ltd.", "BJFRT", "REV Group", "Fendt Caravan",
        "ETRV Technology Co., Ltd"
    ],
    "Website": [
        "N/A", "N/A", "N/A", "N/A", "https://en.yutong.com/",
        "N/A", "N/A", "N/A", "N/A", "N/A", "https://www.revgroup.com/",
        "https://www.fendt-caravan.com/", "N/A"
    ],
    "Country of Origin": [
        "China", "China", "China", "China", "China",
        "China", "China", "China", "China", "China",
        "United States", "Germany", "China"
    ],
    "Industry Specialized": [
        "Manufacturing and distribution of recreational vehicles and campers in the Chinese market.",
        "Manufactures and distributes vehicles for recreation and camping.",
        "Trading and distribution of recreational vehicles, motorhomes, and caravans.",
        "Sales and distribution of specialized vehicles, including campers and recreational vehicles.",
        "Develops and manufactures specialty vehicles, including buses and coaches for various applications.",
        "Provides automobile services, focusing on specialized vehicles for recreational purposes.",
        "Manufacturing and sales of recreational vehicles, with a focus on campervans and motorhomes.",
        "Produces compact campers and caravans, particularly off-road capable models.",
        "Manufacturing of specialized vehicles for recreational use.",
        "Develops and manufactures recreational vehicles and specialized automobiles.",
        "Designs and manufactures specialty vehicles for various markets, including RVs, ambulances, and fire trucks.",
        "Manufacturer of caravans and trailers, providing a range of models for leisure travel.",
        "Develops electric recreational vehicle technology and components, focusing on eco-friendly travel solutions."
    ]
}

# Creating DataFrame for the new company data
df_new_companies = pd.DataFrame(new_company_data)

# Saving the DataFrame to an Excel file
new_company_file_path = "new_company_industry_specialized_websites.xlsx"
df_new_companies.to_excel(new_company_file_path, index=False)

new_company_file_path
