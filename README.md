# 📬 Agente de Email Inteligente — Base44 Superagent

Um agente pessoal de inteligência artificial que **monitora, resume e responde seus emails automaticamente**, integrado ao **Telegram** para que você gerencie sua caixa de entrada de qualquer lugar, sem abrir o computador.

---

## 🤖 O que este agente faz

- **Monitora sua caixa de entrada em tempo real** — assim que um email chega, o agente é notificado automaticamente.
- **Resume o conteúdo do email** — extrai remetente, assunto, data e um resumo do corpo da mensagem.
- **Envia a notificação no Telegram** — você recebe um aviso direto no celular com todas as informações importantes.
- **Responde emails pelo Telegram** — basta dizer ao agente o que quer responder e ele envia o email por você.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| [Base44](https://base44.com) | Plataforma do agente de IA |
| Gmail API (OAuth2) | Leitura e envio de emails |
| Telegram Bot API | Canal de comunicação com o usuário |
| Deno (Backend Functions) | Processamento dos emails em tempo real |
| Google Cloud Pub/Sub | Webhook de notificação de novos emails |

---

## 📁 Estrutura do projeto

```
├── functions/
│   └── processNewEmail.ts   # Função que processa emails recebidos e notifica no Telegram
├── base44/
│   └── connectors/
│       └── gmail.jsonc       # Configuração do conector Gmail
├── .agents/
│   ├── BOOTSTRAP.md          # Configuração inicial do agente
│   └── mcps/
│       └── config.json       # Configuração de ferramentas externas (MCP)
└── README.md
```

---

## ⚙️ Como funciona

```
Gmail recebe email
       ↓
Google Pub/Sub dispara webhook
       ↓
Base44 chama a automação do agente
       ↓
Agente lê o email completo via Gmail API
       ↓
Agente resume e envia mensagem no Telegram
       ↓
Você responde pelo Telegram
       ↓
Agente envia o email de resposta pelo Gmail
```

---

## 🚀 Como configurar

### 1. Pré-requisitos
- Conta na plataforma [Base44](https://base44.com)
- Conta Gmail (gmail.com)
- Bot do Telegram criado via [@BotFather](https://t.me/BotFather)

### 2. Conectar o Gmail
No painel do agente, conecte sua conta Google com permissões de leitura e envio de emails.

### 3. Conectar o Telegram
No painel do agente, conecte o bot do Telegram. O bot já estará disponível em [@AlexisMail_bot](https://t.me/AlexisMail_bot).

### 4. Ativar a automação
A automação de monitoramento de emails é criada automaticamente pelo agente e fica ativa em segundo plano.

---

## 💬 Como usar pelo Telegram

Após a configuração, basta conversar com o bot:

- **Receber resumos:** automático, assim que um email chega
- **Responder um email:** `"Responda o email [ID] dizendo: Olá, recebi sua mensagem..."`
- **Pedir lista de emails recentes:** `"Quais os últimos emails que recebi?"`
- **Resumir um email específico:** `"Me resume o email de [nome do remetente]"`

---

## 📄 Licença

MIT — use à vontade!

---

Feito com ❤️ usando [Base44](https://base44.com)
