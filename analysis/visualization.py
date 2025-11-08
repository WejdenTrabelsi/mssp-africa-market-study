import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuration
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

class MSSPVisualizations:
    """Génère toutes les visualisations pour l'étude de marché"""
    
    def __init__(self):
        """Charge les données"""
        print("  Chargement des données pour visualisation...")
        self.market_data = pd.read_csv('../data/market_data.csv')
        self.regulations = pd.read_csv('../data/regulations.csv')
        self.competitors = pd.read_csv('../data/competitors.csv')
        
        try:
            self.ranking = pd.read_csv('../data/country_ranking.csv')
        except:
            print("   Exécutez d'abord market_analysis.py pour générer country_ranking.csv")
            self.ranking = None
        
        print("   Données chargées!\n")
    
    def plot_market_size_comparison(self):
        """Compare la taille des marchés (TAM)"""
        print("   Génération: Comparaison de la taille des marchés...")
        
        fig = go.Figure()
        
        countries = self.market_data['Country']
        print(self.market_data.columns)

        # Use IT_Market_M_USD as TAM
        fig.add_trace(go.Bar(
            name='TAM',
            x=countries,
            y=self.market_data['IT_Market_M_USD'],
            marker_color='lightblue'
        ))
        
        # Optional: remove SAM/SOM if not available, or set to 0
        fig.add_trace(go.Bar(
            name='SAM',
            x=countries,
            y=[0]*len(countries),  # placeholder
            marker_color='royalblue'
        ))
        
        fig.add_trace(go.Bar(
            name='SOM',
            x=countries,
            y=[0]*len(countries),  # placeholder
            marker_color='darkblue'
        ))
        
        fig.update_layout(
            title='Taille du Marché MSSP par Pays (M USD)',
            xaxis_title='Pays',
            yaxis_title='Taille du Marché (M USD)',
            barmode='group',
            template='plotly_white',
            height=500
        )
        
        fig.write_html('../images/charts/market_size_comparison.html')
        print("       Sauvegardé: market_size_comparison.html\n")
        
        return fig

    def plot_country_attractiveness(self):
        """Score d'attractivité des pays"""
        print("   Génération: Score d'attractivité des pays...")
        
        if self.ranking is not None:
            fig = px.bar(
                self.ranking,
                x='Country',
                y='Attractiveness_Score',
                color='Attractiveness_Score',
                title='Score d\'Attractivité des Pays pour les MSSP',
                labels={
                    'Attractiveness_Score': 'Score d\'Attractivité',
                    'Country': 'Pays'
                },
                color_continuous_scale='Viridis'
            )
            
            fig.update_layout(
                template='plotly_white',
                height=500
            )
            
            fig.write_html('../images/charts/country_attractiveness.html')
            print("   !! Sauvegardé: country_attractiveness.html\n")
            
            return fig
        else:
            print("      Skipped: country_ranking.csv non disponible\n")
            return None

    def plot_segment_revenue_potential(self):
        """Potentiel de revenu par segment"""
        print("   Génération: Potentiel de revenu par segment...")
        
        # Créer des données de démonstration pour les segments
        segments_data = []
        for _, row in self.market_data.iterrows():
            country = row['Country']
            # Estimation du potentiel par segment 
            segments_data.extend([
                {'Country': country, 'Segment': 'Banques', 'Revenue_Potential': row['Banks_Count'] * 0.1},
                {'Country': country, 'Segment': 'Assurances', 'Revenue_Potential': row['Insurance_Companies'] * 0.08},
                {'Country': country, 'Segment': 'PME', 'Revenue_Potential': row['SMEs_Count'] * 0.001}
            ])
        
        segments_df = pd.DataFrame(segments_data)
        
        fig = px.bar(
            segments_df,
            x='Country',
            y='Revenue_Potential',
            color='Segment',
            title='Potentiel de Revenu MSSP par Segment Client',
            labels={
                'Revenue_Potential': 'Potentiel de Revenu (M USD)',
                'Country': 'Pays',
                'Segment': 'Segment Client'
            },
            barmode='stack'
        )
        
        fig.update_layout(
            template='plotly_white',
            height=500
        )
        
        fig.write_html('../images/charts/segment_revenue_potential.html')
        print("       Sauvegardé: segment_revenue_potential.html\n")
        
        return fig

    def plot_competitive_landscape(self):
        """Paysage concurrentiel"""
        print("   Génération: Paysage concurrentiel...")
        
        # Scatter plot: Market Share vs Clients
        fig = px.scatter(
            self.competitors,
            x='Clients_Estimate',
            y='Market_Share_Pct',
            size='Market_Share_Pct',
            color='Pricing_Tier',
            hover_data=['Company', 'Services'],
            title='Positionnement Concurrentiel (Clients vs Part de Marché)',
            labels={
                'Clients_Estimate': 'Nombre de Clients Estimés',
                'Market_Share_Pct': 'Part de Marché (%)',
                'Pricing_Tier': 'Positionnement Prix'
            },
            color_discrete_map={
                'Premium': '#E74C3C',
                'Mid': '#F39C12',
                'Budget': '#3498DB'
            }
        )
        
        fig.update_layout(
            template='plotly_white',
            height=500
        )
        
        fig.write_html('../images/charts/competitive_landscape.html')
        print("       Sauvegardé: competitive_landscape.html\n")
        
        return fig

    def plot_regulatory_maturity(self):
        """Maturité réglementaire par pays"""
        print("   Génération: Maturité réglementaire...")
        
        reg_data = self.market_data.merge(
            self.regulations[['Country', 'Compliance_Maturity', 'Penalties_Max_USD']], 
            on='Country'
        )
        
        # Map maturity to numeric
        maturity_map = {
            'High': 3, 'Advanced': 3,
            'Medium': 2, 'Developing': 2,
            'Low': 1, 'Basic': 1
        }
        reg_data['Maturity_Numeric'] = reg_data['Compliance_Maturity'].map(maturity_map)
        
        fig = px.scatter(
            reg_data,
            x='Maturity_Numeric',
            y='IT_Market_M_USD',  
            size='Penalties_Max_USD',
            color='Country',
            hover_data=['Compliance_Maturity', 'Penalties_Max_USD'],
            title='Maturité Réglementaire vs Potentiel de Marché',
            labels={
                'Maturity_Numeric': 'Niveau de Maturité',
                'IT_Market_M_USD': 'Marché IT (M USD)',
                'Country': 'Pays'
            }
        )
        
        fig.update_xaxes(
            ticktext=['Faible', 'Moyen', 'Élevé'],
            tickvals=[1, 2, 3]
        )
        
        fig.update_layout(
            template='plotly_white',
            height=500
        )
        
        fig.write_html('../images/charts/regulatory_maturity.html')
        print("       Sauvegardé: regulatory_maturity.html\n")
        
        return fig

    def plot_internet_penetration_vs_spending(self):
        """Corrélation pénétration internet vs dépenses cyber"""
        print("   Génération: Internet vs Dépenses Cybersécurité...")
        
        fig = px.scatter(
            self.market_data,
            x='Internet_Penetration_Pct',
            y='Cybersecurity_Spending_M_USD',
            size='Population_M',
            color='Country',
            hover_data=['GDP_B_USD', 'Banks_Count'],
            title='Pénétration Internet vs Dépenses Cybersécurité',
            labels={
                'Internet_Penetration_Pct': 'Pénétration Internet (%)',
                'Cybersecurity_Spending_M_USD': 'Dépenses Cybersécurité (M USD)',
                'Population_M': 'Population (M)',
                'Country': 'Pays'
            },
            trendline='ols'
        )
        
        fig.update_layout(
            template='plotly_white',
            height=500
        )
        
        fig.write_html('../images/charts/internet_vs_spending.html')
        print("       Sauvegardé: internet_vs_spending.html\n")
        
        return fig

    def plot_dashboard_overview(self):
        """Tableau de bord récapitulatif"""
        print("  Génération: Dashboard récapitulatif complet...")
        
        # Créer subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Marché IT par Pays',
                'Dépenses Cybersécurité Actuelles',
                'Nombre d\'Institutions Financières',
                'Pénétration Internet'
            ),
            specs=[
                [{'type': 'bar'}, {'type': 'bar'}],
                [{'type': 'bar'}, {'type': 'bar'}]
            ]
        )
        
        countries = self.market_data['Country']
        
        # 1. Marché IT par pays
        fig.add_trace(
            go.Bar(x=countries, y=self.market_data['IT_Market_M_USD'], 
                   marker_color='royalblue', name='Marché IT'),
            row=1, col=1
        )
        
        # 2. Dépenses actuelles
        fig.add_trace(
            go.Bar(x=countries, y=self.market_data['Cybersecurity_Spending_M_USD'],
                   marker_color='coral', name='Dépenses Cyber'),
            row=1, col=2
        )
        
        # 3. Institutions financières
        fig.add_trace(
            go.Bar(x=countries, 
                   y=self.market_data['Banks_Count'] + self.market_data['Insurance_Companies'],
                   marker_color='mediumseagreen', name='Institutions Financières'),
            row=2, col=1
        )
        
        # 4. Pénétration Internet
        fig.add_trace(
            go.Bar(x=countries, y=self.market_data['Internet_Penetration_Pct'],
                   marker_color='mediumpurple', name='Pénétration Internet (%)'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            showlegend=False,
            title_text="Dashboard Récapitulatif - Marché MSSP Afrique Francophone",
            template='plotly_white'
        )
        
        fig.write_html('../images/charts/dashboard_overview.html')
        print("       Sauvegardé: dashboard_overview.html\n")
        
        return fig

    def generate_all_charts(self):
        """Génère tous les graphiques"""
        print("\n" + "  " * 35)
        print("   GÉNÉRATION DE TOUTES LES VISUALISATIONS")
        print("  " * 35 + "\n")
        
        self.plot_market_size_comparison()
        self.plot_country_attractiveness()
        self.plot_segment_revenue_potential()
        self.plot_competitive_landscape()
        self.plot_regulatory_maturity()
        self.plot_internet_penetration_vs_spending()
        self.plot_dashboard_overview()
        
        print("   Toutes les visualisations ont été générées!")
        print("   Emplacement: /images/charts/")
        print("\n   Vous pouvez ouvrir les fichiers .html dans votre navigateur")
        print("   ou les intégrer dans votre rapport PDF.\n")

def main():
    """Fonction principale"""
    viz = MSSPVisualizations()
    viz.generate_all_charts()

if __name__ == "__main__":
    main()