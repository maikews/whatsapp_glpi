# GLPI + Whatsapp - Notificação

Api do whatsapp utilizada: https://github.com/chrishubert/whatsapp-api

O código foi adaptado a minha necessidade, talvez possa te ajudar.

Fonte: https://github.com/diberlanda95/whatsapp_glpi 

---

Utilizei o crontab do servidor ubuntu para rodar periodicamente o script automaticamente.

```
sudo nano /etc/crontab
```

Add
```
# Whatsapp Api GLPI
*/5 *   * * *   user    python3 /home/user/GLPI_Whats/whatsapp_glpi.py
```

Restart cron service
```
sudo /etc/init.d/cron restart
```
