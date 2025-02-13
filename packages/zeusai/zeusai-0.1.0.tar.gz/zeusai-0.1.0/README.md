# ZeusAI

Uma biblioteca simples para interagir com a API ZeusAI.

## Instalação

```bash
pip install zeusai
```

## Uso

```python
from zeusai import ZeusAI

zeus_ai = ZeusAI(api_key='YOUR_API_KEY')
response = zeus_ai.send_message(prompt='Olá, Zeus!')
print(response)
```
