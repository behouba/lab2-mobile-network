import argparse
import time

from AlgoGen import AlgoGen


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="python %(prog)s [FILE] [OPTIONS]",
    )
    parser.add_argument(
        "nom_fichier", type=str, help="Path of the json data file"
    )

    parser.add_argument(
        '-g', '--generations', default=50, type=int, dest='nb_generations',
        help='The number of generations in a cycle, defaults to 50'
    )

    parser.add_argument(
        '-c', '--cycle', default=5, type=int, dest='nb_cycles',
        help='The number of cycles in the experiment, defaults to 5'
    )

    parser.add_argument(
        '-k', '--cross', default=0.9, type=float, dest='prob_croisement',
        help='The probability to cross parents, defaults to 0.9'
    )

    parser.add_argument(
        '-m', '--mutation', default=0.08, type=float, dest='prob_mutation',
        help='The probability of a mutation, defaults to 0.08'
    )

    parser.add_argument(
        '-v', '--verbose', dest='verbose', action='store_true', default=False, help='Shows the final solution'
    )

    return parser


if __name__ == '__main__':
    parser = init_argparse()
    args = parser.parse_args()

    args = vars(args)
    verbose = args.pop('verbose')

    print("ALGORITHME GENETIQUE")
    print("====================")
    print(f"FICHIER: {args['nom_fichier']}\n")
    print(f"NOMBRE GENERATIONS: {args['nb_generations']}")
    print(f"NOMBRE CYCLES: {args['nb_cycles']}")
    print(f"PROBABILITE CROISEMENT: {args['prob_croisement']}")
    print(f"PROBABILITE MUTATION: {args['prob_mutation']}\n\n")

    begin = time.time()
    solution, cout = AlgoGen.run(**args)
    end = time.time()

    print(f"COUT MEILLEURE SOLUTION: {cout}")
    print(f"Terminé en {end - begin:.5f} secondes\n\n")

    if verbose:
        print("La meilleure solution:")
        print(solution)
