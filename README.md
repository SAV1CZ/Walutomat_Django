Walutomat Django

REST API aplikacji symulującej działanie kantoru internetowego.
Aplikacja umożliwia wymianę walut pomiędzy portfelami użytkowników na podstawie aktualnych kursów pobieranych z zewnętrznego API.
Generator użytkowników pozwala symulować działanie walutomatu i obsługę wielu transakcji. 
System automatycznie nalicza marżę od każdej wymiany, a uzyskany przychód księguje na koncie instytucji w odpowiedniej walucie.
Każda transakcja jest zapisywana w bazie danych wraz z dokładnym czasem jej wykonania (UTC).
Modele aplikacji wykorzystują relacje bazodanowe zapewniające spójność powiązań pomiędzy użytkownikami, portfelami, walutami i transakcjami


Technologie

*Python
*Django i REST Framework
*PostgreSQL
*Docker / Docker Compose
*JWT (Simple JWT)
*Swagger

Funkcjonalności

*Rejestracja i uwierzytelnianie użytkowników,
*Wymiana walut pomiędzy portfelami użytkownika,
*Przelewy na konta innych użytkowników o tej samej walucie bazowej,
*Pobieranie kursów walut z zewnętrznego API,
*Automatyczny mechanizm pobierania marży walutomatu. 


