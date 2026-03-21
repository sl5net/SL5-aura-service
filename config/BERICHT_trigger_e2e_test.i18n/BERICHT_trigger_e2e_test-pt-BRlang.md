# Abschlussbericht: SL5 Aura – Teste de gatilho ponta a ponta

**Dado:** 2026-03-15  
**Data:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. O Plano

Um teste ponta a ponta do problema revelado é o seguinte:
**Bei manchen Aufnahmen fehlt das letzte Wort im Output.**

A solução do teste:
1. Um data WAV para um microfone virtual configurado
2. Aura para iniciar `touch /tmp/sl5_record.trigger` — genau wie im echten Betrieb
3. Mit zweitem Trigger stoppen
4. A saída com a transcrição do YouTube é atualizada
5. Feststellen ob ein Wort am Ende fehlt

---

## 2. Foi erreicht wurde ✅

- Aura reagiert auf den Trigger korrekt
- LT läuft und ist erreichbar (`http://127.0.0.1:8082`)
- `_wait_for_output()` encontre a data `tts_output_*.txt`
- `_fetch_yt_transcript_segment()` contém o texto de referência correto
- O teste básico é sólido e funcional.

---

## 3. O problema mais desconhecido 🔴

### Kern-Problem: `manage_audio_routing` foi resolvido

Beim Session-Start ruft Aura estagiário auf:
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

Esta função faz o primeiro:
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

**Sie löscht jeden Sink den wir vorher erstellt haben.**

Você não precisa de nenhum novo Sink em `mode == 'SYSTEM_DEFAULT'` (não `MIC_AND_DESKTOP`).

### Versuchte Lösungen

| Vertal | Problema |
|---|---|
| PulseAudio Virtual Source criado | PipeWire ignora `module-virtual-source` |
| `settings_local.py` no conjunto `MIC_AND_DESKTOP` | Datei wurde mit mehrfachen Einträgen korrumpiert |
| Marque Override-Block e finalize a tela | Aura lädt Configurações não schnell genug neu bevor Trigger kommt |
| `_create_mic_and_desktop_sink()` diretamente no teste | Aparece `manage_audio_routing` no início da sessão |
| `pw-loopback` | Erscheint als Source aber Aura hört nicht darauf |

### Warum `settings_local.py` Substituir não funciona

`dynamic_settings.py` monitora os dados e os coloca na hora — mas com um intervalo. Der Trigger kommt zu schnell nach dem Schreiben. Aura iniciou a sessão novamente com os outros `SYSTEM_DEFAULT`.

Além disso: selbst wenn Aura `MIC_AND_DESKTOP` lädt, erstellt es the Sink erst beim **nächsten** Session-Start — nicht sofort.

---

## 4. Mögliche Lösungswege

### Opção A — Längeres Warten nach Settings-Änderung
```python
_set_audio_input_device("MIC_AND_DESKTOP")
time.sleep(5.0)   # statt 1.5s — mehr Zeit für dynamic_settings reload
TRIGGER_FILE.touch()
```
Risiko: Nicht zuverlässig, timing-abhängig.

### Opção B — Aura neu starten nach Configurações-Enderung
__CODE_BLOCO_3__
Nachteil: Teste durante mais de 1 minuto. Aber zuverlässig.

### Opção C — `manage_audio_routing` diretamente no teste adicionado
```python
_set_audio_input_device("MIC_AND_DESKTOP")
subprocess.run(["./scripts/restart_venv_and_run-server.sh"])
time.sleep(60)   # warten bis LT bereit
TRIGGER_FILE.touch()
```
O Sink existe antes do Trigger ser conectado - e `manage_audio_routing` no início da sessão exibe `is_mic_and_desktop_sink_active() == True` e inicia a configuração.

Das ist wahrscheinlich die **sauberste Lösung**.

### Opção D — `process_text_in_background` diretamente adicionado (sem gatilho)
Como em `test_youtube_audio_regression.py` — Sua saída diretamente no pipeline é adicionada, sem o mesmo mecanismo de gatilho. Dann testou o pipeline antes de abandonar as palavras escritas.

### Opção E — Aura com `run_mode_override=TEST` iniciada
Falls Aura tem um modo de teste que der o recurso de roteamento de áudio.

---

## 5. Empfehlung

**Opção C** para testar — uma máquina de teste de importação:

__CODE_BLOCO_5__

Quando a funcionalidade:
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing
manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
```

Dann erkennt Aura beim Session-Start `is_mic_and_desktop_sink_active() == True` e lässt den Sink in Ruhe.

---

## 6. Foi este teste langfristig tragat

Sobald é läuft, kann man:
- `SPEECH_PAUSE_TIMEOUT` Foram testados (1.0, 2.0, 4.0s) e vistos como letzte Wort absgeschnitten wird
- `transcribe_audio_with_feedback.py` Parâmetro otimizado
- A regressão é corrigida quando o tratamento de áudio é executado
- Beweisen dass ein Fix wirklich hilft

---

---

# Relatório Final: SL5 Aura – Teste ponta a ponta

**Data:** 15/03/2026  
**Arquivo:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. O Plano

Um verdadeiro teste ponta a ponta para investigar o problema conhecido:
**Em algumas gravações, a última palavra é cortada na saída.**

O teste deve:
1. Alimente um arquivo WAV como um microfone virtual
2. Inicie o Aura via `touch /tmp/sl5_record.trigger` - exatamente como no uso real
3. Pare com um segundo gatilho
4. Compare o resultado com a transcrição do YouTube
5. Detecte se falta alguma palavra no final

---

## 2. O que foi alcançado ✅

- Aura responde ao gatilho corretamente
- LT está em execução e acessível (`http://127.0.0.1:8082`)
- `_wait_for_output()` encontra o arquivo `tts_output_*.txt`
- `_fetch_yt_transcript_segment()` busca o texto de referência corretamente
- A estrutura básica do teste é sólida e funciona conceitualmente

---

## 3. O problema não resolvido 🔴

### Problema central: `manage_audio_routing` substitui tudo

No início da sessão, o Aura chama internamente:
```bash
python3 -c "from scripts.py.func.manage_audio_routing import manage_audio_routing; print('OK')"
```

Esta função primeiro faz:
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

**Ele exclui qualquer coletor que criamos anteriormente.**

Então ele não cria nenhum novo coletor porque `mode == 'SYSTEM_DEFAULT'` (não `MIC_AND_DESKTOP`).

### Tentativas de soluções

| Tentativa | Problema |
|---|---|
| Criar fonte virtual PulseAudio | PipeWire ignora `module-virtual-source` |
| Defina `settings_local.py` como `MIC_AND_DESKTOP` | O arquivo foi corrompido com múltiplas entradas |
| Gravar bloco de substituição marcado no final do arquivo | Aura não recarrega as configurações rápido o suficiente antes do gatilho disparar |
| `_create_mic_and_desktop_sink()` diretamente em teste | Excluído por `manage_audio_routing` no início da sessão |
| `pw-loopback` | Aparece como fonte, mas Aura não escuta |

---

## 4. Próxima etapa recomendada

Chame `manage_audio_routing` diretamente do teste antes do gatilho:

__CODE_BLOCO_9__

Quando o Aura inicia a sessão ele verifica `is_mic_and_desktop_sink_active()` — se `True`, ele pula a configuração e deixa o coletor sozinho. Esta é a solução mais limpa.

---

## 5. O que este teste permitirá a longo prazo

Uma vez em execução:
- Teste os valores `SPEECH_PAUSE_TIMEOUT` (1,0, 2,0, 4,0s) e detecte o corte de palavras
- Otimize os parâmetros `transcribe_audio_with_feedback.py`
- Capture regressões quando o manuseio de áudio for alterado
- Prove que uma correção realmente funciona