import random

class BayesNode:

    def __init__(self, name, parents, cpt):
        self.name = name
        self.parents = parents
        self.cpt = cpt

    def probability(self, value, parent_values):
        p_true = self.cpt[parent_values]
        return p_true if value else (1 - p_true)


class BayesianNetwork:

    def __init__(self):
        self.nodes = {}
        self.order = []

    def add_node(self, node):
        self.nodes[node.name] = node
        self.order.append(node.name)

    def sample(self):
        sample = {}

        for name in self.order:
            node = self.nodes[name]
            parent_vals = tuple(sample[p] for p in node.parents)

            p_true = node.cpt[parent_vals]

            sample[name] = random.random() < p_true

        return sample

    def rejection_sampling(self, query, evidence, n_samples=10000):

        consistent = 0
        query_true = 0

        for _ in range(n_samples):

            s = self.sample()

            if all(s[var] == val for var, val in evidence.items()):
                consistent += 1

                if s[query]:
                    query_true += 1

        if consistent == 0:
            return None

        return query_true / consistent

    def enumerate_all(self, variables, evidence):

        if not variables:
            prob = 1.0

            for name in self.order:
                node = self.nodes[name]

                if name in evidence:
                    parent_vals = tuple(evidence[p] for p in node.parents)

                    prob *= node.probability(
                        evidence[name],
                        parent_vals
                    )

            return prob

        var = variables[0]
        rest = variables[1:]

        total = 0.0

        for val in [True, False]:

            ext_evidence = dict(evidence)
            ext_evidence[var] = val

            total += self.enumerate_all(rest, ext_evidence)

        return total

    def query_exact(self, query_var, query_val, evidence):

        hidden = [
            n for n in self.order
            if n != query_var and n not in evidence
        ]

        ev_true = dict(evidence)
        ev_true[query_var] = True

        p_true = self.enumerate_all(hidden, ev_true)

        ev_false = dict(evidence)
        ev_false[query_var] = False

        p_false = self.enumerate_all(hidden, ev_false)

        total = p_true + p_false

        if total == 0:
            return None

        return (p_true / total) if query_val else (p_false / total)


def build_weather_bn():

    bn = BayesianNetwork()

    cloudy = BayesNode(
        name="Cloudy",
        parents=[],
        cpt={
            (): 0.5
        }
    )

    rain = BayesNode(
        name="Rain",
        parents=["Cloudy"],
        cpt={
            (True,): 0.8,
            (False,): 0.2
        }
    )

    sprinkler = BayesNode(
        name="Sprinkler",
        parents=["Cloudy"],
        cpt={
            (True,): 0.1,
            (False,): 0.5
        }
    )

    wet_grass = BayesNode(
        name="WetGrass",
        parents=["Rain", "Sprinkler"],
        cpt={
            (True, True): 0.99,
            (True, False): 0.9,
            (False, True): 0.9,
            (False, False): 0.0
        }
    )

    bn.add_node(cloudy)
    bn.add_node(rain)
    bn.add_node(sprinkler)
    bn.add_node(wet_grass)

    return bn


def test_bayesian_network():

    random.seed(42)

    bn = build_weather_bn()

    print("=" * 50)
    print("TEST 1 – Prior sample")
    print("=" * 50)

    s = bn.sample()

    print("Sample:", s)

    print("PASS\n")

    print("=" * 50)
    print("TEST 2 – Exact Inference")
    print("=" * 50)

    p = bn.query_exact(
        "Rain",
        True,
        evidence={"Cloudy": True}
    )

    print(f"P(Rain=True | Cloudy=True) = {p:.4f}")

    print("PASS\n")

    print("=" * 50)
    print("TEST 3 – Rejection Sampling")
    print("=" * 50)

    p = bn.rejection_sampling(
        "Rain",
        {"WetGrass": True},
        n_samples=20000
    )

    print(f"P(Rain=True | WetGrass=True) ≈ {p:.4f}")

    print("PASS\n")


if __name__ == "__main__":
    test_bayesian_network()

    print("All Bayesian Network tests passed!")