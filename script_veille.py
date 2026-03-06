import google.generativeai as genai
import os
from datetime import datetime

# 1. Configuration de l'IA
# La clé est récupérée automatiquement depuis les secrets GitHub
api_key = os.environ.get("GEMINI_OSI")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Vos sources (Exemples basés sur vos documents)
sources_context = """
- Reuters & Le Monde : Suivi des régulations IA et procès Grok en France.
- LinkedIn & X : Tendance sur les agents autonomes et le "Vibe Coding".
- HuggingFace : Sorties des modèles 
- Marché : Acquisitions par NVIDIA, Alphabet et Meta (Infrastructure).
"""

# 3. Le Prompt "Vibe Coding"
# On demande à Gemini de générer directement le contenu HTML final
prompt = f"""
Tu es un expert en veille stratégique IA . 
Analyse ces thématiques : {sources_context}

Génère UNIQUEMENT le code HTML contenu à l'intérieur de la balise <main> pour un tableau de bord.
Utilise le style Tailwind CSS suivant :
- 3 colonnes (Gouvernance, Marché, Tech).
- Des cartes avec la classe "neo-card" (bordure noire 2px, ombre portée).
- Utilise des emojis et des titres percutants.
- Ajoute la date du jour ({datetime.now().strftime('%d/%m/%Y')}) discrètement.

Ne mets pas de balises ```html ou d'explications, juste le code HTML brut.
"""

def main():
    try:
        # Génération du contenu via Gemini
        response = model.generate_content(prompt)
        new_content = response.text

        # Lecture du template de base (ou reconstruction du fichier complet)
        full_html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Veille IA </title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <style>
        .neo-card {{ border: 2px solid #000; box-shadow: 5px 5px 0px #000; transition: all 0.2s; }}
        .neo-card:hover {{ transform: translate(-2px, -2px); box-shadow: 7px 7px 0px #000; }}
    </style>
</head>
<body class="bg-gray-50 text-gray-900 p-6">
    <header class="max-w-6xl mx-auto mb-12">
        <h1 class="text-4xl font-black uppercase tracking-tighter border-b-4 border-black inline-block mb-4">🤖 Veille IA 2026</h1>
        <p class="text-lg text-gray-600">Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y')}</p>
    </header>

    <main class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
        {new_content}
    </main>
</body>
</html>
"""
        
        # Écriture du fichier final
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("✅ index.html a été mis à jour avec succès !")

    except Exception as e:
        print(f"❌ Erreur lors de la génération : {e}")

if __name__ == "__main__":
    main()