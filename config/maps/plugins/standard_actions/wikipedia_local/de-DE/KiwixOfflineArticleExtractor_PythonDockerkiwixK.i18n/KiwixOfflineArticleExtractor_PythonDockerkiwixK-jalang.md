## Kiwix オフライン記事抽出 (Python/Docker/kiwix-serve)

このドキュメントでは、Docker コンテナ内で実行されている `kiwix-serve` Web サーバーを使用して、オフライン ZIM ファイルから Wikipedia 記事の完全なクリーン テキストを抽出する Python スクリプトをセットアップして使用するためのステップバイステップ ガイドを提供します。

### 前提条件

Manjaro システムには次のソフトウェアがインストールされている必要があります。

1. **Docker:** コンパイルの問題を発生させずに公式の `kiwix-tools` サーバーを実行します。
2. **Python 3:** 仮想環境 (`venv`) を使用します。
3. **ZIM ファイル:** オフラインの Wikipedia データベース (例: `wikipedia_de_all_mini_2025-09.zim`)。

### 1. システムセットアップ (Docker)

Docker サービスがインストールされ、実行されていることを確認します。

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

### 2. Python 環境のセットアップ

Python 仮想環境をセットアップし、必要なライブラリをインストールします。

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

### 3. Kiwix サーバーの実行 (コアの依存関係)

このスクリプトは、ポート `8080` で実行されている `kiwix-serve` に依存しています。このコマンドは、公式の安定した Docker イメージを使用し、現在のディレクトリ (ZIM ファイルを含む) をコンテナーにバインドします。

**重要:** このコマンドを実行する前に、ZIM ファイル (例: `wikipedia_de_all_mini_2025-09.zim`) を `kiwix_cli` ディレクトリに配置してください。

```bash
# Run the kiwix-serve command in the background (using -d)
# Docker runs the kiwix-tools binary located at /usr/local/bin/kiwix-serve

sudo systemctl start docker

Run this one-liner to forcefully stop and remove any running Kiwix container:
code Bash

docker rm -f $(docker ps -aq --filter ancestor=ghcr.io/kiwix/kiwix-tools)

docker run --rm -d -p 8080:8080 -v ~/Downloads/wikipedia_de_all_mini_2025-09.zim:/data/wikipedia_de_all_mini_2025-09.zim ghcr.io/kiwix/kiwix-tools /usr/local/bin/kiwix-serve --port 8080 /data/wikipedia_de_all_mini_2025-09.zim


```
サーバーは現在 `http://localhost:8080` で実行されています。

### 4. 記事抽出スクリプト

`article_extractor.py` という名前のファイルを作成し、次の最終的な動作するコードをそのファイルに貼り付けます。

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

### 5. アプリケーションとクリーンアップ

1. **スクリプトを実行します:**
    ```bash
    python article_extractor.py
    ```

2. **Docker サーバーを停止します (完了したら):**
Docker コンテナを停止する必要があります。停止しないと、ポート 8080 が使用され続けます。
    ```bash
    # Find the container ID (or just the first few characters)
    docker ps 
    
    # Stop the container
    docker stop <CONTAINER_ID>
    ```
  
  