"""
Dempster-Shafer Theory of Belief Functions
Real Example: Autonomous Vehicle Obstacle Detection

Requirements:
pip install tkinter (usually comes with Python)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Set
import itertools


class DempsterShaferGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Théorie de Dempster-Shafer - Détection d'obstacles")
        self.root.geometry("900x700")
        
        # Frame of discernment
        self.frame_elements = ['Pedestrian', 'Cyclist', 'Vehicle', 'Animal']
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_scenario_tab()
        self.create_sensors_tab()
        self.create_belief_plausibility_tab()
        self.create_fusion_tab()
        self.create_theory_tab()
        
        # Initialize with example data
        self.load_example()
    
    def create_scenario_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Scénario")
        
        # Title
        title = tk.Label(tab, text="Détection d'obstacle - Véhicule autonome", 
                        font=('Arial', 16, 'bold'))
        title.pack(pady=20)
        
        # Description
        desc_frame = tk.Frame(tab, bg='lightblue', padx=20, pady=20)
        desc_frame.pack(fill='x', padx=20, pady=10)
        
        desc_text = """
Un véhicule autonome détecte un objet devant lui à 50 mètres.
Trois capteurs fournissent des informations:

🎥 CAMÉRA (Vision): Analyse visuelle de la forme
📡 LIDAR: Mesure précise de la distance et du profil 3D  
📶 RADAR: Détection de la vitesse et signature métallique

Objectif: Combiner les trois sources pour identifier l'obstacle
        """
        desc_label = tk.Label(desc_frame, text=desc_text, bg='lightblue',
                             font=('Arial', 10), justify='left')
        desc_label.pack()
        
        # Frame of discernment
        frame_label = tk.Label(tab, text="Cadre de discernement Θ:", 
                              font=('Arial', 12, 'bold'))
        frame_label.pack(pady=10)
        
        elements_frame = tk.Frame(tab)
        elements_frame.pack()
        
        colors = ['lightblue', 'lightgreen', 'plum', 'orange']
        for elem, color in zip(self.frame_elements, colors):
            elem_frame = tk.Frame(elements_frame, bg=color, padx=15, pady=10)
            elem_frame.pack(side='left', padx=5)
            tk.Label(elem_frame, text=elem, bg=color, font=('Arial', 10, 'bold')).pack()
    
    def create_sensors_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Données capteurs")
        
        # Camera section
        camera_frame = tk.LabelFrame(tab, text="🎥 CAMÉRA - Fonction de masse m₁",
                                     font=('Arial', 11, 'bold'), padx=10, pady=10)
        camera_frame.pack(fill='x', padx=20, pady=10)
        
        self.camera_text = tk.Text(camera_frame, height=6, width=80, font=('Courier', 9))
        self.camera_text.pack()
        
        # LIDAR section
        lidar_frame = tk.LabelFrame(tab, text="📡 LIDAR - Fonction de masse m₂",
                                    font=('Arial', 11, 'bold'), padx=10, pady=10)
        lidar_frame.pack(fill='x', padx=20, pady=10)
        
        self.lidar_text = tk.Text(lidar_frame, height=7, width=80, font=('Courier', 9))
        self.lidar_text.pack()
        
        # Radar section
        radar_frame = tk.LabelFrame(tab, text="📶 RADAR - Fonction de masse m₃",
                                    font=('Arial', 11, 'bold'), padx=10, pady=10)
        radar_frame.pack(fill='x', padx=20, pady=10)
        
        self.radar_text = tk.Text(radar_frame, height=5, width=80, font=('Courier', 9))
        self.radar_text.pack()
    
    def create_belief_plausibility_tab(self):
        """Create tab for Belief and Plausibility display"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Belief & Plausibility")
        
        # Title and info
        title = tk.Label(tab, text="Calcul de Belief et Plausibility", 
                        font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        info_frame = tk.Frame(tab, bg='lightyellow', padx=15, pady=10)
        info_frame.pack(fill='x', padx=20, pady=5)
        info_text = "Bel(A) = support minimum | Pl(A) = support maximum | Intervalle: [Bel(A), Pl(A)]"
        tk.Label(info_frame, text=info_text, bg='lightyellow', font=('Arial', 9)).pack()
        
        # AVANT FUSION
        avant_label = tk.Label(tab, text="📊 AVANT FUSION (Sources individuelles)", 
                              font=('Arial', 12, 'bold'), fg='blue')
        avant_label.pack(pady=(10, 5))
        
        avant_frame = tk.LabelFrame(tab, text="Valeurs Bel et Pl pour chaque capteur",
                                    font=('Arial', 10, 'bold'), padx=10, pady=10)
        avant_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        self.belief_avant_text = tk.Text(avant_frame, height=12, width=85, font=('Courier', 9))
        self.belief_avant_text.pack(fill='both', expand=True)
        
        # Add scrollbar
        scrollbar1 = ttk.Scrollbar(avant_frame, command=self.belief_avant_text.yview)
        scrollbar1.pack(side='right', fill='y')
        self.belief_avant_text.config(yscrollcommand=scrollbar1.set)
        
        # Separator
        ttk.Separator(tab, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # APRÈS FUSION
        apres_label = tk.Label(tab, text="🎯 APRÈS FUSION (Résultat combiné)", 
                              font=('Arial', 12, 'bold'), fg='green')
        apres_label.pack(pady=(5, 5))
        
        apres_frame = tk.LabelFrame(tab, text="Valeurs Bel et Pl après fusion complète",
                                    font=('Arial', 10, 'bold'), padx=10, pady=10, bg='lightgreen')
        apres_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        self.belief_apres_text = tk.Text(apres_frame, height=8, width=85, font=('Courier', 10, 'bold'))
        self.belief_apres_text.pack(fill='both', expand=True)
        
        # Add scrollbar
        scrollbar2 = ttk.Scrollbar(apres_frame, command=self.belief_apres_text.yview)
        scrollbar2.pack(side='right', fill='y')
        self.belief_apres_text.config(yscrollcommand=scrollbar2.set)
    
    def create_fusion_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Fusion & Résultats")
        
        # Calculate button
        calc_btn = tk.Button(tab, text="🔄 Calculer la fusion", 
                            command=self.calculate_fusion,
                            font=('Arial', 12, 'bold'), bg='lightgreen', padx=20, pady=10)
        calc_btn.pack(pady=20)
        
        # Step 1
        step1_frame = tk.LabelFrame(tab, text="Étape 1: Caméra ⊕ LIDAR",
                                    font=('Arial', 11, 'bold'), padx=10, pady=10)
        step1_frame.pack(fill='x', padx=20, pady=10)
        
        self.step1_text = tk.Text(step1_frame, height=8, width=80, font=('Courier', 9))
        self.step1_text.pack()
        
        # Step 2 (Final)
        step2_frame = tk.LabelFrame(tab, text="Étape 2: (Caméra ⊕ LIDAR) ⊕ Radar - RÉSULTAT FINAL",
                                    font=('Arial', 11, 'bold'), padx=10, pady=10, bg='lightgreen')
        step2_frame.pack(fill='x', padx=20, pady=10)
        
        self.step2_text = tk.Text(step2_frame, height=10, width=80, font=('Courier', 10, 'bold'))
        self.step2_text.pack()
        
        # Decision
        decision_frame = tk.Frame(tab, bg='lightyellow', padx=20, pady=15)
        decision_frame.pack(fill='x', padx=20, pady=10)
        
        self.decision_text = tk.Label(decision_frame, text="", bg='lightyellow',
                                     font=('Arial', 11, 'bold'), justify='left')
        self.decision_text.pack()
    
    def create_theory_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Théorie")
        
        theory_text = """
═══════════════════════════════════════════════════════════════════

RÈGLE DE COMBINAISON DE DEMPSTER
═══════════════════════════════════════════════════════════════════

Pour deux fonctions de masse m₁ et m₂:

    m₁₂(A) = [Σ m₁(B)·m₂(C)] / (1 - K)
             où B∩C = A

Conflit K (mesure du désaccord):

    K = Σ m₁(B)·m₂(C)
        où B∩C = ∅

═══════════════════════════════════════════════════════════════════

BELIEF ET PLAUSIBILITY
═══════════════════════════════════════════════════════════════════

Belief (Croyance) - Support minimum:
    Bel(A) = Σ m(B) pour tout B ⊆ A

Plausibility (Plausibilité) - Support maximum:
    Pl(A) = Σ m(B) pour tout B ∩ A ≠ ∅

Intervalle d'incertitude: [Bel(A), Pl(A)]

═══════════════════════════════════════════════════════════════════

PROBABILITÉ PIGNISTIQUE
═══════════════════════════════════════════════════════════════════

Transformation en probabilité classique pour décision:

    BetP(x) = Σ [m(A) / |A|] pour tout A contenant x

La masse d'un ensemble est distribuée équitablement entre ses éléments.

═══════════════════════════════════════════════════════════════════

AVANTAGES DE LA THÉORIE DS
═══════════════════════════════════════════════════════════════════

✓ Représentation explicite de l'ignorance
✓ Fusion de sources hétérogènes
✓ Détection du conflit entre sources
✓ Intervalles d'incertitude riches
✓ Pas besoin de probabilités a priori

═══════════════════════════════════════════════════════════════════
        """
        
        text_widget = tk.Text(tab, wrap='word', font=('Courier', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert('1.0', theory_text)
        text_widget.config(state='disabled')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tab, command=text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        text_widget.config(yscrollcommand=scrollbar.set)
    
    def load_example(self):
        """Load example sensor data"""
        self.camera_data = {
            frozenset(['Pedestrian']): 0.65,
            frozenset(['Cyclist']): 0.15,
            frozenset(['Pedestrian', 'Cyclist']): 0.20
        }
        
        self.lidar_data = {
            frozenset(['Pedestrian']): 0.50,
            frozenset(['Vehicle']): 0.10,
            frozenset(['Pedestrian', 'Cyclist']): 0.30,
            frozenset(self.frame_elements): 0.10
        }
        
        self.radar_data = {
            frozenset(['Pedestrian']): 0.60,
            frozenset(['Cyclist']): 0.25,
            frozenset(['Cyclist', 'Vehicle']): 0.15
        }
        
        self.display_sensor_data()
        self.calculate_belief_plausibility_avant()
    
    def display_sensor_data(self):
        """Display sensor data in text widgets"""
        # Camera
        self.camera_text.delete('1.0', tk.END)
        self.camera_text.insert('1.0', self.format_mass_function(self.camera_data, "CAMÉRA"))
        
        # LIDAR
        self.lidar_text.delete('1.0', tk.END)
        self.lidar_text.insert('1.0', self.format_mass_function(self.lidar_data, "LIDAR"))
        
        # Radar
        self.radar_text.delete('1.0', tk.END)
        self.radar_text.insert('1.0', self.format_mass_function(self.radar_data, "RADAR"))
    
    def format_mass_function(self, mass_func: Dict, sensor_name: str) -> str:
        """Format mass function for display"""
        result = f"{'Hypothèse':<30} | Masse  | Interprétation\n"
        result += "-" * 80 + "\n"
        
        interpretations = {
            ('CAMÉRA', frozenset(['Pedestrian'])): "Forte confiance - forme humaine",
            ('CAMÉRA', frozenset(['Cyclist'])): "Faible probabilité",
            ('CAMÉRA', frozenset(['Pedestrian', 'Cyclist'])): "Incertitude entre les deux",
            ('LIDAR', frozenset(['Pedestrian'])): "Profil compatible avec piéton",
            ('LIDAR', frozenset(['Vehicle'])): "Faible masse - peu probable",
            ('LIDAR', frozenset(['Pedestrian', 'Cyclist'])): "Taille similaire",
            ('LIDAR', frozenset(self.frame_elements)): "Ignorance totale (Θ)",
            ('RADAR', frozenset(['Vehicle'])): "Forte réflexion métallique",
            ('RADAR', frozenset(['Cyclist'])): "Réflexion partielle (vélo)",
            ('RADAR', frozenset(['Cyclist', 'Vehicle'])): "Incertitude sur taille",
        }
        
        for focal, mass in sorted(mass_func.items(), key=lambda x: -x[1]):
            focal_str = '{' + ', '.join(sorted(focal)) + '}'
            interp = interpretations.get((sensor_name, focal), "")
            result += f"{focal_str:<30} | {mass:.2f}  | {interp}\n"
        
        return result
    
    def dempster_combination(self, m1: Dict, m2: Dict) -> tuple:
        """Combine two mass functions using Dempster's rule"""
        combined = {}
        conflict = 0.0
        
        for focal1, mass1 in m1.items():
            for focal2, mass2 in m2.items():
                intersection = focal1 & focal2
                
                if len(intersection) == 0:  # Empty set
                    conflict += mass1 * mass2
                else:
                    if intersection not in combined:
                        combined[intersection] = 0.0
                    combined[intersection] += mass1 * mass2
        
        # Normalize
        normalizer = 1 - conflict
        if normalizer > 0:
            normalized = {k: v / normalizer for k, v in combined.items()}
        else:
            normalized = combined
        
        return normalized, conflict
    
    def calculate_belief(self, mass_func: Dict, hypothesis: frozenset) -> float:
        """Calculate belief for a hypothesis"""
        belief = 0.0
        for focal, mass in mass_func.items():
            if focal.issubset(hypothesis):
                belief += mass
        return belief
    
    def calculate_plausibility(self, mass_func: Dict, hypothesis: frozenset) -> float:
        """Calculate plausibility for a hypothesis"""
        plausibility = 0.0
        for focal, mass in mass_func.items():
            if len(focal & hypothesis) > 0:
                plausibility += mass
        return plausibility
    
    def format_belief_plausibility(self, mass_func: Dict, source_name: str) -> str:
        """Format belief and plausibility for display"""
        result = f"\n{'='*70}\n"
        result += f"  {source_name}\n"
        result += f"{'='*70}\n"
        result += f"{'Hypothèse':<20} | {'Bel(A)':<10} | {'Pl(A)':<10} | Intervalle\n"
        result += "-" * 70 + "\n"
        
        for elem in self.frame_elements:
            hypothesis = frozenset([elem])
            bel = self.calculate_belief(mass_func, hypothesis)
            pl = self.calculate_plausibility(mass_func, hypothesis)
            result += f"{elem:<20} | {bel:>8.4f}   | {pl:>8.4f}   | [{bel:.4f}, {pl:.4f}]\n"
        
        return result
    
    def calculate_belief_plausibility_avant(self):
        """Calculate and display Belief and Plausibility before fusion"""
        self.belief_avant_text.delete('1.0', tk.END)
        
        result = "CALCUL DES VALEURS Bel ET Pl POUR CHAQUE CAPTEUR (AVANT FUSION)\n"
        result += "="*70 + "\n"
        
        # Camera
        result += self.format_belief_plausibility(self.camera_data, "🎥 CAMÉRA")
        
        # LIDAR
        result += self.format_belief_plausibility(self.lidar_data, "📡 LIDAR")
        
        # Radar
        result += self.format_belief_plausibility(self.radar_data, "📶 RADAR")
        
        self.belief_avant_text.insert('1.0', result)
    
    def calculate_belief_plausibility_apres(self, final_mass: Dict):
        """Calculate and display Belief and Plausibility after fusion"""
        self.belief_apres_text.delete('1.0', tk.END)
        
        result = "CALCUL DES VALEURS Bel ET Pl APRÈS FUSION COMPLÈTE\n"
        result += "="*70 + "\n"
        result += "(Caméra ⊕ LIDAR ⊕ Radar)\n"
        
        result += self.format_belief_plausibility(final_mass, "🎯 RÉSULTAT FINAL")
        
        # Add interpretation
        result += "\n" + "="*70 + "\n"
        result += "INTERPRÉTATION:\n"
        result += "-"*70 + "\n"
        
        for elem in self.frame_elements:
            hypothesis = frozenset([elem])
            bel = self.calculate_belief(final_mass, hypothesis)
            pl = self.calculate_plausibility(final_mass, hypothesis)
            width = pl - bel
            
            result += f"\n{elem}:\n"
            result += f"  • Certitude minimale (Bel): {bel*100:.2f}%\n"
            result += f"  • Certitude maximale (Pl):  {pl*100:.2f}%\n"
            result += f"  • Largeur d'intervalle:     {width*100:.2f}%\n"
            
            if width < 0.1:
                result += f"  → Très faible incertitude\n"
            elif width < 0.3:
                result += f"  → Incertitude modérée\n"
            else:
                result += f"  → Forte incertitude\n"
        
        self.belief_apres_text.insert('1.0', result)
    
    def calculate_fusion(self):
        """Perform fusion calculation"""
        try:
            # Step 1: Camera ⊕ LIDAR
            step1_combined, step1_conflict = self.dempster_combination(
                self.camera_data, self.lidar_data
            )
            
            # Display step 1
            self.step1_text.delete('1.0', tk.END)
            result1 = "Masse combinée (Caméra ⊕ LIDAR):\n"
            result1 += "-" * 60 + "\n"
            for focal, mass in sorted(step1_combined.items(), key=lambda x: -x[1]):
                focal_str = '{' + ', '.join(sorted(focal)) + '}'
                result1 += f"{focal_str:<40} | {mass:.4f}\n"
            result1 += "\n" + "=" * 60 + "\n"
            result1 += f"Conflit K₁ = {step1_conflict:.4f} ({step1_conflict*100:.2f}%)\n"
            self.step1_text.insert('1.0', result1)
            
            # Step 2: (Camera ⊕ LIDAR) ⊕ Radar
            final_combined, final_conflict = self.dempster_combination(
                step1_combined, self.radar_data
            )
            
            # Display step 2
            self.step2_text.delete('1.0', tk.END)
            result2 = "MASSE FINALE (Caméra ⊕ LIDAR ⊕ Radar):\n"
            result2 += "=" * 60 + "\n"
            for focal, mass in sorted(final_combined.items(), key=lambda x: -x[1]):
                focal_str = '{' + ', '.join(sorted(focal)) + '}'
                result2 += f"{focal_str:<40} | {mass:.4f}\n"
            
            result2 += "\n" + "=" * 60 + "\n"
            result2 += f"Conflit total K₂ = {final_conflict:.4f} ({final_conflict*100:.2f}%)\n"
            result2 += "\n" + "=" * 60 + "\n"
            
            self.step2_text.insert('1.0', result2)
            
            # Calculate and display Belief and Plausibility AFTER fusion
            self.calculate_belief_plausibility_apres(final_combined)
            
            # Display decision
            best_hypothesis = max(final_combined.items(), key=lambda x: x[1])
            decision_msg = f"🎯 DÉCISION: L'obstacle est un {', '.join(sorted(best_hypothesis[0]))}\n"
            decision_msg += f"   Confiance: {best_hypothesis[1]*100:.1f}%\n\n"
            
            if any(elem in best_hypothesis[0] for elem in ['Pedestrian', 'Cyclist']):
                decision_msg += "⚠️  ACTION: FREINAGE D'URGENCE ET ARRÊT COMPLET"
            else:
                decision_msg += "⚠️  ACTION: RALENTISSEMENT ET CONTOURNEMENT"
            
            self.decision_text.config(text=decision_msg)
            
            messagebox.showinfo("Calcul terminé", 
                              f"Fusion complétée!\nMeilleure hypothèse: {', '.join(sorted(best_hypothesis[0]))} ({best_hypothesis[1]*100:.1f}%)")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du calcul:\n{str(e)}")


def main():
    root = tk.Tk()
    app = DempsterShaferGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()