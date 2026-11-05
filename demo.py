# -*- coding: utf-8 -*-
"""Prova offline del Radar: dati finti, nessuna rete, nessuna chiave.

Lancia:  python radar.py --demo
Serve a vedere come appaiono le notifiche e a capire come ragiona il punteggio.
Tutti i titoli sono inventati e iniziano con [DEMO].
"""
import datetime as dt

import radar


def _it(source, lang, tier, category, title, summary, minutes_ago, now, own=False, n=[0]):
    n[0] += 1
    pub = now - dt.timedelta(minutes=minutes_ago)
    return radar.Item(
        id="demo%03d" % n[0], title=title, link="https://example.com/demo/%d" % n[0], summary=summary,
        published=pub, source=source, lang=lang, tier=tier, category=category, own=own,
        tokens=radar.title_tokens(title))


def demo_items(now):
    return [
        # stessa notizia su 3 testate (una italiana): sale la saturazione, il punteggio scende
        _it("Deadline", "en", "trade", "film", "[DEMO] Avengers: Doomsday trailer reveals first look at Doctor Doom",
            "The first official trailer has been released, with a first look at Doctor Doom.", 22, now),
        _it("Variety", "en", "trade", "film", "[DEMO] Avengers: Doomsday first trailer arrives with Doctor Doom",
            "A first trailer is out, confirming the villain's role.", 15, now),
        _it("Movieplayer.it", "it", "major", "film", "[DEMO] Avengers: Doomsday, ecco il trailer con Doctor Doom",
            "Il primo trailer ufficiale è online.", 6, now),
        # notizia fresca, una sola fonte: dovrebbe scattare la notifica
        _it("Anime News Network", "en", "trade", "anime", "[DEMO] One Piece anime confirms new arc release date for 2027",
            "The production committee confirms the premiere date and announces the new cast.", 25, now),
        # annuncio enorme e ufficiale: notifica forzata
        _it("Anime News Network", "en", "trade", "manga", "[DEMO] Celebre mangaka muore a 81 anni, lo annuncia la casa editrice",
            "The publisher confirms that the author passes away after a long illness.", 35, now),
        # rumor: punteggio basso
        _it("VGC", "en", "major", "videogiochi", "[DEMO] Rumor: Nintendo reportedly preparing a new console bundle for the holidays",
            "An unconfirmed leak suggests a bundle may be planned.", 40, now),
        # offerta: esclusa dal filtro prima ancora di arrivare all'LLM
        _it("Polygon", "en", "major", "videogiochi", "[DEMO] Best Black Friday deals on LEGO Marvel sets",
            "Save big on sets.", 50, now),
        # notizia che la nostra testata ha già pubblicato: nessuna notifica
        _it("Collider", "en", "major", "anime", "[DEMO] Berserk new anime adaptation announces studio and cast",
            "The studio and cast of the new anime are announced.", 55, now),
        _it("LA NOSTRA TESTATA", "it", "official", "anime", "[DEMO] Berserk, nuovo anime: annunciati studio e cast",
            "Articolo già pubblicato da noi.", 20, now, own=True),
    ]


def mock_rate(clusters, now):
    """Rating a parole chiave, solo per la demo / per --mock. Quello vero lo fa l'LLM."""
    out = {}
    for c in clusters:
        rep = c.rep
        text = (rep.title + " " + rep.summary).lower()
        impact = 5.0
        for kw, v in [("trailer", 2.5), ("release date", 2.5), ("confirm", 1.0), ("announce", 1.5), ("cast", 0.5),
                      ("passes away", 4.0), ("muore", 4.0), ("delay", 2.0), ("cancel", 2.5), ("bundle", 0.5)]:
            if kw in text:
                impact += v
        big = ["avengers", "one piece", "marvel", "star wars", "dragon ball", "nintendo", "playstation", "berserk", "mangaka"]
        hit = any(b in text for b in big)
        rumor = any(k in text for k in ["rumor", "reportedly", "leak", "indiscrezione"])
        if "passes away" in text or "muore" in text:
            rel = "ufficiale"
        elif rumor:
            rel = "rumor"
        elif rep.tier == "trade":
            rel = "trade"
        else:
            rel = "stampa"
        raw = {
            "id": c.cid, "ignore": False, "category": rep.category, "reliability": rel,
            "impact": min(10, impact), "audience_fit": 8.5 if hit else 5.5, "traffic": 8.0 if hit else 5.0,
            "headline_it": rep.title.replace("[DEMO] ", "") if rep.lang == "it" else "(demo) " + rep.title.replace("[DEMO] ", ""),
            "why": "Valutazione di prova basata su parole chiave: in produzione la fa l'LLM leggendo la notizia.",
            "angle": "News breve con link alla fonte e un paragrafo di contesto.",
            "franchise": "",
        }
        r = radar.normalize_rating(raw)
        out[r["id"]] = r
    return out


def run_demo(cfg):
    now = radar.now_utc()
    cfg = radar.deep_merge(cfg, {"quiet_hours": {"enabled": False}, "digest": {"enabled": True, "hour": 0}})
    state = radar.new_state()
    state["_new"] = False
    notifier = radar.Notifier(dry=True)
    items = demo_items(now)

    print("=" * 60)
    print("DEMO — dati inventati, nessuna rete, nessuna chiave")
    print("Soglia notifica: %s · riepilogo sotto %s" % (cfg["thresholds"]["notify"], cfg["thresholds"]["notify"]))
    print("=" * 60)
    stats = radar.process(items, cfg, state, now, lambda cl: mock_rate(cl, now), notifier)
    print("\nPrimo passaggio:", {k: v for k, v in stats.items() if v})
    stats2 = radar.process(items, cfg, state, now, lambda cl: mock_rate(cl, now), notifier)
    print("Secondo passaggio (stesse notizie, nessun duplicato atteso):", {k: v for k, v in stats2.items() if v} or "nessuna novità")
    print("\nRiepilogo serale (di solito parte alle %d:00):" % cfg["digest"]["hour"])
    radar.maybe_send_digest(cfg, state, now, notifier, force=True)
    return 0
