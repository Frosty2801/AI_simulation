# AI_simulation // Admin_123
Assestment practice simulation

## Expose n8n with Cloudflare Tunnel

Telegram cannot send webhooks to `localhost`, so this project uses a Cloudflare Tunnel to expose `n8n` over HTTPS.

### 1. Create your local env file

Copy `.env.example` to `.env` and set:

- `N8N_BASIC_AUTH_USER`
- `N8N_BASIC_AUTH_PASSWORD`
- `N8N_PUBLIC_URL`
- `N8N_PUBLIC_HOST`
- `CLOUDFLARE_TUNNEL_TOKEN`

Example public URL:

`https://n8n.your-domain.com`

### 2. Create the tunnel in Cloudflare

In Cloudflare Zero Trust:

1. Go to `Networks` -> `Tunnels`
2. Create a new tunnel
3. Choose `Cloudflared`
4. Add a public hostname like `n8n.your-domain.com`
5. Point the service to `http://n8n:5678`
6. Copy the generated tunnel token into `.env` as `CLOUDFLARE_TUNNEL_TOKEN`

### 3. Start the stack

```bash
docker compose up -d
```

### 4. Verify webhook URL inside n8n

Once `n8n` is running, it should use the public URL from `N8N_PUBLIC_URL` for webhook registrations.

### 5. Connect Telegram

When you configure the Telegram Trigger or Telegram node, the webhook should now resolve through the public Cloudflare hostname instead of `localhost`.
