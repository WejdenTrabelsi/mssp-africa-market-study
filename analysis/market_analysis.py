import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuration de style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class MSSPMarketAnalysis:
    """Analyse complète du marché MSSP en Afrique Francophone"""
    
    def __init__(self):
        """Initialise l'analyse avec chargement des données"""
        print("  Chargement des données...")
        self.market_data = pd.read_csv('../data/market_data.csv')
        self.regulations = pd.read_csv('../data/regulations.csv')
        self.competitors = pd.read_csv('../data/competitors.csv')
        
        # Calculs dérivés
        self._calculate_derived_metrics()
        print("   Données chargées avec succès!\n")
    
    def _calculate_derived_metrics(self):
        """Calcule les métriques dérivées importantes"""
        # TAM (Total Addressable Market)
        self.market_data['TAM_M_USD'] = (
            self.market_data['Banks_Count'] * 50000 +  # 50k USD/an par banque
            self.market_data['Insurance_Companies'] * 30000 +  # 30k USD/an par assurance
            self.market_data['SMEs_Count'] * 0.02 * 5000  # 2% des PME × 5k USD/an
        ) / 1000000  # Conversion en millions
        
        # SAM (Serviceable Addressable Market) - 40% du TAM
        self.market_data['SAM_M_USD'] = self.market_data['TAM_M_USD'] * 0.4
        
        # SOM (Serviceable Obtainable Market) - 15% du SAM
        self.market_data['SOM_M_USD'] = self.market_data['SAM_M_USD'] * 0.15
        
        # Potential revenue per capita
        self.market_data['Revenue_Per_Capita'] = (
            self.market_data['Cybersecurity_Spending_M_USD'] / 
            self.market_data['Population_M']
        )
        
        # Growth potential score (0-100)
        self.market_data['Growth_Score'] = (
            (self.market_data['Internet_Penetration_Pct'] * 0.3) +
            (self.market_data['Mobile_Penetration_Pct'] * 0.2) +
            (self.market_data['Revenue_Per_Capita'] * 10) +
            (self.market_data['Banks_Count'] * 0.5)
        )
    
    def market_overview(self):
        """Affiche un aperçu général du marché"""
        print("=" * 70)
        print(" APERÇU GÉNÉRAL DU MARCHÉ MSSP - AFRIQUE FRANCOPHONE")
        print("=" * 70)
        
        total_population = self.market_data['Population_M'].sum()
        total_gdp = self.market_data['GDP_B_USD'].sum()
        total_cyber_spending = self.market_data['Cybersecurity_Spending_M_USD'].sum()
        total_tam = self.market_data['TAM_M_USD'].sum()
        total_sam = self.market_data['SAM_M_USD'].sum()
        total_som = self.market_data['SOM_M_USD'].sum()
        
        print(f"\n   Métriques Clés:")
        print(f"   • Population totale: {total_population:.1f}M habitants")
        print(f"   • PIB combiné: ${total_gdp:.1f}B USD")
        print(f"   • Dépenses cybersécurité actuelles: ${total_cyber_spending:.1f}M USD")
        print(f"\n   Taille du Marché (Market Sizing):")
        print(f"   • TAM (Total Addressable Market): ${total_tam:.1f}M USD")
        print(f"   • SAM (Serviceable Addressable Market): ${total_sam:.1f}M USD")
        print(f"   • SOM (Serviceable Obtainable Market): ${total_som:.1f}M USD")
        
        # Top 3 marchés
        print(f"\n  Top 3 Marchés par Potentiel:")
        top_markets = self.market_data.nlargest(3, 'SAM_M_USD')[['Country', 'SAM_M_USD', 'Growth_Score']]
        for idx, row in top_markets.iterrows():
            print(f"   {idx+1}. {row['Country']}: ${row['SAM_M_USD']:.1f}M (Score: {row['Growth_Score']:.0f}/100)")
        
        print("\n" + "=" * 70 + "\n")
    
    def segment_analysis(self):
        """Analyse par segment de clients"""
        print("=" * 70)
        print("   ANALYSE PAR SEGMENT DE CLIENTS")
        print("=" * 70)
        
        # Calcul du potentiel par segment
        segments = pd.DataFrame({
            'Segment': ['Banques', 'Assurances', 'PME'],
            'Total_Clients': [
                self.market_data['Banks_Count'].sum(),
                self.market_data['Insurance_Companies'].sum(),
                (self.market_data['SMEs_Count'].sum() * 0.02)  # 2% des PME adressables
            ],
            'ARPU_USD': [50000, 30000, 5000],  # Average Revenue Per User
        })
        
        segments['Revenue_Potential_M_USD'] = (
            segments['Total_Clients'] * segments['ARPU_USD'] / 1000000
        )
        segments['Market_Share_Pct'] = (
            segments['Revenue_Potential_M_USD'] / segments['Revenue_Potential_M_USD'].sum() * 100
        )
        
        print("\n  Potentiel par Segment:")
        for idx, row in segments.iterrows():
            print(f"\n   {row['Segment']}:")
            print(f"      • Clients adressables: {row['Total_Clients']:.0f}")
            print(f"      • ARPU moyen: ${row['ARPU_USD']:,.0f}/an")
            print(f"      • Revenu potentiel: ${row['Revenue_Potential_M_USD']:.1f}M")
            print(f"      • Part du marché: {row['Market_Share_Pct']:.1f}%")
        
        print("\n   Recommandation Stratégique:")
        top_segment = segments.loc[segments['Revenue_Potential_M_USD'].idxmax(), 'Segment']
        print(f"   Prioriser le segment '{top_segment}' pour un déploiement initial.")
        print("\n" + "=" * 70 + "\n")
        
        return segments
    
    def regulatory_landscape(self):
        """Analyse du paysage réglementaire"""
        print("=" * 70)
        print("   PAYSAGE RÉGLEMENTAIRE")
        print("=" * 70)
        
        # Merge avec données de marché
        reg_analysis = self.market_data.merge(
            self.regulations, 
            on='Country'
        )[['Country', 'Compliance_Maturity', 'Cybersecurity_Framework', 
           'Penalties_Max_USD', 'SAM_M_USD']]
        
        print("\n   Maturité Réglementaire par Pays:")
        for idx, row in reg_analysis.iterrows():
            print(f"\n   {row['Country']}:")
            print(f"      • Maturité: {row['Compliance_Maturity']}")
            print(f"      • Framework: {row['Cybersecurity_Framework']}")
            print(f"      • Pénalités max: ${row['Penalties_Max_USD']:,.0f}")
            print(f"      • Potentiel marché: ${row['SAM_M_USD']:.1f}M")
        
        print("\n   Insight Réglementaire:")
        high_maturity = reg_analysis[reg_analysis['Compliance_Maturity'] == 'High']['Country'].tolist()
        print(f"   Marchés à haute maturité (meilleure sensibilisation): {', '.join(high_maturity)}")
        print("   → Clients plus enclins à investir dans la cybersécurité")
        
        print("\n" + "=" * 70 + "\n")
    
    def competitive_analysis(self):
        """Analyse concurrentielle"""
        print("=" * 70)
        print("   ANALYSE CONCURRENTIELLE")
        print("=" * 70)
        
        total_market_share = self.competitors['Market_Share_Pct'].sum()
        market_concentration = self.competitors.nlargest(3, 'Market_Share_Pct')['Market_Share_Pct'].sum()
        
        print(f"\n  Structure du Marché:")
        print(f"   • Part de marché couverte: {total_market_share:.0f}%")
        print(f"   • Concentration (Top 3): {market_concentration:.0f}%")
        print(f"   • Nombre d'acteurs: {len(self.competitors)}")
        
        print(f"\n Top 5 Concurrents:")
        top_competitors = self.competitors.nlargest(5, 'Market_Share_Pct')
        for idx, row in top_competitors.iterrows():
            print(f"   {idx+1}. {row['Company']} ({row['Country']})")
            print(f"      • Services: {row['Services']}")
            print(f"      • Part de marché: {row['Market_Share_Pct']:.0f}%")
            print(f"      • Clients estimés: ~{row['Clients_Estimate']}")
            print(f"      • Positionnement prix: {row['Pricing_Tier']}")
        
        print("\n   Opportunité Stratégique:")
        uncovered_market = 100 - total_market_share
        print(f"   {uncovered_market:.0f}% du marché reste non couvert par les acteurs majeurs")
        print("   → Opportunité pour un nouvel entrant avec une proposition différenciée")
        
        print("\n" + "=" * 70 + "\n")
    
    def country_ranking(self):
        """Classement des pays par attractivité"""
        print("=" * 70)
        print("  CLASSEMENT DES PAYS PAR ATTRACTIVITÉ")
        print("=" * 70)
        
        # Créer un score composite
        ranking = self.market_data.copy()
        ranking = ranking.merge(self.regulations[['Country', 'Compliance_Maturity']], on='Country')
        
        # Système de scoring
        maturity_score = {'High': 10, 'Medium': 7, 'Low': 4, 'Basic': 4, 'Developing': 7, 'Advanced': 10}
        ranking['Maturity_Score'] = ranking['Compliance_Maturity'].map(maturity_score)
        
        # Score final (0-100)
        ranking['Attractiveness_Score'] = (
            (ranking['SAM_M_USD'] / ranking['SAM_M_USD'].max() * 30) +  # 30% poids marché
            (ranking['Growth_Score'] / ranking['Growth_Score'].max() * 30) +  # 30% poids croissance
            (ranking['Maturity_Score'] / 10 * 20) +  # 20% poids maturité
            (ranking['Internet_Penetration_Pct'] / 100 * 20)  # 20% poids connectivité
        )
        
        ranking_sorted = ranking.sort_values('Attractiveness_Score', ascending=False)
        
        print("\n Classement Final:")
        for idx, (i, row) in enumerate(ranking_sorted.iterrows(), 1):
            print(f"\n   {idx}. {row['Country']} - Score: {row['Attractiveness_Score']:.1f}/100")
            print(f"      • Marché potentiel (SAM): ${row['SAM_M_USD']:.1f}M")
            print(f"      • Maturité réglementaire: {row['Compliance_Maturity']}")
            print(f"      • Pénétration internet: {row['Internet_Penetration_Pct']:.1f}%")
            print(f"      • Banques: {row['Banks_Count']} | Assurances: {row['Insurance_Companies']}")
        
        print("\n   Recommandation de Déploiement:")
        top_3 = ranking_sorted.head(3)['Country'].tolist()
        print(f"   Phase 1 (0-12 mois): {top_3[0]}")
        print(f"   Phase 2 (12-24 mois): {top_3[1]}")
        print(f"   Phase 3 (24-36 mois): {top_3[2]}")
        
        print("\n" + "=" * 70 + "\n")
        
        return ranking_sorted
    
    def export_insights_to_csv(self, ranking_df):
        """Export les insights pour Power BI"""
        print("   Export des données pour Power BI...")
        
        # Export ranking
        ranking_df.to_csv('../data/country_ranking.csv', index=False)
        
        # Export segment analysis
        segments = self.segment_analysis()
        segments.to_csv('../data/segment_analysis.csv', index=False)
        
        print("   Fichiers exportés dans /data/")
        print("   • country_ranking.csv")
        print("   • segment_analysis.csv\n")

def main():
    """Fonction principale"""
    print("\n" + "  " * 35)
    print("   ANALYSE DE MARCHÉ MSSP - AFRIQUE FRANCOPHONE")
    print("  " * 35 + "\n")
    
    # Initialiser l'analyse
    analysis = MSSPMarketAnalysis()
    
    # Exécuter toutes les analyses
    analysis.market_overview()
    input("Appuyer sur Entrée pour continuer...")
    
    analysis.segment_analysis()
    input("Appuyer sur Entrée pour continuer...")
    
    analysis.regulatory_landscape()
    input("Appuyer sur Entrée pour continuer...")
    
    analysis.competitive_analysis()
    input("Appuyer sur Entrée pour continuer...")
    
    ranking = analysis.country_ranking()
    
    # Export pour Power BI
    analysis.export_insights_to_csv(ranking)
    
    print("   Analyse terminée avec succès!   \n")
    print("  Prochaine étape: Ouvrir Power BI et créer les visualisations")

if __name__ == "__main__":
    main()