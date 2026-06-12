import { createClientFromRequest } from 'npm:@base44/sdk@0.8.31';

Deno.serve(async (req) => {
  try {
    const base44 = createClientFromRequest(req);
    const body = await req.json().catch(() => ({}));

    const messageIds: string[] = body.data?.new_message_ids ?? [];

    if (!messageIds.length) {
      return Response.json({ ok: true, message: 'No new messages' });
    }

    // Get Gmail access token
    const { accessToken } = await base44.asServiceRole.connectors.getConnection('gmail');
    const authHeader = { Authorization: `Bearer ${accessToken}` };

    const summaries: string[] = [];

    for (const messageId of messageIds) {
      const res = await fetch(
        `https://gmail.googleapis.com/gmail/v1/users/me/messages/${messageId}?format=full`,
        { headers: authHeader }
      );
      if (!res.ok) continue;

      const message = await res.json();
      const headers = message.payload?.headers ?? [];

      const subject = headers.find((h: any) => h.name === 'Subject')?.value ?? '(sem assunto)';
      const from = headers.find((h: any) => h.name === 'From')?.value ?? '(desconhecido)';
      const date = headers.find((h: any) => h.name === 'Date')?.value ?? '';

      // Extract body text
      let bodyText = '';
      const extractText = (part: any): string => {
        if (part.mimeType === 'text/plain' && part.body?.data) {
          return atob(part.body.data.replace(/-/g, '+').replace(/_/g, '/'));
        }
        if (part.parts) {
          for (const p of part.parts) {
            const t = extractText(p);
            if (t) return t;
          }
        }
        return '';
      };

      bodyText = extractText(message.payload);
      const snippet = bodyText.slice(0, 400).trim() || message.snippet || '';

      summaries.push(
        `📧 *Novo email!*\n` +
        `*De:* ${from}\n` +
        `*Assunto:* ${subject}\n` +
        `*Data:* ${date}\n\n` +
        `*Resumo:*\n${snippet}${bodyText.length > 400 ? '...' : ''}\n\n` +
        `🔑 ID: \`${messageId}\`\n` +
        `📩 Para responder, me diga: _"Responda o email ${messageId} dizendo: [sua mensagem]"_`
      );
    }

    if (summaries.length > 0) {
      // Send to agent (triggers the agent to notify the user via Telegram)
      await base44.asServiceRole.messaging.sendMessage({
        content: summaries.join('\n\n---\n\n'),
        role: 'user',
        metadata: { source: 'email_monitor', messageIds }
      });
    }

    return Response.json({ ok: true, processed: summaries.length });
  } catch (error) {
    console.error('Error processing email:', error);
    return Response.json({ error: error.message }, { status: 500 });
  }
});
