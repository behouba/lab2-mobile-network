import argparse
import time

from Tabu import Tabu


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="python %(prog)s [FILE] [OPTIONS]",
    )
    parser.add_argument(
        "nom_fichier", type=str, help="Path of the json data file"
    )

    parser.add_argument(
        '-t', '--tabusize', default=9, type=int, dest='taille_tabu', help='Size of the Tabu List, defaults to 9'
    )

    parser.add_argument(
        '-m', '--medium', dest='moyen_terme', action='store_true', default=False, help='Activates the Medium Term Memory'
    )

    parser.add_argument(
        '-l', '--long', dest='long_terme', action='store_true', default=False, help='Activates the Long Term Memory'
    )

    parser.add_argument(
        '-v', '--verbose', dest='verbose', action='store_true', default=False, help='Shows the final solution'
    )

    return parser


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()

    args = vars(args)
    verbose = args.pop('verbose')

    print("RECHERCHE TABOUE")
    print("================\n")
    print(f"TAILLE LISTE TABOUE: {args['taille_tabu']}")
    print(f"MOYEN TERME: {args['moyen_terme']}")
    print(f"LONG TERME: {args['long_terme']}\n\n")

    algorithme = Tabu(**args)

    begin = time.time()
    best_cout = algorithme.run()
    end = time.time()

    algorithme.affiche_resultats(best_cout)
    print(f"Terminé en {end-begin:.5f} secondes\n\n")

    if verbose:
        print("La meilleure solution:")
        algorithme.affiche_solution()
