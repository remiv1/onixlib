# Onixlib

![Logo onixlib](https://www.audit-io.fr/static/img/portfolio/onixlib/01.png)

Bibliothèque Python souveraine pour lire, parser et produire des fichiers ONIX

![pypi 0.1.1](https://img.shields.io/pypi/v/onixlib)
![Licence MIT](https://img.shields.io/badge/license-MIT-green)
![Python ≥ 3.11](https://img.shields.io/pypi/pyversions/onixlib)
![Version ONIX 3.0](https://img.shields.io/badge/ONIX-3.0-blue)

**onixlib** est une bibliothèque Python souveraine pour lire, parser et produire des fichiers ONIX — le standard d'échange de métadonnées du monde du livre.

Elle fournit des façades ergonomiques sur les structures ONIX 3.0, un parser streaming adapté aux grands fichiers de distribution, et un système de registre de versions extensible.

---

## Sommaire

- [Onixlib](#onixlib)
  - [Sommaire](#sommaire)
  - [Installation](#installation)
  - [Démarrage rapide](#démarrage-rapide)
    - [Lire un fichier ONIX (streaming)](#lire-un-fichier-onix-streaming)
    - [Lire un fichier ONIX (chargement complet)](#lire-un-fichier-onix-chargement-complet)
    - [Construire et sérialiser une notice ONIX](#construire-et-sérialiser-une-notice-onix)
  - [Référence des façades](#référence-des-façades)
    - [`parse(source, version=None)` — générateur](#parsesource-versionnone--générateur)
    - [`Product`](#product)
    - [`Notice`](#notice)
    - [`Header`](#header)
    - [`DescriptiveDetail`](#descriptivedetail)
    - [`CollateralDetail`](#collateraldetail)
    - [`PublishingDetail`](#publishingdetail)
    - [`ProductSupply` / `SupplyDetail` / `Price`](#productsupply--supplydetail--price)
    - [`Contributor`](#contributor)
  - [Gestion des versions ONIX](#gestion-des-versions-onix)
  - [Ajouter une nouvelle version ONIX](#ajouter-une-nouvelle-version-onix)
    - [1 — Déclarer la source XSD](#1--déclarer-la-source-xsd)
    - [2 — Générer les classes Python](#2--générer-les-classes-python)
    - [3 — Enregistrer la nouvelle version](#3--enregistrer-la-nouvelle-version)
    - [4 — Utiliser la nouvelle version](#4--utiliser-la-nouvelle-version)
  - [Développement](#développement)
    - [Pré-requis](#pré-requis)
    - [Cibles Makefile](#cibles-makefile)

---

## Installation

```bash
pip install onixlib
```

Prérequis : Python ≥ 3.11.

---

## Démarrage rapide

### Lire un fichier ONIX (streaming)

`parse()` est un générateur qui désérialise chaque `<Product>` indépendamment,
sans jamais charger l'ensemble du fichier en mémoire — recommandé pour les flux
de distribution volumineux.

```python
from onixlib import parse

for product in parse("notice.xml"):
    print(product.isbn, product.title)

    # Contributeurs
    if product.author:
        print("Auteur :", product.author.full_name)
    for c in product.contributors:
        print(f"  {c.role.value} — {c.full_name}")

    # Description et couverture
    if product.collateral:
        print("Description :", product.collateral.description)
        print("Couverture   :", product.collateral.cover_url)

    # Date de publication et éditeur
    if product.publishing:
        print("Date  :", product.publishing.publication_date)
        print("Marque:", product.publishing.imprint_name)

    # Prix
    for ps in product.product_supply:
        for price in ps.prices:
            print(f"  {price.amount} {price.currency} (type {price.price_type})")
```

La version ONIX est **auto-détectée** à partir de l'attribut `release` de la
racine XML. Pour forcer une version :

```python
for product in parse("notice.xml", version="3.0"):
    ...
```

---

### Lire un fichier ONIX (chargement complet)

```python
from onixlib import Notice

notice = Notice.parse_full("notice.xml")

print(notice.header.sender_name)
print(notice.header.sent_datetime)

for product in notice.products:
    print(product.isbn, product.title)
```

---

### Construire et sérialiser une notice ONIX

```python
from onixlib import Notice, Product, ContributorRole

# Produit
product = Product.new(isbn="9782070360024", title="Du côté de chez Swann")

author = product.add_contributor(role=ContributorRole.A01)
author.first_name = "Marcel"
author.last_name  = "PROUST"

# Notice complète
notice = Notice.new(sender_name="MON_EDITEUR", sent_datetime="20260428T000000Z")
notice.add_product(product)

xml = notice.to_xml()
print(xml)
```

---

## Référence des façades

Toutes les classes suivantes s'importent directement depuis `onixlib` :

```python
from onixlib import (
    parse, Notice, Product,
    Header, DescriptiveDetail, CollateralDetail,
    PublishingDetail, ProductSupply, SupplyDetail, Price,
    RelatedMaterial, RelatedProduct, RelatedWork,
    Contributor, ContributorRole,
)
```

### `parse(source, version=None)` — générateur

| Paramètre | Type | Description |
| --- | ---- | --- |
| `source` | `str \| Path \| BinaryIO` | Chemin ou flux binaire du fichier XML |
| `version` | `str \| None` | Forcer une version (ex. `"3.0"`). Auto-détecté si `None`. |

Retourne un générateur de `Product`.

---

### `Product`

Façade centrale sur un bloc `<Product>` ONIX.

| Attribut / méthode | Type | Description |
| --- | --- | --- |
| `isbn` | `str \| None` | ISBN-13 ou GTIN-13 |
| `title` | `str` | Titre principal (raccourci vers `descriptive`) |
| `author` | `Contributor \| None` | Premier contributeur de rôle A01 |
| `editor` | `Product.Editor \| None` | Détails de l'éditeur (raccourci vers `publishing`) |
| `price` | `Product.Price \| None` | Premier prix du produit (raccourci vers `product_supply`) |
| `publisher` | `Product.Publisher \| None` | Détails de l'éditeur (raccourci vers `product_supply`) |
| `contributors` | `list[Contributor]` | Tous les contributeurs |
| `add_contributor(role)` | `Contributor` | Ajoute un contributeur |
| `descriptive` | `DescriptiveDetail \| None` | Bloc descriptif |
| `collateral` | `CollateralDetail \| None` | Bloc collatéral |
| `publishing` | `PublishingDetail \| None` | Bloc publication |
| `product_supply` | `list[ProductSupply]` | Blocs disponibilité/prix |
| `related_material` | `RelatedMaterial \| None` | Liens vers œuvres/produits liés |
| `to_xml()` | `str` | Sérialisation XML ONIX |
| `Product.new(isbn, title, …)` | `Product` | Constructeur de commodité |

---

### `Notice`

Façade sur la notice ONIX complète (`<ONIXMessage>`).

| Attribut / méthode | Type | Description |
| --- | --- | --- |
| `header` | `Header` | En-tête de la notice |
| `products` | `list[Product]` | Tous les produits |
| `add_product(product)` | `None` | Ajoute un produit |
| `to_xml()` | `str` | Sérialisation XML |
| `Notice.parse_full(source, version)` | `Notice` | Chargement complet en mémoire |
| `Notice.new(sender_name, sent_datetime, release)` | `Notice` | Création d'une notice vide |

---

### `Header`

| Propriété | Type | Description |
| --- | --- | --- |
| `sender_name` | `str` | Nom de l'expéditeur |
| `sender_gln` | `str \| None` | GLN de l'expéditeur |
| `sender_email` | `str \| None` | E-mail de l'expéditeur |
| `addressee_name` | `str \| None` | Nom du destinataire |
| `addressee_gln` | `str \| None` | GLN du destinataire |
| `message_number` | `str \| None` | Numéro de message |
| `sent_datetime` | `str \| None` | Horodatage d'envoi |
| `Header.new(sender_name, sent_datetime)` | `Header` | Constructeur minimal |

---

### `DescriptiveDetail`

| Propriété | Type | Description |
| --- | --- | --- |
| `title` / setter | `str` | Titre principal |
| `subtitle` | `str \| None` | Sous-titre |
| `product_form` | `str` | Code List 150 (ex. `"BC"` = broché) |
| `product_composition` | `str` | Code List 2 (ex. `"00"` = exemplaire unique) |
| `contributors` | `list[Contributor]` | Tous les contributeurs |
| `author` | `Contributor \| None` | Premier auteur (A01) |
| `languages` | `list[tuple[str, str]]` | `(rôle, code_langue)` |
| `extents` | `list[tuple[str, str, str]]` | `(type, valeur, unité)` |
| `subjects` | `list[tuple[str, str]]` | `(code_schème, code_sujet)` |

---

### `CollateralDetail`

| Propriété | Type | Description |
| --- | --- | --- |
| `description` | `str \| None` | Description produit (TextType 03) |
| `text_contents` | `list[tuple[str, str]]` | `(type_code, texte)` |
| `cover_url` | `str \| None` | URL de la couverture (ResourceContentType 01) |
| `supporting_resources` | `list[tuple[str, list[str]]]` | `(type_code, [urls])` |

---

### `PublishingDetail`

| Propriété | Type | Description |
| --- | --- | --- |
| `imprint_name` / setter | `str \| None` | Marque éditoriale |
| `publisher_name` | `str \| None` | Nom de l'éditeur |
| `publishing_status` | `str \| None` | Statut de publication (List 64) |
| `publication_date` | `str \| None` | Date de publication nominale (DateRole 01) |
| `publishing_dates` | `list[tuple[str, str]]` | `(rôle, date)` |

---

### `ProductSupply` / `SupplyDetail` / `Price`

```python
for ps in product.product_supply:
    for sd in ps.supply_details:
        print(sd.supplier_name, sd.availability)
        for price in sd.prices:
            print(price.amount, price.currency, price.price_type)
```

| Classe | Propriétés clés |
| --- | --- |
| `ProductSupply` | `supply_details`, `availability`, `supplier_name`, `prices` (aplatis) |
| `SupplyDetail` | `supplier_name`, `availability`, `prices` |
| `Price` | `amount: Decimal`, `currency`, `price_type` |

---

### `Contributor`

| Propriété | Type | Description |
| --- | --- | --- |
| `first_name` / setter | `str` | Prénom(s) |
| `last_name` / setter | `str` | Nom de famille |
| `full_name` | `str` | `"Prénom NOM"` |
| `role` | `ContributorRole \| None` | Code List 17 (ex. `A01` = auteur) |

`ContributorRole` est l'enum `List17` ONIX : `ContributorRole.A01`, `ContributorRole.B06`, etc.

---

## Gestion des versions ONIX

onixlib intègre un registre de versions extensible. La version 3.0 est enregistrée
par défaut.

```python
from onixlib import available_releases

print(available_releases())  # ['3.0']
```

Le parser **auto-détecte** la version depuis l'attribut `release` de la racine XML.

---

## Ajouter une nouvelle version ONIX

Lorsque EDItEUR publie une nouvelle version des XSD (ex. ONIX 3.1), voici le
processus complet pour l'intégrer.

### 1 — Déclarer la source XSD

Dans `xsd_sources.toml`, ajouter une entrée :

```toml
[versions."3.1"]
source      = "https://www.editeur.org/files/ONIX%203/ONIX_3-1_reference_XSD.zip"
description = "ONIX 3.1 — prochaine version de référence (EDItEUR)"
```

### 2 — Générer les classes Python

```bash
make generate VERSION=3.1
# ou, pour forcer le re-téléchargement des XSD :
make generate-force VERSION=3.1
```

Cela produit `src/onixlib/models/generated/v3_1.py` via xsdata.

### 3 — Enregistrer la nouvelle version

Dans `src/onixlib/models/versions.py`, ajouter en bas du fichier :

```python
from .generated import v3_1 as _v3_1

register(VersionInfo(
    release="3.1",
    namespace="http://www.editeur.org/onix/3.1/reference",
    module=_v3_1,
    message_class=_v3_1.Onixmessage,
    product_class=_v3_1.Product,
))
```

### 4 — Utiliser la nouvelle version

```python
# Auto-détection depuis release="3.1" dans le XML
for product in parse("notice_3_1.xml"):
    ...

# Ou explicitement :
notice = Notice.parse_full("notice_3_1.xml", version="3.1")
```

Les versions antérieures (`"3.0"`) restent disponibles sans modification.

---

## Développement

### Pré-requis

```bash
python -m venv venv
source venv/bin/activate
make install-dev
```

### Cibles Makefile

| Commande | Description |
| --- | --- |
| `make generate-all` | Génère les modèles pour toutes les versions de `xsd_sources.toml` |
| `make generate VERSION=3.0` | Génère les modèles pour une version spécifique |
| `make generate-from SOURCE=url VERSION=3.1` | Génère depuis une URL externe |
| `make generate-force VERSION=3.0` | Re-télécharge les XSD et régénère |
| `make verify-xsd` | Vérifie l'intégrité des XSD (checksums `.meta.toml`) |
| `make list-versions` | Liste les versions enregistrées et leur statut |
| `make docs` | Génère la documentation Sphinx (HTML) dans `docs/build/html/` |
| `make docs-copy` | Copie `documentations/sphinxdoc/` vers `docs/` |
| `make docs-serve` | Lance un serveur local sur la doc générée (port 8080) |
| `make clean-generated` | Supprime les modèles générés (demande confirmation) |

---

> **_Rémi Verschuur · Audit IO · 2026_**
