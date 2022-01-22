from src.clustering_deletion_simple_graph.clustering_deletion_edge_contraction_based.choice import choice_deleted_edge_greedy, choice_weight_greedy, choice_weight_softmax_random, choice_uniform_random, choice_weight_random, choice_entropy_greedy, choice_max_Ne0_e1
from src.clustering_deletion_simple_graph.clustering_deletion_edge_contraction_based.util_exp import experiments, plot_data_frame

if __name__ == "__main__":
    datasets = {
        "FB1": "data/exp/FB1",
        # "FB2": "data/exp/FB2",
        # "bio-CE-GT": "data/exp/bio-CE-GT",
        # "bio-SC-CC" : "data/bio/bio-SC-CC",
        # "bio-HS-HT.edges" : "data/bio/bio-HS-HT.edges",
        # "bio-grid-plant.edges" : "data/bio/bio-grid-plant.edges",
        # "bio-grid-worm.edges" : "data/bio/bio-grid-worm.edges"
    }

    algorithms = {
        # "choice_uniform_random": choice_uniform_random,
        # "choice_weight_random": choice_weight_random,
        # "choice_weight_softmax_random": choice_weight_softmax_random,
        # "choice_weight_greedy": choice_weight_greedy,
        # "choice_deleted_edge_greedy": choice_deleted_edge_greedy,
        # "choice_entropy_greedy": choice_entropy_greedy,
        "choice_max_Ne0_e1": choice_max_Ne0_e1
    }

    res = experiments(datasets, algorithms)

    df_val = res[0]
    df_time = res[1]

    print(df_time)
    print(df_val)

    # plot_data_frame(df_val, title="Clustering Deletion S*")
