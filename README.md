# AI_simulation // Admin_123
Assestment practice simulation

## Expose n8n with ngrok

Telegram cannot send webhooks to `localhost`, so this project uses ngrok to expose `n8n` over HTTPS (free dynamic URLs).

### 1. Create your local env file

Copy `.env.example` to `.env` and set:

- `N8N_BASIC_AUTH_USER`
- `N8N_BASIC_AUTH_PASSWORD`
- `N8N_PUBLIC_URL` (set to ngrok url from localhost:4040)
- `N8N_PUBLIC_HOST`
- `NGROK_AUTHTOKEN`

Example public URL:

`https://abc123.ngrok-free.app` (dynamic, view at http://localhost:4040)

### 2. Setup ngrok

1. Sign up for free at https://ngrok.com
2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
3. Add to `.env`: `NGROK_AUTHTOKEN=your_token_here`

### 3. Start the stack

```bash
docker compose up -d
```

Check `docker compose logs ngrok` for startup.

### 4. Get ngrok URL and verify

1. `docker compose up -d`
2. Open http://localhost:4040 -> copy "HTTPS Forwarding URL"
3. (Optional) Add to .env `N8N_PUBLIC_URL=https://abc.ngrok-free.app` & restart compose for auto webhooks
4. Access n8n at http://localhost:5678 (admin/admin123), test workflows with ngrok URL

### 5. Connect Telegram

Use the ngrok HTTPS URL in Telegram Trigger node's webhook URL/Test URL.
