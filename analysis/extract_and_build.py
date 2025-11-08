
import pandas as pd
import os

def extract_world_bank_data(csv_path):

    print(" Lecture du fichier Banque Mondiale...")
    
    # Lire le CSV
    df = pd.read_csv(csv_path)
    
    # Filtrer juste les 4 indicateurs qui nous intéressent
    indicators = {
        'GDP (current US$)': 'gdp',
        'Population, total': 'population',
        'Individuals using the Internet (% of population)': 'internet',
        'Mobile cellular subscriptions (per 100 people)': 'mobile'
    }
    
    # Créer un dictionnaire pour stocker les données par pays
    countries_data = {}
    
    for _, row in df.iterrows():
        country = row['Country Name']
        series = row['Series Name']
        value = row['2024 [YR2024]']
        
        # Ignorer les lignes vides
        if pd.isna(country) or country == '':
            continue
        
        # Initialiser le pays s'il n'existe pas
        if country not in countries_data:
            countries_data[country] = {}
        
        # Stocker la valeur selon l'indicateur
        for indicator_name, key in indicators.items():
            if series == indicator_name:
                countries_data[country][key] = value
    
    return countries_data

def create_market_data_with_real_data():
 
    
    print("\n" + " "*35)
    print("   CRÉATION DE market_data.csv AVEC MES VRAIES DONNÉES")
    print(" "*35 + "\n")
    

    
    world_bank_data = {
        'Senegal': {
            'gdp': 32267254425.052,     
            'population': 18501984,     
            'internet': 58.2,             
            'mobile': 115.5               
        },
        'Cote_Ivoire': {
            'gdp': 86538413923.3943,  
            'population': 31934230,  
            'internet': 47.0,          
            'mobile': 142.3               
        },
        'Cameroon': {
            'gdp': 51326764684.8595,     
            'population': 29123744,          
            'internet': 38.5,                
            'mobile': 89.7                   
        },
        'Morocco': {
            'gdp': 154430996472.752,        
            'population': 38081173,          
            'internet': 88.1,                
            'mobile': 132.8                  
        },
        'Tunisia': {
            'gdp': 53409988744.5968,        
            'population': 12277109,          
            'internet': 74.3,                
            'mobile': 130.2                  
        },
        'Burkina_Faso': {
            'gdp': 23250214909.5391,        
            'population': 23548781,          
            'internet': 24.5,                
            'mobile': 110.8                  
        }
    }
    

    
    wikipedia_counts = {
        'Senegal': {'banks': 29, 'insurance': 30},
        'Cote_Ivoire': {'banks': 29, 'insurance': 32},
        'Cameroon': {'banks': 19, 'insurance': 30},
        'Morocco': {'banks': 32, 'insurance': 26},
        'Tunisia': {'banks': 26, 'insurance': 22},
        'Burkina_Faso': {'banks': 16, 'insurance': 17}
    }
    

    
    rows = []
    
    for country in world_bank_data.keys():
        data = world_bank_data[country]
        counts = wikipedia_counts[country]
        
        # Convertir GDP en milliards
        gdp_billions = data['gdp'] / 1_000_000_000
        
        # Convertir population en millions
        population_millions = data['population'] / 1_000_000
        
        # Calculs standards industrie
        it_market_m = gdp_billions * 0.025 * 1000  # 2.5% du PIB
        cyber_spending_m = it_market_m * 0.03      # 3% du marché IT
        smes_count = int(population_millions * 4000)  # 4 PME / 1000 habitants
        
        row = {
            'Country': country,
            'Population_M': round(population_millions, 1),
            'GDP_B_USD': round(gdp_billions, 1),
            'IT_Market_M_USD': round(it_market_m, 1),
            'Cybersecurity_Spending_M_USD': round(cyber_spending_m, 1),
            'Banks_Count': counts['banks'],
            'Insurance_Companies': counts['insurance'],
            'SMEs_Count': smes_count,
            'Internet_Penetration_Pct': data['internet'],
            'Mobile_Penetration_Pct': data['mobile']
        }
        
        rows.append(row)
    
    # Créer DataFrame
    df = pd.DataFrame(rows)
    
    # Sauvegarder
    output_path = '../data/market_data.csv'
    df.to_csv(output_path, index=False)
    
    print("\n" + "="*70)
    print("   FICHIER market_data.csv CRÉÉ AVEC TES VRAIES DONNÉES!")
    print("="*70)
    print(f"\n   Emplacement: {os.path.abspath(output_path)}")
    
    print("\n  APERÇU DE TES DONNÉES:\n")
    print(df.to_string(index=False))
    
    print("\n" + "="*70)
    print("   SOURCES DES DONNÉES:")
    print("="*70)
    print("   PIB (2024): Banque Mondiale - TES données")
    print("   Population (2024): Banque Mondiale - TES données")
    print("   Banques: Wikipedia - TES comptages")
    print("   Assurances: Wikipedia - TES comptages")
    print("   Internet/Mobile: Estimations 2023 (données 2024 non disponibles)")
    print("   Marché IT: Calculé (2.5% du PIB)")
    print("   Dépenses Cyber: Calculé (3% du marché IT)")
    print("   Nombre PME: Calculé (4 PME/1000 habitants)")
    
    print("\n" + "="*70)
    print("   RECOMMANDATION:")
    print("="*70)
    print("Pour avoir les vraies données Internet/Mobile 2023:")
    print("1. Retourne sur https://databank.worldbank.org")
    print("2. Change l'année de 2024 → 2023")
    print("3. Télécharge à nouveau")
    print("4. Relance ce script")
    print("="*70 + "\n")
    
    print("  PROCHAINES ÉTAPES:")
    print("1.    Vérifie les données ci-dessus")
    print("2.    Lance: python market_analysis.py")
    print("3.    Lance: python visualization.py")
    print("\n")
    
    return df

def main():
    """Fonction principale"""
    
    print("\n   EXTRACTION ET CRÉATION AUTOMATIQUE\n")
    
   
    
    df = create_market_data_with_real_data()
    
    print("   TERMINÉ! Tes données sont prêtes!   \n")

if __name__ == "__main__":
    main()