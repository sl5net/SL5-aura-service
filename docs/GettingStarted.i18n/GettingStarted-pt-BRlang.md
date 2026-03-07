# Introdução ao SL5 Aura

## O que é SL5 Aura?

SL5 Aura é um assistente de voz off-line que converte fala em texto (STT) e aplica regras configuráveis para limpar, corrigir e transformar a saída.

Funciona sem GUI – tudo é executado via CLI ou console.

## Como funciona

```
Microphone → Vosk (STT) → Maps (Pre) → LanguageTool → Maps (Post) → Output
```

1. **Vosk** converte seu discurso em texto bruto
2. **Pré-Mapas** limpe e corrija o texto antes da verificação ortográfica
3. **LanguageTool** corrige gramática e ortografia
4. **Pós-Mapas** aplicam transformações finais
5. **Saída** é o texto limpo final (e opcionalmente TTS)

## Seus primeiros passos

### 1. Inicie a Aura
```bash
python main.py
```

### 2. Teste com entrada do console
Digite `s` seguido do seu texto:
```
s hello world
```

### 3. Veja uma regra em ação
Abra `config/maps/koans_deutsch/01_koan_erste_schritte/de-DE/FUZZY_MAP_pre.py`

Remova o comentário da regra e teste novamente. O que acontece?

## Compreendendo as regras

As regras residem em `config/maps/` em arquivos Python chamados `FUZZY_MAP_pre.py` ou `FUZZY_MAP.py`.

Uma regra é assim:
__CODE_BLOCO_3__

A **saída** vem primeiro – você vê imediatamente o que a regra produz.

As regras são processadas **de cima para baixo**. O primeiro fullmatch (`^...$`) para tudo.

## Koans – Aprendendo fazendo

Koans são pequenos exercícios em `config/maps/koans_deutsch/` e `config/maps/koans_english/`.

Cada koan ensina um conceito:

| Koan | Tópico |
|---|---|
| 01_koan_erste_schritte | Primeira regra, fullmatch, parada de pipeline |
| 02_koan_listen | Listas, múltiplas regras |
| 03_koan_schwierige_namen | Nomes difíceis, correspondência fonética |

Comece com Koan 01 e vá aumentando.

## Pontas

- Regras em `FUZZY_MAP_pre.py` executadas **antes** da verificação ortográfica – bom para corrigir erros de STT
- As regras em `FUZZY_MAP.py` são executadas **após** a verificação ortográfica – bom para formatação
- Arquivos de backup (`.peter_backup`) são criados automaticamente antes de qualquer alteração
- Use `peter.py` para permitir que uma IA trabalhe através dos koans automaticamente