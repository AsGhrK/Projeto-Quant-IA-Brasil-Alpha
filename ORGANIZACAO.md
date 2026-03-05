# 📁 Reorganização do Projeto Quant IA Brasil

## Estrutura Nova Proposta

```
quant-ia-brasil/
├── apps/                          # Aplicações Streamlit
│   ├── __init__.py
│   ├── app_quant_ia.py           # ← MOVER DE: raiz/app_quant_ia.py
│   └── dashboard.py              # ← MOVER DE: raiz/dashboard.py
│
├── core/                          # Núcleo do projeto (lógica + dados)
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py           # ← MOVER DE: database/database.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── crypto_collector.py   # ← MOVER DE: data/crypto_collector.py
│   │   ├── global_collector.py   # ← MOVER DE: data/global_collector.py
│   │   ├── market_data.py        # ← MOVER DE: data/market_data.py
│   │   ├── news_collector.py     # ← MOVER DE: data/news_collector.py
│   │   └── stocks_collector.py   # ← MOVER DE: data/stocks_collector.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── ml_model.py           # ← MOVER DE: models/ml_model.py
│   ├── indicators/
│   │   ├── __init__.py
│   │   └── technical.py          # ← MOVER DE: indicators/technical.py
│   └── engines/
│       ├── __init__.py
│       ├── ai_assistant.py       # ← MOVER DE: engines/ai_assistant.py
│       ├── patterns.py           # ← MOVER DE: engines/patterns.py
│       ├── regime_engine.py      # ← MOVER DE: engines/regime_engine.py
│       └── decision_engine.py    # ← MOVER DE: raiz/decision_engine.py
│
├── scripts/                       # Utilitários e automação
│   ├── __init__.py
│   ├── scheduler.py              # ← MOVER DE: raiz/scheduler.py
│   ├── setup_carteira.py         # ← MOVER DE: raiz/setup_carteira.py
│   ├── collect_all.py            # ← MOVER DE: raiz/collect_all.py
│   └── test_assistant.py         # ← MOVER DE: raiz/test_assistant.py
│
├── legacy/                        # Arquivos deprecados/antigos
│   ├── app_principal.py          # ← MOVER DE: raiz/app_principal.py
│   ├── market_scanner.py         # ← MOVER DE: raiz/market_scanner.py
│   └── main.py                   # ← MOVER DE: raiz/main.py (em desuso)
│
├── venv/                          # Ambiente virtual (não mexer)
├── data/                         # Diretório original (pode deletar após migrate)
├── news/                         # Diretório vazio (pode mover se houver uso)
│
├── market_data.db               # Banco de dados SQLite (na raiz)
├── requirements.txt             # Dependências Python
├── README.md                    # Documentação principal
└── ORGANIZACAO.md               # Este arquivo
```

---

## 📋 Guia de Migração

### Passo 1: Mover arquivos de aplicações
```powershell
# Mover Streamlit apps
Move-Item -Path "app_quant_ia.py" -Destination "apps/"
Move-Item -Path "dashboard.py" -Destination "apps/"
```

### Passo 2: Mover lógica de banco de dados
```powershell
# Já existe em database/, mas mover imports se necessário
Move-Item -Path "database/database.py" -Destination "core/database/"
```

### Passo 3: Mover coletores de dados
```powershell
# Reorganizar data
Move-Item -Path "data/*.py" -Destination "core/data/"
```

### Passo 4: Mover modelos e indicadores
```powershell
Move-Item -Path "models/ml_model.py" -Destination "core/models/"
Move-Item -Path "indicators/technical.py" -Destination "core/indicators/"
```

### Passo 5: Mover engines
```powershell
# Reorganizar engines
Move-Item -Path "engines/*.py" -Destination "core/engines/"
Move-Item -Path "decision_engine.py" -Destination "core/engines/"
```

### Passo 6: Mover scripts utilitários
```powershell
Move-Item -Path "scheduler.py", "setup_carteira.py", "collect_all.py", "test_assistant.py" -Destination "scripts/"
```

### Passo 7: Arquivar legacy
```powershell
Move-Item -Path "app_principal.py", "market_scanner.py", "main.py" -Destination "legacy/"
```

---

## 🔧 Atualizar Imports após Migração

### Antes (raiz):
```python
from database.database import create_connection
from data.market_data import get_stock_data
from models.ml_model import train_model
from indicators.technical import add_indicators
from engines.ai_assistant import get_ai_recommendation
from engines.regime_engine import detect_regime
from engines.patterns import identify_patterns
from scheduler import start_scheduler
from collect_all import run_collection
```

### Depois (nova estrutura):
```python
from core.database.database import create_connection
from core.data.market_data import get_stock_data
from core.models.ml_model import train_model
from core.indicators.technical import add_indicators
from core.engines.ai_assistant import get_ai_recommendation
from core.engines.regime_engine import detect_regime
from core.engines.patterns import identify_patterns
from scripts.scheduler import start_scheduler
from scripts.collect_all import run_collection
```

---

## 📝 Arquivos que Precisam Ser Atualizados

| Arquivo | Ação | Imports a Ajustar |
|---------|------|---|
| `apps/app_quant_ia.py` | Mover + Atualizar imports | database, scheduler (relative imports) |
| `apps/dashboard.py` | Mover | Nenhum importante |
| `scripts/scheduler.py` | Mover | collect_all para scripts.collect_all |
| `scripts/collect_all.py` | Mover | data.* para core.data.* |
| `scripts/setup_carteira.py` | Mover | Nenhum |
| `core/engines/ai_assistant.py` | Mover | database para core.database, patterns para . |
| `core/engines/patterns.py` | Mover | Nenhum importante |
| `core/engines/regime_engine.py` | Mover | database para core.database |
| `core/data/*` | Mover | database para core.database |

---

## ✅ Checklist Final

- [ ] Criar estrutura de pastas (OS FEITO ✓)
- [ ] Mover apps/* (próximo passo)
- [ ] Mover core/* (próximo passo)
- [ ] Mover scripts/* (próximo passo)
- [ ] Arquivar legacy/* (próximo passo)
- [ ] Atualizar imports em todos os arquivos moveidos
- [ ] Testar: `streamlit run apps/app_quant_ia.py`
- [ ] Testar: `python scripts/collect_all.py`
- [ ] Deletar diretórios antigos vazios (data/, database/, models/, indicators/, engines/)
- [ ] Atualizar README.md com nova estrutura

---

## 🎯 Benefícios da Nova Estrutura

✅ **Modularidade**: Componentes separados por responsabilidade  
✅ **Escalabilidade**: Fácil adicionar novas apps ou engines  
✅ **Manutenibilidade**: Estrutura clara e intuitiva  
✅ **Testing**: Isolação de testes por módulo  
✅ **Produção**: Pronto para containerização (Docker)  

---

**Data da organização**: 4 de março de 2026  
**Status**: Estrutura criada, aguardando migração de arquivos
