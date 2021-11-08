from src.clustering_deletion_edge_contraction_based.choice import choice_deleted_edge_greedy, choice_weight_greedy, choice_weight_softmax_random, choice_uniform_random, choice_weight_random, choice_entropy_greedy
from src.clustering_deletion_edge_contraction_based.util_exp import experiments, plot_data_frame

if __name__ == "__main__":
    datasets = {
        "FB1": "data/cur_data_exp/0.edges",
        # "FB2": "data/cur_data_exp/107.edges",
        # "bio-CE-GT": "data/bio/bio-CE-GT.edges",
        # # "bio-celegans": "data/bio/bio-celegans.edges",
        # "bio-SC-CC": "data/bio/bio-SC-CC.edges"
    }

    algorithms = {
        # "choice_uniform_random": choice_uniform_random,
        # "choice_weight_random": choice_weight_random,
        # "choice_weight_softmax_random": choice_weight_softmax_random,
        # "choice_weight_greedy": choice_weight_greedy,
        "choice_deleted_edge_greedy": choice_deleted_edge_greedy,
        # "choice_entropy_greedy": choice_entropy_greedy
    }

    res = experiments(datasets, algorithms)

    df_val = res[0]
    df_time = res[1]

    plot_data_frame(df_val, title="Clustering Deletion S*")
