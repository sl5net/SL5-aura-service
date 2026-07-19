# setup/helper/download_and_extract_helper.sh
# --- Configuration ---
PREFIX="Z_"
# Format: "BaseName FinalDirName DestinationPath"
ARCHIVE_CONFIG=(
    "LanguageTool-6.6 LanguageTool-6.6 ."
    "vosk-model-en-us-0.22 vosk-model-en-us-0.22 ./models"
    "vosk-model-small-en-us-0.15 vosk-model-small-en-us-0.15 ./models"
    "vosk-model-de-0.21 vosk-model-de-0.21 ./models"
    "lid.176 lid.176.bin ./models"
)
DOWNLOAD_REQUIRED=false

# --- Filter Configuration based on EXCLUDE_LANGUAGES ---
INSTALL_CONFIG=()
if [ -z "$EXCLUDE_LANGUAGES" ]; then
    # Keine Ausschlüsse, die gesamte MASTER-Liste wird installiert.
    INSTALL_CONFIG=("${ARCHIVE_CONFIG[@]}")
else
    # Ausschlüsse aktiv, die Liste wird gefiltert.
    for config_line in "${ARCHIVE_CONFIG[@]}"; do
        read -r base_name final_name dest_path <<< "$config_line"

        IS_MANDATORY=false
        IS_EXCLUDED=false

        # Komponenten, die immer benötigt werden (z.B. LanguageTool Core)
        if [[ "$base_name" == "LanguageTool-6.6" ]] || [[ "$base_name" == "lid.176" ]]; then
            IS_MANDATORY=true
        fi

        # 1. Ausschluss-Check: exclude=all
        if [ "$EXCLUDE_LANGUAGES" == "all" ] && [ "$IS_MANDATORY" = false ]; then
            echo "    -> Excluding (all): $base_name"
            IS_EXCLUDED=true
        fi

        # 2. Ausschluss-Check: Spezifische Sprachen (z.B. de, en)
        if [ "$IS_EXCLUDED" = false ]; then
            # Test auf 'de' im Namen und in der Ausschlussliste
            if [[ "$base_name" =~ vosk-model-de- ]] && [[ "$EXCLUDE_LANGUAGES" =~ de ]]; then
                echo "    -> Excluding (de): $base_name"
                IS_EXCLUDED=true
            fi
            # Test auf 'en' im Namen und in der Ausschlussliste
            if [[ "$base_name" =~ vosk-model-en-us- ]] && [[ "$EXCLUDE_LANGUAGES" =~ en ]]; then
                echo "    -> Excluding (en): $base_name"
                IS_EXCLUDED=true
            fi

            if [[ "$base_name" == "vosk-model-en-us-0.22" ]] && ([[ "$EXCLUDE_LANGUAGES" =~ en ]] || [[ "$CI" == "true" ]]); then
                echo "    -> Excluding large in CI (en): $base_name"
                IS_EXCLUDED=true
            fi


            # Hinzufügen weiterer spezifischer Exklusionsregeln nach Bedarf...
        fi

        # Nur hinzufügen, wenn nicht ausgeschlossen
        if [ "$IS_EXCLUDED" = false ]; then
            INSTALL_CONFIG+=("$config_line")
        fi
    done
fi
# --- End Filter Configuration ---


# --- Phase 1: Check and attempt to restore from local ZIP cache ---
echo "    -> Phase 1: Checking and trying to restore from local cache..."
for config_line in "${INSTALL_CONFIG[@]}"; do
    read -r base_name final_name dest_path <<< "$config_line"
    target_path="$dest_path/$final_name"
    zip_file="$PROJECT_ROOT/${PREFIX}${base_name}.zip"

    # If the component already exists, we're good for this one.
    if [ -e "$target_path" ]; then
        continue
    fi

    # The component is missing. Let's see if we can unzip it from a local cache.
    echo "    -> Missing: '$target_path'. Searching for '$zip_file'..."
    if [ -f "$zip_file" ]; then
        echo "    -> Found ZIP cache. Extracting '$zip_file'..."
        unzip -q "$zip_file" -d "$dest_path"
    else
        # The ZIP is not there. We MUST run the downloader.
        echo "    -> ZIP cache not found. A download is required."
        DOWNLOAD_REQUIRED=true
    fi
done

# --- Phase 2: Download if necessary ---
if [ "$DOWNLOAD_REQUIRED" = true ]; then
    echo "    -> Phase 2: Running Python downloader for missing components..."

    # Create the models directory before attempting to download files into it.
    mkdir -p ./models

    ./.venv/bin/python tools/download_all_packages.py --exclude "$EXCLUDE_LANGUAGES"
    echo "    -> Downloader finished. Retrying extraction..."

    # After downloading, we must re-check and extract anything that's still missing.
    for config_line in "${INSTALL_CONFIG[@]}"; do
        read -r base_name final_name dest_path <<< "$config_line"
        target_path="$dest_path/$final_name"
        zip_file="$PROJECT_ROOT/${PREFIX}${base_name}.zip"

        if [ -e "$target_path" ]; then
            continue
        fi

        if [ -f "$zip_file" ]; then
            echo "    -> Extracting newly downloaded '$zip_file'..."
            unzip -q "$zip_file" -d "$dest_path"
        else
            echo "    -> FATAL: Downloader ran but '$zip_file' is still missing. Aborting."
            exit 1
        fi
    done
fi

echo "--> All components are present and correctly placed."

# ==============================================================================
# --- End of Download/Extract block ---
# ==============================================================================

