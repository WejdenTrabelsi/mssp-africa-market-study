

import pandas as pd
import os

def create_market_data():

    
    data = {
        'Senegal': {
            'population_m': 17.2,     
            'gdp_b_usd': 27.6,         
            'internet_pct': 58.2,     
            'mobile_pct': 115.5,       
            'banks': 29,               
            'insurance': 30            
        },
        'Cote_Ivoire': {
            'population_m': 27.5,      
            'gdp_b_usd': 70.0,        
            'internet_pct': 47.0,      
            'mobile_pct': 142.3,      
            'banks': 29,               
            'insurance': 32           
        },
        'Cameroon': {
            'population_m': 27.9,       
            'gdp_b_usd': 44.9,       
            'internet_pct': 38.5,      
            'mobile_pct': 89.7,
            'banks': 19,          
            'insurance': 30           
        },
        'Morocco': {
            'population_m': 37.5, 
            'gdp_b_usd': 134.2,       
            'internet_pct': 84.1,     
            'mobile_pct': 130.2,       
            'banks': 32,          
            'insurance': 26           
        },
        'Tunisia': {
            'population_m': 12.0,    
            'gdp_b_usd': 46.8,         
            'internet_pct': 71.5,      
            'mobile_pct': 128.9,       
            'banks': 26,               
            'insurance': 22            
        },
        'Burkina_Faso': {
            'population_m': 22.1,      
            'gdp_b_usd': 19.7,        
            'internet_pct': 22.0,    
            'mobile_pct': 106.8,       
            'banks': 16,              
            'insurance': 17            
        }
    }
    

    
    rows = []
    
    for country, values in data.items():
        # Calculs standards industrie
        it_market_m = values['gdp_b_usd'] * 0.025 * 1000  # 2.5% du PIB
        cyber_spending_m = it_market_m * 0.03  # 3% du marché IT
        smes_count = int(values['population_m'] * 4000)  # 4 PME / 1000 habitants
        
        row = {
            'Country': country,
            'Population_M': values['population_m'],
            'GDP_B_USD': values['gdp_b_usd'],
            'IT_Market_M_USD': round(it_market_m, 1),
            'Cybersecurity_Spending_M_USD': round(cyber_spending_m, 1),
            'Banks_Count': values['banks'],
            'Insurance_Companies': values['insurance'],
            'SMEs_Count': smes_count,
            'Internet_Penetration_Pct': values['internet_pct'],
            'Mobile_Penetration_Pct': values['mobile_pct']
        }
        
        rows.append(row)
    
    # Créer DataFrame
    df = pd.DataFrame(rows)
    
    # Sauvegarder
    output_path = '../data/market_data.csv'
    df.to_csv(output_path, index=False)
    
    print("\n" + "="*70)
    print("   FICHIER market_data.csv CRÉÉ AVEC SUCCÈS!")
    print("="*70)
    print(f"\n   Emplacement: {os.path.abspath(output_path)}")
    print("\n  Aperçu des données:\n")
    print(df.to_string(index=False))
    
    print("\n" + "="*70)
    print("  PROCHAINES ÉTAPES:")
    print("="*70)
    print("1. Vérifie les données ci-dessus")
    print("2. Si tout est correct, lance: python market_analysis.py")
    print("3. Puis: python visualization.py")
    print("="*70 + "\n")
    
    return df

def show_instructions():
    """Affiche les instructions pour remplir les données"""
    print("\n" + "  "*35)
    print("   INSTRUCTIONS: Comment remplir tes données")
    print("  "*35 + "\n")
    
    print("   ÉTAPE 1: Ouvre ton CSV de la Banque Mondiale")
    print("   Trouve pour chaque pays:")
    print("   • GDP (current US$) → Divise par 1,000,000,000 pour avoir en milliards")
    print("   • Population, total → Divise par 1,000,000 pour avoir en millions")
    print("   • Individuals using Internet (% of pop.) → Garde tel quel")
    print("   • Mobile cellular subscriptions → Garde tel quel")
    
    print("\n   ÉTAPE 2: Édite ce fichier (build_market_data.py)")
    print("   Remplace les valeurs dans le dictionnaire 'data'")
    print("      NE touche PAS aux chiffres banks/insurance (déjà corrects!)")
    
    print("\n   ÉTAPE 3: Exécute ce script")
    print("   python build_market_data.py")
    
    print("\n   Le fichier market_data.csv sera automatiquement créé!")
    print("\n" + "="*70 + "\n")

def main():
    """Fonction principale"""
    
    print("\n   CRÉATION DE TON FICHIER market_data.csv PERSONNALISÉ\n")
    
    # Demander confirmation
    print("   As-tu déjà rempli les données de la Banque Mondiale dans ce script?")
    print("   (Édite les valeurs dans le dictionnaire 'data' avant de continuer)")
    
    response = input("\n   Données remplies? (o/n): ").lower().strip()
    
    if response != 'o':
        show_instructions()
        print("👉 Remplis d'abord les données, puis relance ce script!\n")
        return
    
    # Créer le fichier
    df = create_market_data()
    
    # Vérification
    print("\n   VÉRIFICATION RAPIDE:")
    print(f"   • Nombre de pays: {len(df)}")
    print(f"   • PIB total: ${df['GDP_B_USD'].sum():.1f}B")
    print(f"   • Population totale: {df['Population_M'].sum():.1f}M")
    print(f"   • Banques totales: {df['Banks_Count'].sum()}")
    print(f"   • Assurances totales: {df['Insurance_Companies'].sum()}")
    
    print("\n   C'est tout! Tes données sont prêtes!   \n")

if __name__ == "__main__":
    main()