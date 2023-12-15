USE filmy;
CREATE TABLE filmy (
    id INT IDENTITY(1, 1),
    tytul VARCHAR(255) NOT NULL,
    oryginalny_tytul VARCHAR(255) NOT NULL,
    premiera DATE CHECK (premiera > '1895-01-01') NOT NULL,
    czas_trwania INT CHECK (czas_trwania > 0) NOT NULL,
    okladka VARCHAR(2048) CHECK (
        okladka LIKE 'https://%'
        OR okladka LIKE 'http://%'
    ) NULL,
    zwiastun VARCHAR(2048) CHECK (
        zwiastun LIKE 'https://%'
        OR zwiastun LIKE 'http://%'
    ) NULL,
    PRIMARY KEY (id)
);
CREATE TABLE pracownicy_filmowi (
    id INT IDENTITY(1, 1),
    imie VARCHAR(255) NOT NULL,
    nazwisko VARCHAR(255) NOT NULL,
    data_urodzenia DATE CHECK (data_urodzenia < GETDATE()) NOT NULL,
    data_smierci DATE CHECK (data_smierci < GETDATE()) NULL,
    plec CHAR(1) CHECK (plec like 'M' OR plec like 'K') NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE kraje (
    nazwa VARCHAR(63) CHECK (nazwa LIKE '[A-Z][a-z]%') NOT NULL,
    PRIMARY KEY (nazwa)
);
CREATE TABLE uzytkownicy_platformy (
    email VARCHAR(255) CHECK (email LIKE '%@%.%') NOT NULL,
    nick VARCHAR(20) NOT NULL,
    imie VARCHAR(255) NOT NULL,
    nazwisko VARCHAR(255) NOT NULL,
    awatar VARCHAR(2048) CHECK (
        awatar LIKE 'https://%'
        OR awatar LIKE 'http://%'
    ) NULL,
    data_urodzenia DATE CHECK (data_urodzenia < GETDATE()) NOT NULL,
    haslo VARCHAR(255) NOT NULL,
    zweryfikowano_email BIT NOT NULL,
    PRIMARY KEY (email)
);
CREATE TABLE gatunki (
    nazwa VARCHAR(255) NOT NULL,
    PRIMARY KEY (nazwa)
);
CREATE TABLE nalezace_gatunki (
    filmy_id INT NOT NULL,
    gatunki_nazwa VARCHAR(255) NOT NULL,
    FOREIGN KEY (filmy_id) REFERENCES filmy(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (gatunki_nazwa) REFERENCES gatunki(nazwa) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (filmy_id, gatunki_nazwa)
);
CREATE TABLE certyfikaty_wiekowe (
    id INT IDENTITY(1, 1),
    nazwa VARCHAR(255) NOT NULL,
    wiek INT CHECK (
        wiek > 1
        AND wiek <= 18
    ) NOT NULL,
    kraje_nazwa VARCHAR(63) NOT NULL,
    FOREIGN KEY (kraje_nazwa) REFERENCES kraje(nazwa) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (id),
);
CREATE TABLE posiadane_certyfikaty_wiekowe (
    filmy_id INT NOT NULL,
    certyfikaty_wiekowe_id INT NOT NULL,
    FOREIGN KEY (filmy_id) REFERENCES filmy(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (certyfikaty_wiekowe_id) REFERENCES certyfikaty_wiekowe(id) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (filmy_id, certyfikaty_wiekowe_id)
);
CREATE TABLE funkcje_w_filmie (
    nazwa_funkcji VARCHAR(255) NOT NULL,
    filmy_id INT NOT NULL,
    pracownicy_filmowi_id INT NOT NULL,
    FOREIGN KEY (filmy_id) REFERENCES filmy(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (pracownicy_filmowi_id) REFERENCES pracownicy_filmowi(id) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (nazwa_funkcji, filmy_id, pracownicy_filmowi_id)
);
CREATE TABLE narodowosc (
    pracownicy_filmowi_id INT NOT NULL,
    kraje_nazwa VARCHAR(63) NOT NULL,
    FOREIGN KEY (pracownicy_filmowi_id) REFERENCES pracownicy_filmowi(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (kraje_nazwa) REFERENCES kraje(nazwa) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (pracownicy_filmowi_id, kraje_nazwa)
);
CREATE TABLE oceny (
    filmy_id INT NOT NULL,
    uzytkownicy_platformy_email VARCHAR(255) NOT NULL,
    ocena INT CHECK (
        ocena >= 1
        AND ocena <= 10
    ) NOT NULL,
    recenzja VARCHAR(255) NULL,
    FOREIGN KEY (filmy_id) REFERENCES filmy(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (uzytkownicy_platformy_email) REFERENCES uzytkownicy_platformy(email) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (filmy_id, uzytkownicy_platformy_email)
);
CREATE TABLE obejrzane_tytuly (
    czas INT NOT NULL,
    filmy_id INT NOT NULL,
    uzytkownicy_platformy_email VARCHAR(255) NOT NULL,
    FOREIGN KEY (filmy_id) REFERENCES filmy(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (uzytkownicy_platformy_email) REFERENCES uzytkownicy_platformy(email) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (filmy_id, uzytkownicy_platformy_email)
);
CREATE TABLE wyprodukowano_film_w (
    filmy_id INT NOT NULL,
    kraje_nazwa VARCHAR(63) NOT NULL,
    FOREIGN KEY (filmy_id) REFERENCES filmy(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (kraje_nazwa) REFERENCES kraje(nazwa) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (filmy_id, kraje_nazwa)
);
CREATE TABLE krytycy_filmowi (
    uzytkownicy_platformy_email VARCHAR(255) NOT NULL,
    data_przyznania_statusu_krytyka DATE CHECK (data_przyznania_statusu_krytyka < GETDATE()) NOT NULL,
    data_odebrania_statusu_krytyka DATE CHECK (data_odebrania_statusu_krytyka < GETDATE()) NULL,
    FOREIGN KEY (uzytkownicy_platformy_email) REFERENCES uzytkownicy_platformy(email) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (uzytkownicy_platformy_email)
);
CREATE TABLE zalozono_w (
    uzytkownicy_platformy_email VARCHAR(255) NOT NULL,
    kraje_nazwa VARCHAR(63) NOT NULL,
    FOREIGN KEY (uzytkownicy_platformy_email) REFERENCES uzytkownicy_platformy(email) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (kraje_nazwa) REFERENCES kraje(nazwa) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (uzytkownicy_platformy_email, kraje_nazwa)
);