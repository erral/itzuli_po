# Itzuli PO

Itzuli PO, PO formatuko fitxategiak euskararako itzultzaile automatikoetatik pasatzeko scripta da.

Inspirazioa [@gailapa](https://mastodon.eus/@galaipa@mastodon.jalgi.eus) eta [@urtzai](https://mastodon.eus/@urtzai/) erabitlzaileek [hasitako harian](https://mastodon.eus/@urtzai/111870223636030746) eta [@mgoiogana](https://mastodon.eus/@mgoiogana) erabiltzailearen [eskaeran](https://mastodon.eus/@mgoiogana/111903123557988154) dago.

Helburua, software jakin baten itzulpena era automatikoan egitean datza.

Horretarako nik aurrez sortutako [YogiTea mezu-txiokatzailea](https://github.com/erral/yogitea-txiokatzailea/) proiektuan erabilitako scriptak berrerabili ditut [elia.eus](https://elia.eus), [batua.eus](https://batua.eus) eta [itzuli](https://www.euskadi.eus/itzuli/) web zerbitzuak ingelesezko mezuak euskarara itzultzeko.

## Nola erabili

1. Lehenengo dependentziak instalatu:

```python
pip install -r requirements.txt
```

2. Ondoren itzuli behar den fitxategia lortu.

3. Azkenik scripta exekutatu fitxategiaren izena eta erabili beharreko zerbitzua parametro gisa pasatuz. Azken honetarako 3 aukera dituzu, batua, itzuli edo elia:

```bash
python itzuli.py fitxategia.po itzuli
```

Itzulpena egiteko erabiltzen den zerbitzu bakoitzeko fitxategi bat sortuko du: `eliaeus.po`, `batuaeus.po` eta `itzulieus.po`.

## OHARRA

Hau ez da software itzulpenak egiteko modu zuzena.

Gainera, itzulpenak egiteko erabiltzen ari garen zerbitzuen baldintzak urratzen ari gaitezke erabilera masibo bat egiten ari garelako. Adi beraz, litekeena da-eta zerbitzu horiek scripta _baneatzea_.

Erabili zure kontura.
