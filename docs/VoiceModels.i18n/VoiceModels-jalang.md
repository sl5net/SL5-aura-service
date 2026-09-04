```markdown
# Voice Models & Memory Management

Aura uses offline speech recognition models (powered by Vosk). Models are available for over 20 languages and come in two distinct tiers to fit any hardware.

---

## 1. Model Tiers

| Tier | Folder Pattern | RAM Usage | Best For |
|---|---|---|---|
| **Small Models** | `vosk-model-small-*` | ~100–250 MB | Systems with < 8 GB RAM, Laptops, Raspberry Pi |
| **Standard Models** | `vosk-model-*` | ~1.5–4.5 GB | Systems with ≥ 8 GB RAM, Desktop workstations |

---

## 2. Supported Languages

Vosk provides official offline models for English, German, French, Spanish, Italian, Portuguese, Russian, Chinese, Japanese, and many others.

- **Browse & Download Models:** [Official Vosk Model Directory](https://alphacephei.com/vosk/models)

---

## 3. How to Install and Switch Models

### Step 1: Download and Extract
Download the model archive for your language and extract it into the `models/` directory:

```bash
CDモデル
wget -q --show-progress https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
unzip -q vosk-model-small-de-0.15.zip
rm vosk-model-small-de-0.15.zip
CD ..
```

### Step 2: Set Active Model
Write the exact folder name into `config/model_name.txt`:

```bash
echo "vosk-model-small-de-0.15" > config/model_name.txt
```

### Step 3: Set in config/settings.py

open `config/settings.py` change model there

```py
PRELOAD_MODELS = ["vosk-model .."]
```


Restart Aura to apply the new model.

---

## 4. Troubleshooting & Virtual RAM (Swap)

If Aura's memory watchdog triggers or the application runs out of memory, follow these steps:

### Option A: Switch to a Small Model (Recommended)
Switch to the `small` version of your language (e.g. `vosk-model-small-fr-0.22` instead of `vosk-model-fr-0.22`).

### Option B: Configure Virtual RAM (Swap / Paging File)

#### Linux (Create an 8 GB Swapfile):
```bash
sudo スワップオフ -a
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap 0 0' | sudo tee -a /etc/fstab
```

#### Windows (Increase Paging File):
1. Press `Win + R`, type `sysdm.cpl`, and press **Enter**.
2. Go to the **Advanced** tab -> click **Settings** under *Performance*.
3. Go to the **Advanced** tab -> click **Change** under *Virtual Memory*.
4. Uncheck *Automatically manage paging file size*, select your drive, and set **Initial size** and **Maximum size** (e.g. `8192 MB`).

#### macOS (Dynamic Swap Management):
macOS dynamically allocates swapfiles in `/private/var/vm/`. Ensure your system drive has at least **10–15 GB** of free disk space so the kernel can allocate swap space automatically. Check current swap usage with:
```bash
sysctl vm.swapusage
```
```