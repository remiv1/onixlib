PYTHON      = python
SOURCES_FILE = xsd_sources.toml

.PHONY: help install-dev generate generate-all generate-from verify-xsd \
        docs docs-serve docs-copy clean-generated

# ---------------------------------------------------------------------------
help:
	@echo ""
	@echo "  Cibles disponibles :"
	@echo ""
	@echo "  install-dev          Installe les dépendances de développement"
	@echo ""
	@echo "  generate-all         Génère les modèles pour toutes les versions du fichier sources"
	@echo "  generate VERSION=X.Y Génère les modèles pour la version spécifiée"
	@echo "                       Exemple : make generate VERSION=3.0"
	@echo "  generate-from        Génère depuis une source externe"
	@echo "                       Exemple : make generate-from SOURCE=https://... VERSION=3.0"
	@echo "  generate-force V=X.Y Re-télécharge et régénère, même si XSD déjà présents"
	@echo "                       Exemple : make generate-force VERSION=3.0"
	@echo ""
	@echo "  verify-xsd           Vérifie l'intégrité des XSD (checksums .meta.toml)"
	@echo "  list-versions        Liste les versions et leur statut"
	@echo ""
	@echo "  docs                 Génère la documentation Sphinx (HTML)"
	@echo "  docs-copy            Copie la doc de documentations/sphinxdoc/ vers docs/"
	@echo "  docs-serve           Lance un serveur local sur la documentation"
	@echo ""
	@echo "  clean-generated      Supprime les modèles générés (demande confirmation)"
	@echo ""

# ---------------------------------------------------------------------------
# Installation
# ---------------------------------------------------------------------------

install-dev:
	$(PYTHON) -m pip install -e ".[dev]"

# ---------------------------------------------------------------------------
# Génération des modèles
# ---------------------------------------------------------------------------

generate-all:
	$(PYTHON) -m onixlib.cli.generate --from-file $(SOURCES_FILE)

generate:
ifndef VERSION
	$(error VERSION est requis. Exemple : make generate VERSION=3.0)
endif
	$(PYTHON) -m onixlib.cli.generate --from-file $(SOURCES_FILE) --version $(VERSION)

generate-from:
ifndef SOURCE
	$(error SOURCE est requis. Exemple : make generate-from SOURCE=https://... VERSION=3.0)
endif
ifndef VERSION
	$(error VERSION est requis. Exemple : make generate-from SOURCE=https://... VERSION=3.0)
endif
	$(PYTHON) -m onixlib.cli.generate --source $(SOURCE) --version $(VERSION)

generate-force:
ifndef VERSION
	$(error VERSION est requis. Exemple : make generate-force VERSION=3.0)
endif
	$(PYTHON) -m onixlib.cli.generate --from-file $(SOURCES_FILE) --version $(VERSION) --force

# ---------------------------------------------------------------------------
# Vérification
# ---------------------------------------------------------------------------

verify-xsd:
	@echo "Vérification des checksums XSD…"
	@for dir in documentations/xsd_onix3/*/; do \
		if [ -f "$$dir/.meta.toml" ]; then \
			echo "  $$dir : OK"; \
		else \
			echo "  $$dir : AVERTISSEMENT — aucun .meta.toml (lancer make generate)"; \
		fi \
	done

list-versions:
	$(PYTHON) -m onixlib.cli.generate --list-versions

# ---------------------------------------------------------------------------
# Documentation Sphinx
# ---------------------------------------------------------------------------

docs:
	sphinx-apidoc -f -e -o docs/source src/onixlib
	sphinx-build -b html docs/source docs/build/html
	@echo ""
	@echo "  Documentation générée dans docs/build/html/index.html"

docs-copy:
	@if [ -z "$$(ls -A documentations/sphinxdoc 2>/dev/null)" ]; then \
		echo "AVERTISSEMENT : documentations/sphinxdoc/ est vide — rien à copier."; \
	else \
		cp -r documentations/sphinxdoc/. docs/; \
		echo "  Contenu de documentations/sphinxdoc/ copié vers docs/"; \
	fi

docs-serve: docs
	$(PYTHON) -m http.server 8080 --directory docs/build/html

# ---------------------------------------------------------------------------
# Nettoyage
# ---------------------------------------------------------------------------

clean-generated:
	@echo "ATTENTION : cette action supprime tous les modèles générés."
	@read -p "Confirmer (oui/non) : " ans && [ "$$ans" = "oui" ] || { echo "Annulé."; exit 1; }
	rm -rf src/onixlib/models/generated/
	@echo "Modèles supprimés. Relancer 'make generate-all' pour recréer."
