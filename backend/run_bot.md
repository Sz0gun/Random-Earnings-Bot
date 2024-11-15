Tak, jeśli zamkniesz terminal, w którym uruchomiłeś skrypt, to proces, w tym przypadku działanie Twojego bota, również zostanie zatrzymany. Aby bot działał w tle, nawet po zamknięciu terminala, masz kilka opcji:

### 1. **Uruchomienie bota w tle za pomocą `nohup`**:
`nohup` pozwala uruchomić program w tle, niezależnie od terminala. Możesz użyć tej komendy, aby uruchomić skrypt, który będzie działał w tle, nawet po zamknięciu terminala.

```bash
nohup python /ścieżka/do/skryptu.py &
```

- `nohup`: oznacza "no hang up" i pozwala na działanie programu po zamknięciu terminala.
- `&`: Uruchamia program w tle.

Po uruchomieniu tej komendy, wszystkie logi będą zapisane w pliku `nohup.out` w katalogu, w którym uruchomiłeś tę komendę. Możesz sprawdzić wynik, używając:

```bash
tail -f nohup.out
```

### 2. **Użycie `screen`**:
`screen` to narzędzie, które pozwala na tworzenie wirtualnych sesji terminalowych, które mogą działać w tle.

1. Zainstaluj `screen`, jeśli jeszcze go nie masz (w systemie Ubuntu/Debian):

   ```bash
   sudo apt-get install screen
   ```

2. Uruchom nową sesję `screen`:

   ```bash
   screen -S mybot
   ```

3. Uruchom swój skrypt w tej sesji:

   ```bash
   python /ścieżka/do/skryptu.py
   ```

4. Aby odłączyć się od sesji `screen` (i pozostawić ją działającą w tle), naciśnij:

   ```
   Ctrl + A, a potem D
   ```

5. Aby wrócić do tej sesji:

   ```bash
   screen -r mybot
   ```

### 3. **Użycie `tmux`**:
`tmux` to kolejne narzędzie do tworzenia wirtualnych terminali, które pozwala na pracę w tle. Jest bardzo podobne do `screen`.

1. Zainstaluj `tmux` (w systemie Ubuntu/Debian):

   ```bash
   sudo apt-get install tmux
   ```

2. Uruchom nową sesję `tmux`:

   ```bash
   tmux new-session -s mybot
   ```

3. Uruchom swój skrypt w tej sesji:

   ```bash
   python /ścieżka/do/skryptu.py
   ```

4. Aby odłączyć się od sesji `tmux`, naciśnij:

   ```
   Ctrl + B, a potem D
   ```

5. Aby wrócić do tej sesji:

   ```bash
   tmux attach -t mybot
   ```

### 4. **Użycie `systemd` (jeśli chcesz, aby bot działał zawsze po restarcie systemu)**:
Jeśli chcesz, aby Twój bot działał nie tylko w tle, ale również po restarcie systemu, najlepiej użyć `systemd`. Będziesz musiał stworzyć jednostkę systemd dla swojego skryptu.

1. Utwórz plik jednostki systemd w katalogu `/etc/systemd/system/`, np. `mybot.service`.

2. W pliku `mybot.service` dodaj:

   ```ini
   [Unit]
   Description=My Telegram Bot
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /ścieżka/do/skryptu.py
   WorkingDirectory=/ścieżka/do/skryptu/
   Restart=always
   User=nazwa_użytkownika
   Group=nazwa_grupy

   [Install]
   WantedBy=multi-user.target
   ```

3. Zapisz plik i uruchom usługę:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start mybot
   sudo systemctl enable mybot
   ```

4. Aby sprawdzić status usługi:

   ```bash
   sudo systemctl status mybot
   ```

Dzięki tym rozwiązaniom bot będzie działał w tle, a jego działanie nie będzie zależne od stanu terminala. Wybierz metodę, która najlepiej pasuje do Twoich potrzeb.