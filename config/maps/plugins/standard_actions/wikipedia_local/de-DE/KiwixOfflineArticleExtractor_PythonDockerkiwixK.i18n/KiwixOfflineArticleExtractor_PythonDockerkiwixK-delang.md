## Kiwix Offline-Artikelextraktor (Python/Docker/kiwix-serve)

Dieses Dokument bietet eine Schritt-für-Schritt-Anleitung zum Einrichten und Verwenden eines Python-Skripts, das den vollständigen, sauberen Text eines Wikipedia-Artikels aus einer Offline-ZIM-Datei extrahiert, indem der Webserver „kiwix-serve“ in einem Docker-Container ausgeführt wird.

### Voraussetzungen

Auf Ihrem Manjaro-System muss die folgende Software installiert sein:

1. **Docker:** Um den offiziellen „kiwix-tools“-Server ohne Kompilierungsprobleme auszuführen.
2. **Python 3:** Mit einer virtuellen Umgebung („venv“).
3. **Eine ZIM-Datei:** Die Offline-Wikipedia-Datenbank (z. B. „wikipedia_de_all_mini_2025-09.zim“).

### 1. System-Setup (Docker)

Stellen Sie sicher, dass der Docker-Dienst installiert ist und ausgeführt wird.

```bash
# 1. Install Docker on Manjaro
sudo pacman -S docker

# 2. Start and enable the Docker service
sudo systemctl start docker
sudo systemctl enable docker

# 3. Add your user to the 'docker' group (avoids 'sudo' for docker commands)
sudo usermod -aG docker $USER

# NOTE: You must log out and log back in (or reboot) for the group change to take effect.
```

### 2. Einrichtung der Python-Umgebung

Richten Sie Ihre virtuelle Python-Umgebung ein und installieren Sie die erforderlichen Bibliotheken.

```bash
# Create a new directory for your project (e.g., 'kiwix_cli')
mkdir kiwix_cli
cd kiwix_cli

# Create and activate a Python virtual environment
python -m venv .venv
source .venv/bin/activate

# Install required libraries
pip install requests beautifulsoup4
```

### 3. Ausführen des Kiwix-Servers (die Kernabhängigkeit)

Das Skript basiert darauf, dass „kiwix-serve“ auf Port „8080“ ausgeführt wird. Dieser Befehl verwendet das offizielle, stabile Docker-Image und bindet Ihr aktuelles Verzeichnis (das die ZIM-Datei enthält) an den Container.

**WICHTIG:** Platzieren Sie Ihre ZIM-Datei (z. B. „wikipedia_de_all_mini_2025-09.zim“) im Verzeichnis „kiwix_cli“, bevor Sie diesen Befehl ausführen.

```bash
# Run the kiwix-serve command in the background (using -d)
# Docker runs the kiwix-tools binary located at /usr/local/bin/kiwix-serve

sudo systemctl start docker

Run this one-liner to forcefully stop and remove any running Kiwix container:
code Bash

docker rm -f $(docker ps -aq --filter ancestor=ghcr.io/kiwix/kiwix-tools)

docker run --rm -d -p 8080:8080 -v ~/Downloads/wikipedia_de_all_mini_2025-09.zim:/data/wikipedia_de_all_mini_2025-09.zim ghcr.io/kiwix/kiwix-tools /usr/local/bin/kiwix-serve --port 8080 /data/wikipedia_de_all_mini_2025-09.zim


```
Der Server läuft jetzt unter „http://localhost:8080“.

### 4. Das Artikelextraktionsskript

Erstellen Sie eine Datei mit dem Namen „article_extractor.py“ und fügen Sie den folgenden endgültigen, funktionierenden Code ein.

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re

# --- CONFIGURATION (Change these values to match your ZIM file and server port) ---
ZIM_FILE_NAME = "wikipedia_de_all_mini_2025-09.zim"
BASE_SERVER_URL = "http://localhost:8080"
ZIM_URL_PART = ZIM_FILE_NAME.replace('.zim', '')
# --- END CONFIGURATION ---

def _find_best_article_path_via_http(search_term: str, zim_file: str) -> str | None:
    """
    Performs a search via the kiwix-serve HTTP API and finds the best article path.
    
    The best match logic ensures the most relevant non-disambiguation article is chosen.
    """
    
    search_url = (
        f"{BASE_SERVER_URL}/search?"
        f"pattern={quote(search_term)}&"
        f"book={zim_file}"
    )
    
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Select all search result links
        result_links = soup.select('div.results ul li a')
        
        if not result_links:
            return None
        
        best_path = None
        shortest_non_disambiguation_path = None
        shortest_length = float('inf')
        
        for link in result_links:
            href = link.get('href')
            link_text = link.get_text().strip()
            
            # Extract the article path from the anchor link (e.g., /viewer#.../Tübingen)
            article_path_with_hash = href.split('#', 1)[-1]
            final_content_path = f"/{article_path_with_hash}"

            # Priority 1: Exact Match (case-insensitive) - e.g., 'Tübingen' == 'tübingen'
            if link_text.lower() == search_term.lower():
                return final_content_path

            # Priority 2: Shortest title that is NOT a 'Begriffsklärung'
            if "Begriffsklärung" not in link_text and "Begriffsklärung" not in link_text:
                if len(link_text) < shortest_length:
                    shortest_length = len(link_text)
                    shortest_non_disambiguation_path = final_content_path
                
            # Fallback: Keep the first link's path
            if best_path is None:
                best_path = final_content_path
                
        if shortest_non_disambiguation_path:
            return shortest_non_disambiguation_path
        
        # Priority 3: Fallback to the first result (which might be a disambiguation page)
        return best_path

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to fetch search URL. Is kiwix-serve running? Error: {e}")
        return None

def execute(search_term: str) -> str:
    """
    Searches for an article and fetches its clean text content.
    """
    try:
        # Step 1: Find the article path using the HTTP Search API
        article_path = _find_best_article_path_via_http(search_term, ZIM_FILE_NAME)
        
        if not article_path:
            return f"No articles found for search term: '{search_term}'"

        # Step 2: Construct the full URL for the article content
        server_article_url = f"{BASE_SERVER_URL}{article_path}"

        # Step 3: Fetch the article's HTML content
        response = requests.get(server_article_url, timeout=10)
        response.raise_for_status()

        # Step 4: Parse the HTML and extract clean text
        soup = BeautifulSoup(response.content, 'html.parser')

        article_text_parts = []
        if soup.find('body'):
            # Extract text only from paragraph tags for clean content
            paragraphs = soup.find('body').find_all('p')
            article_text_parts = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
            
        if not article_text_parts:
            # Absolute fallback: get all text from the body
            body_text = soup.find('body').get_text() if soup.find('body') else soup.get_text()
            return ' '.join(body_text.split())

        # Join paragraphs with two newlines for readability
        full_text = "\n\n".join(article_text_parts)
        clean_text = ' '.join(full_text.split())
        
        return clean_text

    except requests.exceptions.RequestException as e:
        return f"ERROR: Failed to fetch article URL '{server_article_url}'. Is kiwix-serve running? Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred during processing: {e}"

# --- Example Usage ---
if __name__ == '__main__':
    # Test 1: Exact match with case difference
    print("-" * 50)
    print("TEST: Tübingen")
    text_tuebingen = execute("Tübingen")
    print(text_tuebingen[:200] + "...") 
    
    # Test 2: Inexact search that requires fuzzy matching
    print("-" * 50)
    print("TEST: licht (should find Licht)")
    text_licht = execute("licht")
    print(text_licht[:200] + "...")
    
    # Test 3: Search with no result
    print("-" * 50)
    print("TEST: nonexistantarticle")
    text_fail = execute("nonexistantarticle")
    print(text_fail)
```

### 5. Anwendung und Bereinigung

1. **Führen Sie das Skript aus:**
    ```bash
    python article_extractor.py
    ```

2. **Stoppen Sie den Docker-Server (wenn Sie fertig sind):**
Sie müssen den Docker-Container stoppen, sonst verwendet er weiterhin Port 8080.
    ```bash
    # Find the container ID (or just the first few characters)
    docker ps 
    
    # Stop the container
    docker stop <CONTAINER_ID>
    ```
  
  