
EVOLUTIONS = {

    "1": {
        "name": "Nadadeiras",
        "description": "Aumenta a velocidade de movimento.",
        "cost": 3,
        "trait": "fins"
    },

    "2": {
        "name": "Membrana reforçada",
        "description": "Melhora a proteção do organismo.",
        "cost": 4,
        "trait": "membrane"
    },

    "3": {
        "name": "Percepção avançada",
        "description": "Melhora a percepção do ambiente.",
        "cost": 2,
        "trait": "perception"
    },

    "4": {
        "name": "Eficiência energética",
        "description": "Reduz o consumo de energia.",
        "cost": 5,
        "trait": "efficiency"
    }

}


def purchase_evolution(organism, evolution_id):

    evolution = EVOLUTIONS[evolution_id]

    cost = evolution["cost"]

    if organism.evolution_points < cost:
        return False

    organism.evolution_points -= cost

    organism.evolve(evolution["trait"])

    return True
