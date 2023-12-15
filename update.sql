USE filmy;

SELECT * FROM kraje;
SELECT * FROM uzytkownicy_platformy INNER JOIN zalozono_w ON uzytkownicy_platformy.email = zalozono_w.uzytkownicy_platformy_email WHERE zalozono_w.kraje_nazwa = 'Nowa Zelandia';
SELECT * FROM certyfikaty_wiekowe WHERE kraje_nazwa = 'Nowa Zelandia';
DELETE FROM kraje WHERE nazwa = 'Nowa Zelandia';
SELECT * FROM kraje;
SELECT * FROM uzytkownicy_platformy INNER JOIN zalozono_w ON uzytkownicy_platformy.email = zalozono_w.uzytkownicy_platformy_email WHERE zalozono_w.kraje_nazwa = 'Nowa Zelandia';
SELECT * FROM uzytkownicy_platformy WHERE email = 'kornel89@example.net';
SELECT * FROM certyfikaty_wiekowe WHERE kraje_nazwa = 'Nowa Zelandia';


SELECT * FROM filmy INNER JOIN obejrzane_tytuly ON filmy.id = obejrzane_tytuly.filmy_id WHERE obejrzane_tytuly.uzytkownicy_platformy_email = 'kornel89@example.net';
UPDATE uzytkownicy_platformy SET email = 'kornel89@example.net_updated' WHERE email = 'kornel89@example.net';
SELECT * FROM filmy INNER JOIN obejrzane_tytuly ON filmy.id = obejrzane_tytuly.filmy_id WHERE obejrzane_tytuly.uzytkownicy_platformy_email = 'kornel89@example.net_updated';
