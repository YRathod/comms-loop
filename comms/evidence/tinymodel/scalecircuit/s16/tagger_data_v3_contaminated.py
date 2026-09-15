"""Synthetic pairs for the tagger fine-tune: an English-lite question -> the mini-language tag.

Source side: relation phrasings (nominal forms that wrap an inner phrase, question forms for the
outermost hop), realistic entity spans (people, films, places, organisations, songs), optional
filter clauses, crowd-style noise (lowercasing, trailing "?" dropped, run-on lead-ins), and
comparison / two-thing questions that map to NA. The model's own outputs never enter the data.

    .venv\\Scripts\\python scripts/tagger_data.py --n 20000 --out data/tagger_train.jsonl
"""
import argparse
import json
import random

RELS = {
    "father": (["the father of {x}", "{x}'s father"], ["Who is the father of {x}?", "Who was {x}'s father?"]),
    "mother": (["the mother of {x}", "{x}'s mother"], ["Who is the mother of {x}?", "Who was {x}'s mother?"]),
    "parent": (["a parent of {x}", "the parents of {x}"], ["Who are the parents of {x}?", "Who is a parent of {x}?"]),
    "spouse": (["the spouse of {x}", "the wife of {x}", "the husband of {x}", "the person married to {x}"], ["Who is {x} married to?", "Who is the spouse of {x}?"]),
    "child": (["a child of {x}", "the son of {x}", "the daughter of {x}"], ["Who is the child of {x}?", "Name a child of {x}."]),
    "brother": (["the brother of {x}", "a sibling of {x}"], ["Who is the brother of {x}?", "Who is a sibling of {x}?"]),
    "sister": (["the sister of {x}"], ["Who is the sister of {x}?"]),
    "director": (["the director of {x}", "the man who directed {x}", "the person who directed {x}", "the man who also did {x}", "the filmmaker behind {x}", "the person behind the camera on {x}", "who helmed {x}"],
                 ["Who directed {x}?", "Who was the director of {x}?", "{x} was directed by whom?"]),
    "writer": (["the author of {x}", "the writer of {x}", "the person who wrote {x}", "the novelist behind {x}"],
               ["Who wrote {x}?", "Who is the author of {x}?", "{x} was written by what author?"]),
    "producer": (["the producer of {x}", "the film {x} made", "a film by {x}", "the work made by {x}"],
                 ["Who produced {x}?", "What film did {x} make?", "What did {x} produce?"]),
    "employer": (["the team {x} played for", "the company {x} worked for", "the school {x} attended", "the organisation {x} worked with",
                  "the presidents {x} worked with", "the club {x} was a main player for", "the firm {x} consulted for", "the utility {x} worked as a consultant for", "the school {x} played for prior to transferring", "the missions {x} was part of", "the administration {x} served in"],
                 ["Which team did {x} play for?", "Who did {x} work for?", "Which school did {x} attend?", "Which company employed {x}?"]),
    "birthplace": (["the birthplace of {x}", "the town where {x} was born"], ["Where was {x} born?", "What is the birthplace of {x}?"]),
    "home": (["the city where {x} is located", "the place {x} is in", "the town that contains {x}", "the region {x} belongs to", "the location of {x}", "the island {x} is situated on", "the city {x} is based in", "the district {x} belongs to", "the village {x} is part of"],
             ["Where is {x} located?", "In what city is {x}?", "Which town is {x} in?", "What island is {x} situated on?"]),
    "capital": (["the capital of {x}"], ["What is the capital of {x}?"]),
    "founder": (["the founder of {x}", "the person who founded {x}"], ["Who founded {x}?", "Who was the founder of {x}?", "{x} was founded by whom?"]),
    "owner": (["the owner of {x}", "the actress in {x}", "the star of {x}", "whoever holds {x}"], ["Who owns {x}?", "Who starred in {x}?", "Who holds {x}?"]),
    "leader": (["the leader of {x}", "a member of {x}", "a player for {x}", "the frontwoman of {x}", "the actor who plays the lead in {x}", "the guest on {x}", "the driver of {x}", "the person who drove {x}", "the forward who played for {x}", "the choreographer of {x}", "the person who starred in {x}"],
               ["Who leads {x}?", "Name a member of {x}.", "Who was a player for {x}?", "Who is a guest on {x}?"]),
    "composer": (["the composer of {x}"], ["Who composed {x}?"]),
    "publisher": (["the channel that aired {x}", "the album that features {x}", "the series that includes {x}", "the network {x} aired on", "the label that released {x}", "the programming block that included {x}", "the collective series that includes {x}", "the supergroup that recorded {x}", "the national park named after {x}"],
                  ["Which channel aired {x}?", "Which album features {x}?", "What series includes {x}?", "On which network did {x} air?"]),
    "country": (["the country of {x}", "the destination of {x}", "the nation {x} represents", "the celestial body that is the destination of {x}", "the primary destination of {x}"], ["Which country is {x} from?", "What is the destination of {x}?"]),
    "attribute": (["the population of {x}", "the year {x} was founded", "the rank of {x}", "the position {x} held", "the date {x} was born", "the year {x} became president", "the peak chart position of {x}", "what {x} peaked at", "the number of citizens of {x}", "where {x} ranked", "the year {x} was released", "the medium of {x}"],
                  ["What is the population of {x}?", "In what year was {x} founded?", "What rank did {x} hold?", "When was {x} born?", "What position did {x} hold?", "What did {x} peak at?"]),
}
FILTERS = {"actor": ["who was also an actor", "that is an actor"], "president": ["who was also a president", "that was a president"],
           "singer": ["who is a singer"], "doctor": ["who is a doctor"], "female": ["who is female", "she"], "male": ["who is male", "he"],
           "retired": ["who is retired", "that is now retired"], "alive": ["who is still alive"]}

FIRST = ["Gary", "Keith", "Mary", "Richard", "Sara", "Claudio", "Alfred", "Russell", "Bob", "Mika", "Charles", "Robbie", "Betty", "Atom", "Francis", "George", "Lily", "Bernhard", "Julie", "Daniel", "Anna", "Marta", "Kenji", "Priya"]
LAST = ["Cooper", "Nichol", "Astor", "Darman", "Symington", "Lopez", "Marcus", "Moore", "Dylan", "Hakkinen", "Haughey", "Tucker", "Cohen", "Egoyan", "Lawrence", "Bush", "Okafor", "Novak", "Ibarra", "Lindqvist", "Sato", "Bennett"]
ADJ = ["Great", "Last", "Silent", "Hidden", "Red", "Final", "Broken", "Golden", "Wild", "Lost"]
NOUN = ["Event", "Confidential", "Magic", "Frontier", "Harbor", "Garden", "Signal", "Kingdom", "Bridge", "Season"]
PLACES = ["Overland Park", "Lowell", "Troy", "Sydney", "Norman", "Kellyville Ridge", "Oak Beach", "Yau Ma Tei North", "Tharangambadi", "Lincoln County", "Long Island", "Cumberland Plain"]
ORGS = ["Valencia CF", "Michigan State", "Wanxiang Group", "Xcel Energy", "Goldwyn Productions", "Southern Baptist Theological Seminary", "The Rebirth", "Fitz and The Tantrums", "A123 Systems", "Cartoon Network"]
CODES = ["WLLZ-LP", "McLaren MP4/11", "Spider9", "Band-e-Amir Dragons", "Pueraria", "Pleiospilos", "Thirukkalacherry"]


def entity(rng):
    k = rng.random()
    if k < 0.35:
        return f"{rng.choice(FIRST)} {rng.choice(LAST)}"
    if k < 0.55:
        t = f"{rng.choice(ADJ)} {rng.choice(NOUN)}"
        return f'"{t}"' if rng.random() < 0.5 else f"The {t}"
    if k < 0.75:
        return rng.choice(PLACES)
    if k < 0.9:
        return rng.choice(ORGS)
    return rng.choice(CODES)


def noise(q, rng):
    r = rng.random()
    if r < 0.15:
        q = q[0].lower() + q[1:]
    elif r < 0.25:
        q = q.rstrip("?").rstrip() + " ?"
    elif r < 0.35:
        q = q.rstrip("?").rstrip()
    elif r < 0.45:
        q = rng.choice(["Prior to that, ", "Finally, ", "In the end, ", "Name the "]) + q[0].lower() + q[1:]
    return q


OOV_NOMINAL = ["the mascot of {x}", "the colour scheme of {x}", "the running time of {x}", "the sponsor of {x}", "the elevation of {x}",
               "the ticker symbol of {x}", "the last recorded speed of {x}", "the motto of {x}", "the mascot chosen by {x}", "the nickname of {x}"]
OOV_QUESTION = ["What is the mascot of {x}?", "How long is {x}?", "What is the motto of {x}?", "What nickname does {x} have?", "What is the elevation of {x}?"]
OOV_MODIFIERS = ["from Finland", "in 1990", "who is Argentine", "that is eight parts long", "who worked as a consultant", "who is Irish",
                 "that is 3-D", "in the 1964 film", "ranked in 2009", "held in Sydney", "who is a forward", "that has more than one appearance"]
DESCRIPTORS = ["the large subunit and small subunit", "two types of RNA", "the eight part documentary", "a British-American supergroup",
               "the female member of the band", "the 1958 pro bowl", "the lower house of parliament"]


# v3 (2026-09-13, loop round 2 5-why): relation phrasings shaped as participial / relative clauses that wrap the
# inner phrase without a "the X of" head. Real HotpotQA middle hops read "a 1982 film adapted from ...",
# "the nursery rhyme inspiring ...", "the company that created ...", "the show co-created by ...".
CLAUSE = {
    "parent": ["a film loosely adapted from {x}", "the work based on {x}", "the story {x} draws on", "the nursery rhyme that inspired {x}", "the source material for {x}"],
    "writer": ["the man who penned {x}", "whoever wrote {x}", "the author responsible for {x}"],
    "producer": ["the show co-created by {x}", "a Netflix series {x} co-created", "the fourth studio album made by {x}", "the film {x} directed and produced", "a documentary {x} put together"],
    "leader": ["the actor who plays the title role in {x}", "the monarch who ruled {x}", "the singer who performs on {x}", "the person who stars in {x}", "the waterfowl that live in {x}", "the men who founded {x} together"],
    "home": ["the city {x} grew up in", "the county whose seat is {x}", "the area {x} lies within", "the suburb where {x} is found", "the rule-class city that contains {x}"],
    "employer": ["the club {x} signed with", "the university where {x} taught", "the network {x} hosted a show on", "the company {x} was hired by"],
    "founder": ["the company that created {x}", "the firm that developed {x}", "the man who established {x}", "the studio that built {x}"],
    "owner": ["the person {x} testified against", "the character {x} plays", "the label that owns {x}", "the star {x} is best known for"],
    "publisher": ["the network on which {x} aired", "the album on which {x} appears", "the series {x} belongs to", "the anthology {x} was collected in"],
    "brother": ["the politician who preceded {x}", "the sibling {x} grew up with", "the season that came right before {x}"],
    "birthplace": ["the town in which {x} was born", "the suburb {x} comes from"],
    "country": ["the nation {x} hails from", "the country in which {x} is located"],
    "attribute": ["the year in which {x} was established", "how many people live in {x}", "the ethnic group among which {x} developed", "the chart position {x} reached"],
    "director": ["the filmmaker who made {x}", "whoever directed {x}", "the man behind the camera on {x}"],
    "spouse": ["the woman {x} married", "the man who married {x}"],
    "child": ["the boy born to {x}", "the daughter raised by {x}"],
    "father": ["the man who fathered {x}"],
    "mother": ["the woman who gave birth to {x}"],
    "sister": ["the girl who grew up alongside {x}"],
    "capital": ["the city that serves as the seat of {x}"],
    "composer": ["the musician who scored {x}"],
}
CLAUSE_Q = ["What is {p}?", "Who is {p}?", "Name {p}.", "What was {p}?"]
# v3 outer-question lead-ins that carry a date or number BEFORE the anchor (real anchors are not the first salient span)
LEADINS = ["On {d}, ", "In {y}, ", "As of {y}, ", "With a population of {n}, ", "Back in {y}, "]
MONTHS = ["May", "June", "March", "October"]
# v3 NA forms: two entities compared or sharing a property
NA_V3 = ["{a} and {b} are both this nationality?", "{a} and {b} are both what profession?", "What organization do {a} and {b} have in common?",
         "What do {a} and {b} have in common?", "Are {a} and {b} both American?", "{a} and {b}, which was born first?",
         "Which of {a} and {b} has won more awards?", "Do {a} and {b} share a hometown?"]

OOV_FRAC, DESC_FRAC, FILTER_FRAC, DEPTH_WEIGHTS = 0.15, 0.10, 0.25, [35, 40, 20, 5]   # loop-routable knobs
CLAUSE_FRAC, LEADIN_FRAC = 0.35, 0.15                                                 # v3 knobs (TAGGER_CLAUSE_FRAC, TAGGER_LEADIN_FRAC)


def make_chain(rng, max_depth=4):
    depth = rng.choices([1, 2, 3, 4], weights=DEPTH_WEIGHTS)[0]
    rels = [rng.choice(list(RELS)) for _ in range(depth)]
    oov_slot = rng.randrange(depth) if rng.random() < OOV_FRAC else None    # (b) one relation phrased outside the set -> attribute
    if oov_slot is not None:
        rels[oov_slot] = "attribute"
    ent = rng.choice(DESCRIPTORS) if rng.random() < DESC_FRAC else entity(rng)   # (d) descriptor anchors
    phrase = ent
    for i, r in enumerate(rels[:-1]):                                   # inner hops as nominal phrases, innermost first
        if i == oov_slot:
            form = rng.choice(OOV_NOMINAL)
        elif r in CLAUSE and rng.random() < CLAUSE_FRAC:                # v3: clause-shaped wrapper
            form = rng.choice(CLAUSE[r])
        else:
            form = rng.choice(RELS[r][0])
        phrase = form.format(x=phrase)
    outer = rels[-1]
    if oov_slot == depth - 1:
        q = rng.choice(OOV_QUESTION).format(x=phrase)
    elif outer in CLAUSE and rng.random() < CLAUSE_FRAC:
        q = rng.choice(CLAUSE_Q).format(p=rng.choice(CLAUSE[outer]).format(x=phrase))
    elif rng.random() < 0.7:
        q = rng.choice(RELS[outer][1]).format(x=phrase)
    else:
        q = f"What is {rng.choice(RELS[outer][0]).format(x=phrase)}?"
    prop = None
    r = rng.random()
    if r < FILTER_FRAC:
        prop = rng.choice(list(FILTERS))
        q = q.rstrip("?").rstrip() + " " + rng.choice(FILTERS[prop]) + "?"
    elif r < FILTER_FRAC + 0.20:                                        # (c) a modifier that is NOT a filter
        q = q.rstrip("?").rstrip() + " " + rng.choice(OOV_MODIFIERS) + "?"
    if rng.random() < LEADIN_FRAC:                                       # v3: date / number before the anchor
        lead = rng.choice(LEADINS).format(d=f"{rng.choice(MONTHS)} {rng.randrange(1, 29)}, {rng.randrange(1890, 2018)}",
                                          y=rng.randrange(1890, 2018), n=f"{rng.randrange(1, 900)},{rng.randrange(100, 999)}")
        q = lead + q[0].lower() + q[1:]
    tag = " of ".join(reversed(rels)) + f" of {ent}" + (f" [ {prop} ]" if prop else "") + " ?"
    return noise(q, rng), tag


def make_na(rng):
    a, b = entity(rng), entity(rng)
    q = rng.choice([f"Which came first, {a} or {b}?", f"Which has more species, {a} or {b}?", f"Are {a} and {b} both located in the same state?",
                    f"Which is older, {a} or {b}?", f"Which case was brought to court first, {a} or {b}?", f"Which is a flowering plant, {a} or {b}?",
                    f"How many films did {a} and {b} make together?"] + [t.format(a=a, b=b) for t in NA_V3])
    return noise(q, rng), "NA"


def _env_float(name, default):
    import os
    v = os.environ.get(name)
    return float(v) if v else default


def main():
    import os
    global OOV_FRAC, DESC_FRAC, FILTER_FRAC, DEPTH_WEIGHTS, CLAUSE_FRAC, LEADIN_FRAC
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="data/tagger_train.jsonl")
    args = ap.parse_args()
    rng = random.Random(args.seed)
    # loop-routable knobs (scripts/tagger_loop.py sets these per round)
    na_frac = _env_float("TAGGER_NA_FRAC", 0.12)
    OOV_FRAC = _env_float("TAGGER_OOV_FRAC", OOV_FRAC)
    DESC_FRAC = _env_float("TAGGER_DESC_FRAC", DESC_FRAC)
    FILTER_FRAC = _env_float("TAGGER_FILTER_FRAC", FILTER_FRAC)
    CLAUSE_FRAC = _env_float("TAGGER_CLAUSE_FRAC", CLAUSE_FRAC)
    LEADIN_FRAC = _env_float("TAGGER_LEADIN_FRAC", LEADIN_FRAC)
    if os.environ.get("TAGGER_DEPTH_WEIGHTS"):
        DEPTH_WEIGHTS = [int(x) for x in os.environ["TAGGER_DEPTH_WEIGHTS"].split(",")]
    with open(args.out, "w", encoding="utf-8") as f:
        for _ in range(args.n):
            q, t = make_na(rng) if rng.random() < na_frac else make_chain(rng)
            f.write(json.dumps({"question": q, "tag": t}, ensure_ascii=False) + "\n")
    print(f"wrote {args.n} pairs to {args.out}")


if __name__ == "__main__":
    main()
