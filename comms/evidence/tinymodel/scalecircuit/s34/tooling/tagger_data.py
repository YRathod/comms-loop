"""Synthetic pairs for the tagger fine-tune: an English-lite question -> the mini-language tag.

v5 (2026-09-13, s21): name-plus-descriptor competition (APPOS) added on top of v4; TAGGER_APPOS_FRAC, default 0.30.
v4 (2026-09-13, scalecircuit s16 remedy). PROVENANCE RULE: nothing on the source side may be traceable
to the scored eval docs (HotpotQA docs 0-39). Entity pools are built mechanically from the questions
of train-side docs 40-159 (data/tagger_pools_v4.json, any span also present in docs 0-39 dropped;
DEV docs 160-199 excluded too); relation phrasings are generic or come from the hand-labelled
train-side batches (docs 70-129, the round-1/2 5-whys); descriptors, modifiers and filters are
generic. scripts/tagger_data_check.py verifies zero overlap with the eval questions and must be
CLEAN before any training run. v1/v2 pools and several phrasings had been typed from eval questions;
that generator is frozen as comms evidence s16/tagger_data_v3_contaminated.py and is not used again.

Source side: relation phrasings (nominal forms that wrap an inner phrase, question forms for the
outermost hop, clause-shaped wrappers), entity spans, optional filter clauses, crowd-style noise,
date/number lead-ins, and comparison / two-thing questions that map to NA. The model's own outputs
never enter the data.

    .venv\\Scripts\\python scripts/tagger_data.py --n 20000 --out data/tagger_train_v4.jsonl
"""
import argparse
import json
import os
import random

_POOLS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "tagger_pools_v4.json"), encoding="utf-8"))
FIRST, LAST, MULTI, SINGLE = _POOLS["FIRST"], _POOLS["LAST"], _POOLS["MULTI"], _POOLS["SINGLE"]

# generic relation phrasings only (nominal forms wrap an inner phrase; question forms for the outer hop)
RELS = {
    "father": (["the father of {x}", "{x}'s father"], ["Who is the father of {x}?", "Who was {x}'s father?"]),
    "mother": (["the mother of {x}", "{x}'s mother"], ["Who is the mother of {x}?", "Who was {x}'s mother?"]),
    "parent": (["a parent of {x}", "the parents of {x}", "the work {x} is based on"], ["Who are the parents of {x}?", "Who is a parent of {x}?", "What is {x} based on?"]),
    "spouse": (["the spouse of {x}", "the wife of {x}", "the husband of {x}", "the person married to {x}"], ["Who is {x} married to?", "Who is the spouse of {x}?"]),
    "child": (["a child of {x}", "the son of {x}", "the daughter of {x}"], ["Who is the child of {x}?", "Name a child of {x}."]),
    "brother": (["the brother of {x}", "a sibling of {x}", "the predecessor of {x}"], ["Who is the brother of {x}?", "Who is a sibling of {x}?", "What preceded {x}?"]),
    "sister": (["the sister of {x}"], ["Who is the sister of {x}?"]),
    "director": (["the director of {x}", "the person who directed {x}", "the filmmaker behind {x}"],
                 ["Who directed {x}?", "Who was the director of {x}?", "{x} was directed by whom?"]),
    "writer": (["the author of {x}", "the writer of {x}", "the person who wrote {x}", "the novelist behind {x}"],
               ["Who wrote {x}?", "Who is the author of {x}?", "{x} was written by what author?"]),
    "producer": (["the producer of {x}", "a film by {x}", "the work made by {x}", "a show created by {x}", "an album recorded by {x}"],
                 ["Who produced {x}?", "What film did {x} make?", "What did {x} produce?", "What show did {x} create?"]),
    "employer": (["the team {x} played for", "the company {x} worked for", "the school {x} attended", "the organisation {x} worked with", "the club {x} joined", "the university {x} taught at"],
                 ["Which team did {x} play for?", "Who did {x} work for?", "Which school did {x} attend?", "Which company employed {x}?"]),
    "birthplace": (["the birthplace of {x}", "the town where {x} was born"], ["Where was {x} born?", "What is the birthplace of {x}?"]),
    "home": (["the city where {x} is located", "the place {x} is in", "the town that contains {x}", "the region {x} belongs to", "the location of {x}", "the county {x} is part of", "the neighbourhood {x} lies in"],
             ["Where is {x} located?", "In what city is {x}?", "Which town is {x} in?", "What county is {x} part of?"]),
    "capital": (["the capital of {x}"], ["What is the capital of {x}?"]),
    "founder": (["the founder of {x}", "the person who founded {x}", "the company that developed {x}"], ["Who founded {x}?", "Who was the founder of {x}?", "{x} was established by whom?"]),
    "owner": (["the owner of {x}", "the star of {x}", "the person who holds {x}", "the character played by {x}"], ["Who owns {x}?", "Who starred in {x}?", "Who holds {x}?"]),
    "leader": (["the leader of {x}", "a member of {x}", "a player for {x}", "the lead singer of {x}", "the person who starred in {x}", "the head of {x}", "the ruler of {x}"],
               ["Who leads {x}?", "Who is a member of {x}?", "Who was a player for {x}?", "Who ruled {x}?"]),
    "composer": (["the composer of {x}"], ["Who composed {x}?"]),
    "publisher": (["the channel that aired {x}", "the album that features {x}", "the series containing {x}", "the network {x} aired on", "the label that released {x}", "the magazine that printed {x}"],
                  ["Which channel aired {x}?", "Which album features {x}?", "What series includes {x}?", "On which network did {x} air?"]),
    "country": (["the country of {x}", "the nation {x} represents", "the country {x} comes from"], ["Which country is {x} from?", "What country is {x} in?"]),
    "attribute": (["the population of {x}", "the year {x} was founded", "the rank of {x}", "the position {x} held", "the date {x} was born", "the length of {x}", "the height of {x}", "the year {x} was released", "the number of members of {x}", "the profession of {x}"],
                  ["What is the population of {x}?", "In what year was {x} founded?", "What rank did {x} hold?", "When was {x} born?", "What position did {x} hold?", "How long is {x}?", "What was the profession of {x}?"]),
}
# clause-shaped wrappers (round-1/2 5-whys, written from the train-side batches docs 70-129)
CLAUSE = {
    "parent": ["a film loosely adapted from {x}", "the work based on {x}", "the story {x} draws on", "the nursery rhyme that inspired {x}", "the source material for {x}"],
    "writer": ["the man who penned {x}", "whoever wrote {x}", "the author responsible for {x}"],
    "producer": ["the show co-created by {x}", "a series {x} co-created", "the fourth studio album made by {x}", "the film {x} directed and produced", "a documentary {x} put together"],
    "leader": ["the actor who plays the title role in {x}", "the monarch who ruled {x}", "the singer who performs on {x}", "the person who stars in {x}", "the birds that live in {x}", "the men who founded {x} together"],
    "home": ["the city {x} grew up in", "the county whose seat is {x}", "the area {x} lies within", "the suburb where {x} is found", "the city that contains {x}"],
    "employer": ["the club {x} signed with", "the university where {x} taught", "the network {x} hosted a show on", "the company {x} was hired by"],
    "founder": ["the company that created {x}", "the firm that developed {x}", "the man who established {x}", "the studio that built {x}"],
    "owner": ["the person {x} testified against", "the character {x} plays", "the label that owns {x}", "the role {x} is best known for"],
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
LEADINS = ["On {d}, ", "In {y}, ", "As of {y}, ", "With a population of {n}, ", "Back in {y}, "]
MONTHS = ["May", "June", "March", "October"]
NA_V3 = ["{a} and {b} are both this nationality?", "{a} and {b} are both what profession?", "What organization do {a} and {b} have in common?",
         "What do {a} and {b} have in common?", "Are {a} and {b} both American?", "{a} and {b}, which was born first?",
         "Which of {a} and {b} has won more awards?", "Do {a} and {b} share a hometown?"]

FILTERS = {"actor": ["who was also an actor", "that is an actor"], "president": ["who served as president", "that was a president"],
           "singer": ["who is a singer"], "doctor": ["who is a doctor"], "female": ["who is a woman", "she"], "male": ["who is a man", "he"],
           "retired": ["who has retired", "that is now retired"], "alive": ["who is still living"]}

# generic titles for works (adjective + noun), not tied to any document
ADJ = ["Silent", "Hidden", "Broken", "Golden", "Wild", "Lost", "Distant", "Quiet", "Crimson", "Frozen"]
NOUN = ["Harbor", "Signal", "Kingdom", "Bridge", "Orchard", "Lantern", "Voyage", "Meadow", "Compass", "Tower"]

OOV_NOMINAL = ["the mascot of {x}", "the colour scheme of {x}", "the running time of {x}", "the sponsor of {x}", "the elevation of {x}",
               "the ticker symbol of {x}", "the top speed of {x}", "the motto of {x}", "the mascot chosen by {x}", "the nickname of {x}"]
OOV_QUESTION = ["What is the mascot of {x}?", "What is the motto of {x}?", "What nickname does {x} have?", "What is the elevation of {x}?", "Who sponsors {x}?"]
OOV_MODIFIERS = ["from Portugal", "in 1975", "who is Peruvian", "that is six parts long", "who worked as an engineer", "who is Welsh",
                 "that is animated", "in the 1971 film", "ranked in 2004", "held in Lisbon", "who is a goalkeeper", "that ran for several seasons"]
DESCRIPTORS = ["the largest city in the province", "the follow-up record by the band", "the winning side of the final", "the female lead of the series",
               "the oldest member of the group", "a two-part television special", "the national anthem of the republic", "the smaller of the two moons",
               "the third book in the trilogy", "the losing finalist"]

# v5 (2026-09-13, s21 anchor 5-why): a descriptor competes with the proper name inside one question and the
# name stays the anchor (appositive after the name, type noun before it, trailing descriptor). Generic material only.
NATIONALITY = ["Peruvian", "Welsh", "Portuguese", "Nigerian", "Danish", "Turkish", "Chilean", "Estonian", "Malaysian", "Icelandic"]
TYPE_NOUN = ["cricket team", "national park", "radio station", "racing car", "software company", "folk singer", "documentary series",
             "rugby club", "research institute", "mountain village", "shipping firm", "chess player", "opera house", "textile mill"]
REGION = ["the north coast", "the southern highlands", "the river delta", "the eastern provinces", "the old town"]
APPOS = ["{x}, a {nat} {tn},", "{x} (a {tn}),", "the {nat} {tn} {x}", "{x}, the {tn} from {reg},", "{x}, which is a {tn} in {reg},"]
APPOS_FRAC = 0.30                                                                     # v5 knob (TAGGER_APPOS_FRAC)

OOV_FRAC, DESC_FRAC, FILTER_FRAC, DEPTH_WEIGHTS = 0.15, 0.10, 0.25, [35, 40, 20, 5]   # loop-routable knobs
CLAUSE_FRAC, LEADIN_FRAC = 0.35, 0.15                                                 # v3 knobs (TAGGER_CLAUSE_FRAC, TAGGER_LEADIN_FRAC)


def entity(rng):
    k = rng.random()
    if k < 0.35:
        return f"{rng.choice(FIRST)} {rng.choice(LAST)}"
    if k < 0.50:
        t = f"{rng.choice(ADJ)} {rng.choice(NOUN)}"
        return f'"{t}"' if rng.random() < 0.5 else f"The {t}"
    if k < 0.80:
        return rng.choice(MULTI)
    return rng.choice(SINGLE)


def noise(q, rng):
    r = rng.random()
    if r < 0.15:
        q = q[0].lower() + q[1:]
    elif r < 0.25:
        q = q.rstrip("?").rstrip() + " ?"
    elif r < 0.35:
        q = q.rstrip("?").rstrip()
    elif r < 0.45:
        q = rng.choice(["Prior to that, ", "Lastly, ", "In the end, ", "Name the "]) + q[0].lower() + q[1:]
    return q


def make_chain(rng, max_depth=4):
    depth = rng.choices([1, 2, 3, 4], weights=DEPTH_WEIGHTS)[0]
    rels = [rng.choice(list(RELS)) for _ in range(depth)]
    oov_slot = rng.randrange(depth) if rng.random() < OOV_FRAC else None    # one relation phrased outside the set -> attribute
    if oov_slot is not None:
        rels[oov_slot] = "attribute"
    ent = rng.choice(DESCRIPTORS) if rng.random() < DESC_FRAC else entity(rng)   # descriptor anchors
    phrase = ent
    if ent not in DESCRIPTORS and rng.random() < APPOS_FRAC:                # v5: descriptor competes with the name; name stays the anchor
        phrase = rng.choice(APPOS).format(x=ent, nat=rng.choice(NATIONALITY), tn=rng.choice(TYPE_NOUN), reg=rng.choice(REGION))
    for i, r in enumerate(rels[:-1]):                                   # inner hops as nominal phrases, innermost first
        if i == oov_slot:
            form = rng.choice(OOV_NOMINAL)
        elif r in CLAUSE and rng.random() < CLAUSE_FRAC:                # clause-shaped wrapper
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
    elif r < FILTER_FRAC + 0.20:                                        # a modifier that is NOT a filter
        q = q.rstrip("?").rstrip() + " " + rng.choice(OOV_MODIFIERS) + "?"
    if rng.random() < LEADIN_FRAC:                                       # date / number before the anchor
        lead = rng.choice(LEADINS).format(d=f"{rng.choice(MONTHS)} {rng.randrange(1, 29)}, {rng.randrange(1890, 2018)}",
                                          y=rng.randrange(1890, 2018), n=f"{rng.randrange(1, 900)},{rng.randrange(100, 999)}")
        q = lead + q[0].lower() + q[1:]
    tag = " of ".join(reversed(rels)) + f" of {ent}" + (f" [ {prop} ]" if prop else "") + " ?"
    return noise(q, rng), tag


def make_na(rng):
    a, b = entity(rng), entity(rng)
    q = rng.choice([f"Which came first, {a} or {b}?", f"Which has more members, {a} or {b}?", f"Are {a} and {b} both located in the same state?",
                    f"Which is older, {a} or {b}?", f"Which lawsuit was filed earlier, {a} or {b}?", f"Which is a conifer, {a} or {b}?",
                    f"How many films did {a} and {b} make together?"] + [t.format(a=a, b=b) for t in NA_V3])
    return noise(q, rng), "NA"


def _env_float(name, default):
    v = os.environ.get(name)
    return float(v) if v else default


def main():
    global OOV_FRAC, DESC_FRAC, FILTER_FRAC, DEPTH_WEIGHTS, CLAUSE_FRAC, LEADIN_FRAC, APPOS_FRAC
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
    APPOS_FRAC = _env_float("TAGGER_APPOS_FRAC", APPOS_FRAC)
    if os.environ.get("TAGGER_DEPTH_WEIGHTS"):
        DEPTH_WEIGHTS = [int(x) for x in os.environ["TAGGER_DEPTH_WEIGHTS"].split(",")]
    with open(args.out, "w", encoding="utf-8") as f:
        for _ in range(args.n):
            q, t = make_na(rng) if rng.random() < na_frac else make_chain(rng)
            f.write(json.dumps({"question": q, "tag": t}, ensure_ascii=False) + "\n")
    print(f"wrote {args.n} pairs to {args.out}")
    # provenance duty (PROTOCOL v1.15): the generator refuses to leave an unchecked file behind
    import subprocess, sys
    rc = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tagger_data_check.py"), args.out]).returncode
    if rc != 0:
        os.remove(args.out)
        raise SystemExit(f"provenance check FAILED; {args.out} deleted (fix the generator lists, never the check)")


if __name__ == "__main__":
    main()
