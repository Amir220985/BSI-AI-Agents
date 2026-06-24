#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lint_process.py — Statischer Linter für BSI-CustomerSuite-Prozess-Exporte.

Prüft jeden `crm.ProcessTransfer` in einem entpackten Export gegen die
Design-Rules / Anti-Patterns der Wissensbasis (../knowledge).

Aufruf:
    python3 tools/lint_process.py <pfad-zum-export-ordner> [--json] [--min-severity WARN]
    python3 tools/lint_process.py examples/bsi-crm-2026-06-24_15-09-39

Der Export-Ordner muss `codes/Prozess-45831/*.json` enthalten; `lambda-bindings/`
wird – falls vorhanden – zur sicheren Erkennung von Schnittstellen-Steps genutzt.

Exit-Code: 0 = keine ERRORs, 1 = mindestens ein ERROR gefunden.

Geprüfte Regeln (Verweis auf knowledge/bsi_process_design_rules.md & process_anti_patterns.md):
  R1  Start- und End-Step vorhanden; keine offenen/ungültigen Outlets; keine Sackgassen
  R2/AP7  Prozesse > GROUP_THRESHOLD Steps ohne Gruppen
  R3/AP2  Monolith-Warnung ab MONOLITH_THRESHOLD Steps
  R5/AP5  Schnittstellen-/Lambda-Step ohne behandelten Fehlerpfad
  R6/AP9  Entscheidungs-/Lambda-Step ohne fachliche notes; nur generische Outlet-Labels
  R8/AP1  Benennung: Tippfehler/auffällige Zeichen; Steps ohne Namen
  --      Leere Verzweigung (mehrere Outlets auf dasselbe Ziel)
  --      Unerreichbare Steps (nicht vom Start aus erreichbar)
"""
import json, os, sys, glob, re, argparse
from collections import deque, defaultdict

DE_LANG = "1;112192;106064;j246;j71099"      # Sprach-UID Deutsch (in den Beispielen)

# Step-Typen (abgeleitet, siehe knowledge/bsi_step_type_catalog.md)
TID_START   = "201503"
TID_END     = "201504"
TID_LAMBDA  = {"209754"}                       # synchroner Lambda-/Schnittstellenaufruf
TID_BG      = {"216266"}                        # Hintergrund-Versand/Erstellung (asynchron)
TID_CRIT    = {"209153", "107779"}             # Kriterien-/Entscheidungs-Step
TID_ERRINFO = {"138297", "168173"}             # Info-/Fehler-/Hinweis-Steps

# Schwellwerte
GROUP_THRESHOLD    = 8
MONOLITH_THRESHOLD = 40
BFS_DEPTH          = 5

# Heuristiken
RE_ERR_HINT = re.compile(r'fehler|abbruch|manuell|nachbearbeit|prüf|techn|nicht erfolg|nicht geladen|'
                         r'nicht durchgeführt|ablehn|wiederhol|retry|eskal|gesperrt', re.I)
RE_SUCCESS  = re.compile(r'erfolgreich|erfolg|geklappt|fehler|gültig|vorhanden|zugewiesen|'
                         r'gesperrt|abgeschlossen|geladen|durchgeführt', re.I)
RE_GENERIC_LABEL = re.compile(r'^[A-Z]$')      # Outlet-Label nur "A"/"B"/"C"

# Benennungs-Lint: kuratierte Tippfehler aus dem Datensatz + strukturelle Auffälligkeiten
KNOWN_TYPOS = ["sStart", "Vetrag", "Vetrags", "Beschwerdeführe ", "Kontakdaten",
               "Starkommunikation", "Empfangbestätigung", "adress-"]
RE_DOUBLE_SPACE = re.compile(r"  +")
RE_DOUBLE_PAREN = re.compile(r"\)\)|\(\(")
RE_TRAILING_WS  = re.compile(r"^\s|\s$")


class Finding:
    __slots__ = ("severity", "rule", "step", "msg")
    def __init__(self, severity, rule, step, msg):
        self.severity, self.rule, self.step, self.msg = severity, rule, step, msg
    def as_dict(self):
        return {"severity": self.severity, "rule": self.rule, "step": self.step, "msg": self.msg}


def de_name(items):
    for li in items or []:
        if li.get("languageUid") == DE_LANG and li.get("name"):
            return li["name"]
    for li in items or []:
        if li.get("name"):
            return li["name"]
    return None


def gid_from_primary(key):
    m = re.search(r's([0-9a-f\-]{36})', key or "")
    return m.group(1) if m else None


def load_lambda_gids(export_dir):
    gids = set()
    for f in glob.glob(os.path.join(export_dir, "lambda-bindings", "*.json")):
        try:
            j = json.load(open(f, encoding="utf-8"))
        except Exception:
            j = {}
        cid = j.get("lambdaConsumerId", "") or ""
        m = re.search(r'invokeLambdaProcessStep:([0-9a-f\-]{36})', cid)
        if m:
            gids.add(m.group(1))
        m2 = re.search(r'crminvokeLambdaProcessStep([0-9a-f\-]{36})', os.path.basename(f))
        if m2:
            gids.add(m2.group(1))
    return gids


def build_graph(ptransfer):
    """Liefert (name, nodes_by_id, groups).

    Outlet-Ziele werden auf zwei Wegen aufgelöst:
      1. direkt über `targetProcessStepId`
      2. falls null: über geteilte `descriptorId` – ein Outlet ohne eigenes Ziel
         erbt das Ziel eines Geschwister-Outlets mit gleicher descriptorId.
    Pro Outlet wird die Liste effektiver Ziele (`targets`) und ein `open`-Flag
    (kein Ziel auflösbar) gespeichert.
    """
    pc = ptransfer["processConfig"]
    defs = ptransfer["processStepDefinitions"]
    sdef = {gid_from_primary(sd.get("primaryStepIdKey")): sd for sd in defs}

    # descriptorId -> Menge real verbundener Ziele (für Vererbung)
    desc2tgt = defaultdict(set)
    for s in pc["processSteps"]:
        for o in s.get("outlets", []):
            if o.get("targetProcessStepId") and o.get("descriptorId"):
                desc2tgt[o["descriptorId"]].add(o["targetProcessStepId"])

    nodes = {}
    for s in pc["processSteps"]:
        sd = sdef.get(s.get("gid"))
        name = de_name(sd.get("languageItems")) if sd else None
        outlets = []
        for o in s.get("outlets", []):
            tgt = o.get("targetProcessStepId")
            if tgt:
                targets = [tgt]
            elif o.get("descriptorId") and desc2tgt.get(o["descriptorId"]):
                targets = sorted(desc2tgt[o["descriptorId"]])   # über descriptorId vererbt
            else:
                targets = []                                    # echt offen
            outlets.append({"label": o.get("configurationName"),
                            "targets": targets,
                            "open": not targets})
        nodes[s["id"]] = {
            "id": s["id"], "gid": s.get("gid"), "tid": s.get("typeId"),
            "name": name or s.get("name"),
            "outlets": outlets,
            "notes": (sd.get("notes") if sd else None),
        }
    return pc.get("name"), nodes, pc.get("processStepGroups", [])


def node_targets(node):
    """Alle effektiven Zielknoten-IDs eines Steps (über alle Outlets)."""
    out = []
    for o in node["outlets"]:
        out.extend(o["targets"])
    return out


def reachable_from(start_ids, nodes):
    seen = set()
    q = deque(start_ids)
    while q:
        cid = q.popleft()
        if cid in seen or cid not in nodes:
            continue
        seen.add(cid)
        for t in node_targets(nodes[cid]):
            q.append(t)
    return seen


def has_error_handling(node, nodes):
    """OK, wenn ein Erfolgs-/Fehlerkriterium binnen BFS_DEPTH erreichbar ist
    ODER der Step selbst differenzierte Ausgänge (einer Richtung Fehler-Info) hat."""
    real = node_targets(node)
    distinct = set(real)
    # (1) eigene Ausgänge: nachgelagerter Fehler-Info- oder Kriterien-Step
    for t in real:
        tn = nodes.get(t, {})
        if tn.get("tid") in TID_ERRINFO and tn.get("name") and RE_ERR_HINT.search(tn["name"]):
            return True, f"Fehlerzweig am Step: '{tn['name']}'"
        if tn.get("tid") in TID_CRIT:
            return True, f"Kriterien-Step '{tn.get('name')}'"
    # (2) Vorwärts-BFS auf Erfolgs-Kriterium mit ≥2 verschiedenen Zielen
    seen = {node["id"]}
    q = deque((t, 1) for t in real)
    while q:
        cid, d = q.popleft()
        if cid in seen or d > BFS_DEPTH:
            continue
        seen.add(cid)
        cn = nodes.get(cid)
        if not cn:
            continue
        if cn["tid"] in TID_CRIT and cn["name"] and RE_SUCCESS.search(cn["name"]):
            if len(set(node_targets(cn))) >= 2:
                return True, f"Erfolgskontrolle '{cn['name']}'"
        for t in node_targets(cn):
            q.append((t, d + 1))
    # (3) keine Differenzierung
    if len(distinct) <= 1:
        return False, "alle Ausgänge führen zum selben Ziel – keine Fehlerdifferenzierung"
    return False, "kein Erfolgs-/Fehlerkriterium erreichbar"


def naming_issues(text):
    if not text:
        return []
    out = []
    for typo in KNOWN_TYPOS:
        if typo.lower() in text.lower():
            out.append(f"möglicher Tippfehler '{typo.strip()}'")
    if RE_DOUBLE_SPACE.search(text):
        out.append("doppeltes Leerzeichen")
    if RE_DOUBLE_PAREN.search(text):
        out.append("doppelte Klammer")
    if RE_TRAILING_WS.search(text):
        out.append("führendes/abschließendes Leerzeichen")
    return out


def lint_process(ptransfer, lambda_gids):
    name, nodes, groups = build_graph(ptransfer)
    F = []
    add = lambda sev, rule, step, msg: F.append(Finding(sev, rule, step, msg))

    nstep = len(nodes)
    starts = [n["id"] for n in nodes.values() if n["tid"] == TID_START]
    ends   = [n["id"] for n in nodes.values() if n["tid"] == TID_END]

    # R1: Start/End
    if not starts:
        add("ERROR", "R1", None, "Kein Start-Step (201503) vorhanden.")
    if not ends:
        add("ERROR", "R1", None, "Kein End-Step (201504) vorhanden.")

    # R1: offene/ungültige Outlets + leere Verzweigung
    for n in nodes.values():
        open_outlets = [o["label"] for o in n["outlets"] if o["open"]]
        if open_outlets and n["tid"] != TID_END:
            add("ERROR", "R1", n["name"],
                f"{len(open_outlets)} Outlet(s) ohne auflösbares Ziel (weder targetProcessStepId "
                f"noch descriptorId): {'/'.join(str(l) for l in open_outlets)}.")
        for o in n["outlets"]:
            for t in o["targets"]:
                if t not in nodes:
                    add("ERROR", "R1", n["name"], f"Outlet '{o['label']}' zeigt auf nicht existierenden Step.")
        # leere Verzweigung: ≥2 Outlets, alle auf dasselbe Ziel
        tgts = node_targets(n)
        if len(tgts) >= 2 and len(set(tgts)) == 1:
            add("WARN", "LINT", n["name"], f"Leere Verzweigung: {len(tgts)} Ausgänge auf dasselbe Ziel.")
        # Sackgasse: Nicht-End-Step ohne Ausgänge
        if not n["outlets"] and n["tid"] != TID_END:
            add("WARN", "R1", n["name"], "Sackgasse: Step ohne Ausgang (kein End-Step).")

    # Unerreichbarkeit
    if starts:
        reach = reachable_from(starts, nodes)
        for n in nodes.values():
            if n["id"] not in reach and n["tid"] != TID_START:
                add("WARN", "R1", n["name"], "Step ist vom Start aus nicht erreichbar.")

    # R2/AP7: Gruppen
    if nstep > GROUP_THRESHOLD and not groups:
        add("WARN", "R2", None, f"{nstep} Steps ohne Gruppen (Empfehlung ab >{GROUP_THRESHOLD}).")

    # R3/AP2: Monolith
    if nstep >= MONOLITH_THRESHOLD:
        add("INFO", "R3", None, f"Monolith-Verdacht: {nstep} Steps – Auslagerung in Subprozesse prüfen.")

    # R5/AP5: Schnittstellen-Fehlerpfade
    for n in nodes.values():
        is_lambda = n["gid"] in lambda_gids or n["tid"] in TID_LAMBDA
        is_bg = n["tid"] in TID_BG
        if is_bg and not is_lambda:
            add("INFO", "R5", n["name"], "Hintergrund-/Async-Step: Fehlerbehandlung außerhalb des Flows verifizieren.")
            continue
        if not is_lambda:
            continue
        ok, why = has_error_handling(n, nodes)
        if ok:
            add("INFO", "R5", n["name"], f"Schnittstelle abgesichert ({why}).")
        else:
            add("ERROR", "R5", n["name"], f"Schnittstellen-/Lambda-Step ohne behandelten Fehlerpfad: {why}.")

    # R6/AP9: notes + generische Labels an Entscheidungs-/Lambda-Steps
    for n in nodes.values():
        decisionlike = n["tid"] in TID_CRIT or n["tid"] in TID_LAMBDA or n["gid"] in lambda_gids
        if not decisionlike:
            continue
        if not n["notes"]:
            add("INFO", "R6", n["name"], "Entscheidungs-/Schnittstellen-Step ohne fachliche notes.")
        labels = [o["label"] for o in n["outlets"] if o["targets"] and o["label"]]
        if n["tid"] in TID_CRIT and labels and all(RE_GENERIC_LABEL.match(l) for l in labels):
            add("INFO", "R6", n["name"], f"Nur generische Outlet-Labels ({'/'.join(labels)}) – sprechende Labels empfohlen.")

    # R8/AP1: Benennung
    for n in nodes.values():
        if n["name"] is None and n["tid"] not in (TID_START, TID_END):
            add("INFO", "R8", None, f"Step ohne Namen (typeId {n['tid']}).")
        for issue in naming_issues(n["name"]):
            add("WARN", "R8", n["name"], issue)
    for g in groups:
        for issue in naming_issues(g.get("name")):
            add("WARN", "R8", g.get("name"), f"Gruppenname: {issue}")
    for issue in naming_issues(name):
        add("WARN", "R8", name, f"Prozessname: {issue}")

    return name, nstep, F


def main():
    ap = argparse.ArgumentParser(description="BSI Prozess-Export Linter")
    ap.add_argument("export_dir", help="Pfad zum entpackten Export-Ordner")
    ap.add_argument("--json", action="store_true", help="Ergebnis als JSON ausgeben")
    ap.add_argument("--min-severity", choices=["ERROR", "WARN", "INFO"], default="INFO")
    args = ap.parse_args()

    proc_dir = os.path.join(args.export_dir, "codes", "Prozess-45831")
    files = sorted(glob.glob(os.path.join(proc_dir, "*.json")))
    if not files:
        print(f"FEHLER: keine Prozessdateien unter {proc_dir}", file=sys.stderr)
        sys.exit(2)

    lambda_gids = load_lambda_gids(args.export_dir)
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    minlvl = order[args.min_severity]

    results = []
    totals = defaultdict(int)
    for fp in files:
        try:
            d = json.load(open(fp, encoding="utf-8"))
        except Exception as e:
            print(f"FEHLER beim Parsen {os.path.basename(fp)}: {e}", file=sys.stderr)
            continue
        if d.get("_type") != "crm.ProcessTransfer":
            continue
        name, nstep, findings = lint_process(d, lambda_gids)
        for f in findings:
            totals[f.severity] += 1
        results.append({"name": name, "nsteps": nstep,
                        "findings": [f.as_dict() for f in findings]})

    if args.json:
        print(json.dumps({"summary": dict(totals), "processes": results},
                         ensure_ascii=False, indent=1))
        sys.exit(1 if totals.get("ERROR") else 0)

    icon = {"ERROR": "❌", "WARN": "⚠️ ", "INFO": "ℹ️ "}
    print(f"BSI Prozess-Linter — {len(results)} Prozesse, Export: {os.path.basename(args.export_dir.rstrip('/'))}")
    print(f"Summe: {totals.get('ERROR',0)} ERROR · {totals.get('WARN',0)} WARN · {totals.get('INFO',0)} INFO\n")
    for r in results:
        shown = [f for f in r["findings"] if order[f["severity"]] <= minlvl]
        if not shown:
            continue
        ne = sum(1 for f in r["findings"] if f["severity"] == "ERROR")
        nw = sum(1 for f in r["findings"] if f["severity"] == "WARN")
        print(f"## {r['name']}  [{r['nsteps']} Steps · {ne}E/{nw}W]")
        for f in shown:
            step = f" «{f['step']}»" if f["step"] else ""
            print(f"  {icon[f['severity']]}[{f['rule']}]{step}: {f['msg']}")
        print()
    sys.exit(1 if totals.get("ERROR") else 0)


if __name__ == "__main__":
    main()
