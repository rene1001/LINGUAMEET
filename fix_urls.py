#!/usr/bin/env python
"""
Script pour corriger les URLs dans les vues
"""

# Lire le fichier views.py
with open('conference/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer les redirections sans namespace
content = content.replace("return redirect('join_room'", "return redirect('conference:join_room'")
content = content.replace("return redirect('room'", "return redirect('conference:room'")
content = content.replace("return redirect('home'", "return redirect('conference:home'")

# Écrire le fichier corrigé
with open('conference/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ URLs corrigées dans conference/views.py") 