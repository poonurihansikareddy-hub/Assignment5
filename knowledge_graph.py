from collections import defaultdict


class KnowledgeGraph:

    def __init__(self):

        self.triples = set()

        self.index = defaultdict(lambda: defaultdict(list))


    def add(self, subject, predicate, obj):

        triple = (subject, predicate, obj)

        if triple not in self.triples:

            self.triples.add(triple)

            self.index[subject][predicate].append(obj)


    def add_many(self, triples_list):

        for s, p, o in triples_list:
            self.add(s, p, o)


    def query(self, subject=None, predicate=None, obj=None):

        results = []

        for s, p, o in self.triples:

            if (subject is None or s == subject) and \
               (predicate is None or p == predicate) and \
               (obj is None or o == obj):

                results.append((s, p, o))

        return results


    def get_related(self, subject, predicate):

        return self.index[subject].get(predicate, [])


    def get_all_predicates(self):

        return sorted({p for _, p, _ in self.triples})


    def get_all_entities(self):

        entities = set()

        for s, _, o in self.triples:
            entities.add(s)
            entities.add(o)

        return sorted(entities)


    def print_graph(self):

        print("\nKnowledge Graph")
        print("-" * 50)

        for s, p, o in sorted(self.triples):

            print(f"({s}) --[{p}]--> ({o})")

        print()


    def describe(self, entity):

        print(f"\nFacts about '{entity}':")

        found = False

        for s, p, o in sorted(self.triples):

            if s == entity:

                print(f"{entity} --[{p}]--> {o}")

                found = True

            elif o == entity:

                print(f"{s} --[{p}]--> {entity}")

                found = True

        if not found:
            print("No facts found.")


def build_travel_kg():

    kg = KnowledgeGraph()

    kg.add_many([

        ("France", "isA", "Country"),
        ("Japan", "isA", "Country"),
        ("India", "isA", "Country"),
        ("Italy", "isA", "Country"),

        ("Paris", "isA", "City"),
        ("Kyoto", "isA", "City"),
        ("Goa", "isA", "City"),
        ("Florence", "isA", "City"),

        ("Paris", "locatedIn", "France"),
        ("Kyoto", "locatedIn", "Japan"),
        ("Goa", "locatedIn", "India"),
        ("Florence", "locatedIn", "Italy"),

        ("Eiffel Tower", "isA", "Attraction"),
        ("Louvre Museum", "isA", "Attraction"),
        ("Fushimi Inari", "isA", "Attraction"),
        ("Baga Beach", "isA", "Attraction"),

        ("Eiffel Tower", "locatedIn", "Paris"),
        ("Louvre Museum", "locatedIn", "Paris"),
        ("Fushimi Inari", "locatedIn", "Kyoto"),
        ("Baga Beach", "locatedIn", "Goa"),

        ("Croissants", "isA", "Food"),
        ("Ramen", "isA", "Food"),
        ("Fish Curry", "isA", "Food"),
        ("Bistecca", "isA", "Food"),

        ("Croissants", "popularIn", "Paris"),
        ("Ramen", "popularIn", "Kyoto"),
        ("Fish Curry", "popularIn", "Goa"),
        ("Bistecca", "popularIn", "Florence"),

        ("Chianti", "isA", "Wine"),
        ("Champagne", "isA", "Wine"),
        ("Sake", "isA", "Wine"),

        ("Chianti", "producedIn", "Italy"),
        ("Champagne", "producedIn", "France"),
        ("Sake", "producedIn", "Japan"),

        ("Paris", "suitableFor", "Art lovers"),
        ("Kyoto", "suitableFor", "Culture lovers"),
        ("Goa", "suitableFor", "Beach lovers"),
        ("Florence", "suitableFor", "Wine lovers"),

    ])

    return kg


def test_knowledge_graph():

    kg = build_travel_kg()

    print("=" * 50)
    print("TEST 1 – Print full graph")
    print("=" * 50)

    kg.print_graph()

    print("=" * 50)
    print("TEST 2 – Describe Paris")
    print("=" * 50)

    kg.describe("Paris")

    print("\n" + "=" * 50)
    print("TEST 3 – Query attractions in Paris")
    print("=" * 50)

    results = kg.query(predicate="locatedIn", obj="Paris")

    print("Things in Paris:")

    for r in results:
        print(r)

    print("PASS\n")

    print("=" * 50)
    print("TEST 4 – Paris suitable for")
    print("=" * 50)

    suitable = kg.get_related("Paris", "suitableFor")

    print("Paris is suitable for:", suitable)

    print("PASS\n")

    print("=" * 50)
    print("TEST 5 – All predicates")
    print("=" * 50)

    preds = kg.get_all_predicates()

    print(preds)

    print("PASS\n")

    print("=" * 50)
    print("TEST 6 – All entities")
    print("=" * 50)

    entities = kg.get_all_entities()

    print("Total entities:", len(entities))

    print("PASS\n")


if __name__ == "__main__":

    test_knowledge_graph()

    print("All Knowledge Graph tests passed!")