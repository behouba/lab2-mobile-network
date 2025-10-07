import argparse
import time
import random
from copy import deepcopy

from Base import Base
from RecuitGlouton.Glouton import Glouton
from RecuitGlouton.Recuit import Recuit


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="python %(prog)s [FILE] [OPTIONS]",
    )
    parser.add_argument(
        "filename", type=str, help="Path of the json data file"
    )

    parser.add_argument(
        '-r', '--randfactor', default=0.4, type=float, help='Randomization factor, defaults to 0.4'
    )

    parser.add_argument(
        '-i', '--iterations', default=3, type=int, help='Number of iterations, defaults to 3'
    )

    parser.add_argument(
        '-n', '--relances', default=5, type=int, help='Number of runs, defaults to 5'
    )

    parser.add_argument(
        '-t', '--inittemp', default=400.0, type=float, help='Initial temperature, defaults to 400.0'
    )

    parser.add_argument(
        '-f', '--tfactor', default=0.95, type=float, help='Temperature Factor, defaults to 0.95'
    )

    parser.add_argument(
        '-p', '--tpalier', default=300, type=int, help='Temperature Palier, defaults to 300'
    )

    return parser


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()

    print("ALGORITHME GLOUTON / RECUIT SIMULÉ")
    print("==================================")
    print(f"FICHIER: {args.filename}\n")

    print(f"NOMBRE ITÉRATIONS: {args.iterations}")
    print(f"NOMBRE RELANCES: {args.relances}\n")

    print(f"RANDFACTOR: {args.randfactor}\n")

    print(f"TEMPERATURE INITIALE: {args.inittemp}")
    print(f"FACTEUR DE TEMPERATURE: {args.tfactor}")
    print(f"PALIER DE TEMPERATURE{args.tpalier}\n\n")

    Base.read(args.filename)
    random.seed(time.time())

    for j in range(args.relances):
        best_glouton = None
        print("Début du glouton...")
        for i in range(args.iterations):
            glouton = Glouton()
            begin = time.time()
            solution = glouton.start(args.randfactor)
            end = time.time()

            print("Itération {} terminée en {:.5f} secondes".format(i, end - begin))
            if best_glouton is None:
                best_glouton = solution
            elif best_glouton.cost == solution.cost:
                best_glouton = deepcopy(solution)

        print("Fin de glouton. Meilleure solution: {:.2f}".format(best_glouton.cost))

        print("Début du recuit simulé...")
        begin = time.time()
        recuit = Recuit()
        solution = recuit.start(best_glouton, args.inittemp, args.tfactor, args.tpalier)
        end = time.time()

        print("Terminé en {:.5f} secondes".format(end - begin))
        print("Fin du recuit simulé. Meilleure solution: {:.2f}".format(solution.cost))
        delta = best_glouton.cost - solution.cost
        pourcent = 100 * delta / best_glouton.cost
        if delta > 0:
            print("Le coût de glouton a été amélioré de {:.2f}, soit {:.2f}%".format(delta, pourcent))

        print('=====================================')
