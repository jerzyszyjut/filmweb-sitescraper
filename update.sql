USE filmy;

SELECT * FROM kraje;
SELECT * FROM uzytkownicy_platformy INNER JOIN zalozono_w ON uzytkownicy_platformy.email = zalozono_w.uzytkownicy_platformy_email WHERE zalozono_w.kraje_nazwa = 'Nowa Zelandia';
DELETE FROM kraje WHERE nazwa = 'Nowa Zelandia';
SELECT * FROM kraje;
SELECT * FROM uzytkownicy_platformy INNER JOIN zalozono_w ON uzytkownicy_platformy.email = zalozono_w.uzytkownicy_platformy_email WHERE zalozono_w.kraje_nazwa = 'Nowa Zelandia';
SELECT * FROM uzytkownicy_platformy WHERE email = 'wolochkacper@example.com';


SELECT * FROM filmy INNER JOIN obejrzane_tytuly ON filmy.id = obejrzane_tytuly.filmy_id WHERE obejrzane_tytuly.uzytkownicy_platformy_email = 'wolochkacper@example.com';
UPDATE uzytkownicy_platformy SET email = 'wolochkacper@example.com_updated' WHERE email = 'wolochkacper@example.com';
SELECT * FROM filmy INNER JOIN obejrzane_tytuly ON filmy.id = obejrzane_tytuly.filmy_id WHERE obejrzane_tytuly.uzytkownicy_platformy_email = 'wolochkacper@example.com_updated';
