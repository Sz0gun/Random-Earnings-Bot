**FCM Credentials** to dane uwierzytelniające, które pozwalają Twojej aplikacji na wysyłanie powiadomień push za pomocą **Firebase Cloud Messaging (FCM)**. FCM to usługa opracowana przez Google, która umożliwia aplikacjom mobilnym i internetowym wysyłanie powiadomień do użytkowników w czasie rzeczywistym.

### Co to są FCM Credentials?
FCM Credentials składają się z kluczy i identyfikatorów, które pozwalają Twojej aplikacji na komunikację z Firebase i wysyłanie powiadomień push. Zwykle obejmują:
- **Server Key (Klucz serwera)**: Służy do autoryzacji zapytań z Twojego serwera do usługi FCM. Używasz go, aby wysyłać wiadomości do urządzeń użytkowników.
- **Sender ID**: Jest to identyfikator, który jest powiązany z Twoim projektem Firebase, używany do identyfikacji Twojego konta w FCM.

### Jak uzyskać FCM Credentials?

Aby uzyskać **FCM credentials**, musisz przejść przez kilka kroków w konsoli Firebase. Oto jak to zrobić:

1. **Zaloguj się do Firebase Console**:
   - Przejdź do [Firebase Console](https://console.firebase.google.com/) i zaloguj się na swoje konto Google.

2. **Utwórz nowy projekt lub wybierz istniejący**:
   - Jeśli jeszcze nie masz projektu Firebase, kliknij "Add project" (Dodaj projekt) i postępuj zgodnie z instrukcjami, aby utworzyć nowy projekt.
   - Jeśli już masz projekt, wybierz go z listy.

3. **Wejdź w sekcję Cloud Messaging**:
   - Po utworzeniu lub wybraniu projektu, w lewym panelu wybierz **Project settings** (Ustawienia projektu).
   - Następnie przejdź do zakładki **Cloud Messaging**.

4. **Zdobądź Server Key i Sender ID**:
   - W sekcji **Cloud Messaging** znajdziesz swoje **Server Key** i **Sender ID**.
   - **Server Key**: Użyj go do autoryzacji zapytań w celu wysyłania powiadomień.
   - **Sender ID**: Jest wykorzystywany do identyfikacji Twojego projektu Firebase, gdy konfigurujesz aplikację kliencką.

5. **Konfiguracja w aplikacji**:
   - **Mobile App (np. Android/iOS)**: Zainstaluj SDK Firebase w swojej aplikacji i użyj tych credentials do wysyłania powiadomień push.
   - **Web App**: Jeśli używasz FCM w aplikacji webowej, również musisz skonfigurować Firebase SDK i dostarczyć credentials, aby móc odbierać powiadomienia push.

### Co robią te credentials?

- **Server Key**: Autoryzuje Twoje zapytania do serwera FCM, kiedy wysyłasz wiadomości push do użytkowników.
- **Sender ID**: Pomaga zidentyfikować Twoje konto Firebase, gdy konfigurowane są aplikacje mobilne (np. Android) lub aplikacje internetowe, które będą odbierały powiadomienia push.

### Bezpieczeństwo FCM Credentials
- **Trzymaj je w tajemnicy**: Server Key jest kluczowym elementem autoryzacji, dlatego nie powinno się go udostępniać publicznie.
- **Używaj środowisk zabezpieczonych**: Klucze FCM powinny być przechowywane w bezpieczny sposób (np. w zmiennych środowiskowych) i nie powinny być zawarte bezpośrednio w kodzie aplikacji, szczególnie w przypadku publicznego repozytorium.

### Podsumowanie
**FCM Credentials** (Server Key i Sender ID) to dane uwierzytelniające, które pozwalają aplikacjom wysyłać powiadomienia push za pomocą usługi **Firebase Cloud Messaging**. Są one dostępne w konsoli Firebase i muszą być używane w aplikacjach do autoryzacji połączeń z serwerem FCM.