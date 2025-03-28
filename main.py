from int_alg import int_alg
from synth_gen import generate_data
from vizualize import visualize_pidf
from feature_selection import run_feature_selection
import argparse
import numpy as np
import time

parser = argparse.ArgumentParser()
parser.add_argument("name", help="Dataset name", type=str)
parser.add_argument("num_iters", help="Number of iterations", type=int)
parser.add_argument("feature_selection", help="True to run feature selection, False to run int_alg and visualize", type=bool)
args = parser.parse_args()


if __name__ == "__main__":
    if not args.feature_selection:
        # Run the int_alg and visualize branch
        obs, acs = generate_data(nme=args.name)
        start_time = time.time()

        # Run the algorithm
        data, data_std, reds_n_syns = int_alg(obs, acs, args.num_iters, scalable=False).run()

        # End timing
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to run int_alg: {time_taken:.2f} seconds")

        # Save results to .npy files
        np.save(f'interpretability_{args.name}.npy', np.array(data))
        np.save(f'interpretability_std_{args.name}.npy', np.array(data_std))
        np.save(f'syns_and_reds_{args.name}.npy', np.array(reds_n_syns))

        # Visualize results
        visualize_pidf(args.name)
    else:
        # Run feature selection on the provided dataset name with the specified number of iterations.
        start_time = time.time()
        run_feature_selection(names=[args.name], num_iters=args.num_iters)
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to run feature selection: {time_taken:.2f} seconds")
