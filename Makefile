PYTHON      = python
SOURCES_FILE = xsd_sources.toml

.PHONY: help install-dev generate generate-all generate-from verify-xsd \
        docs docs-init docs-serve docs-copy clean-generated test build clean-dist release

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
	@echo "  docs-init            Initialise conf.py et index.rst si absents (1ère fois)"
	@echo "  docs-copy            Copie la doc de documentations/sphinxdoc/ vers docs/"
	@echo "  docs-serve           Lance un serveur local sur la documentation"
	@echo ""
	@echo "  test                 Lance les tests pytest"
	@echo "  build                Génère le package PyPI (dist/)"
	@echo "  clean-dist           Supprime les artefacts de build"
	@echo "  release              test + docs + build (prêt à publier)"
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

docs-init:
	@if [ ! -f docs/source/conf.py ]; then \
		sphinx-quickstart docs/source \
			--no-sep \
			--project onixlib \
			--author "Rémi Verschuur" \
			-v 0.1.0 \
			--release 0.1.0 \
			--language fr \
			--ext-autodoc \
			--quiet; \
		echo "  conf.py et index.rst générés dans docs/source/"; \
	else \
		echo "  docs/source/conf.py déjà présent — rien à faire."; \
	fi

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
# Tests
# ---------------------------------------------------------------------------

test:
	$(PYTHON) -m pytest

# ---------------------------------------------------------------------------
# Build PyPI
# ---------------------------------------------------------------------------

clean-dist:
	rm -rf dist/ build/ src/*.egg-info

build: clean-dist
	$(PYTHON) -m build
	@echo ""
	@echo "  Package généré dans dist/"

build-verify:
	$(PYTHON) -m twine check dist/*
	@echo ""
	@echo "  Vérification des artefacts de build : OK"

# ---------------------------------------------------------------------------
# Release (tests + doc + build)
# ---------------------------------------------------------------------------

release: test docs build
	@echo ""
	@echo "  Tests OK"
	@echo "  Documentation dans docs/build/html/"
	@echo "  Package dans dist/"
	@echo ""
	@echo "  Pour publier sur PyPI  : twine upload dist/*"
	@echo "  Pour taguer sur GitHub : git tag vX.Y.Z && git push origin main --tags"

# ---------------------------------------------------------------------------
# Publication sur PyPI
# ---------------------------------------------------------------------------

publish:
	@echo "AVERTISSEMENT : cette action publie le package sur PyPI."
	@read -p "Confirmer (oui/non) : " ans && [ "$$ans" = "oui" ] || { echo "Annulé."; exit 1; }
	twine upload dist/*
	@echo ""
	@echo "  Package publié sur PyPI. N'oubliez pas de taguer la release sur GitHub."
	@echo "  Exemple : git tag vX.Y.Z && git push origin main --tags"

# ---------------------------------------------------------------------------
# Nettoyage
# ---------------------------------------------------------------------------

clean-generated:
	@echo "ATTENTION : cette action supprime tous les modèles générés."
	@read -p "Confirmer (oui/non) : " ans && [ "$$ans" = "oui" ] || { echo "Annulé."; exit 1; }
	rm -rf src/onixlib/models/generated/
	@echo "Modèles supprimés. Relancer 'make generate-all' pour recréer."
