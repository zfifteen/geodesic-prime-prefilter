from weight_gap_classifier import predict_next_gap_candidates, filtered_next_prime_search

# 1. decompwlj filter: enumerate even g, compute implied k = min divisor of p-g > g
#    keep only g where k's historical allowed set contains g
cands = predict_next_gap_candidates(p=113, max_g=50)
# p=113 returns 11 candidates out of 25 evens, actual g=14 is in list with k=33

# 2. PGS ranking: for each surviving g, compute Gap Winner tau
ranked = filtered_next_prime_search(p=113, max_g=50)
# sorted by num_options_for_k + compress -> g=14 surfaces with compress=8, tau=3