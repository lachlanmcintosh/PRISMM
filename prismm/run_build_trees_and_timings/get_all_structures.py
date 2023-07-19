
def timing_struct_to_all_structures(trees_and_timings, pre, mid, post, max_epoch):
    all_structures = {}
    
    for chrom in trees_and_timings:
        all_structures[chrom] = timing_structs_to_all_structs_per_chrom(trees_and_timings[chrom], pre, mid, post, max_epoch)

    

    return all_structures


def timing_structs_to_all_structs_per_chrom(trees_and_timings, pre, mid, post, max_epoch):
    logging.debug("trees_and_timings")
    logging.debug(trees_and_timings)
    all_structures = [] 
    for index, these_tts in enumerate(trees_and_timings):  # these tts are a 2d array
        if None in these_tts[3]:
            continue
            #BP_likelihoods = -1
        else:
            # trace back to here, asdfasdf
            CNs, unique_CNs, branch_lengths, stacked_branch_lengths = get_branch_lengths(trees_and_timings=these_tts, max_epoch=max_epoch)

            logging.debug("CNs, unique_CNs, branch_lengths, stacked_branch_lengths")
            logging.debug(f"{CNs}, {unique_CNs}, {branch_lengths}, {stacked_branch_lengths}")
            logging.debug("starts and ends")

            path = create_path(pre, mid, post)

            logging.debug(path)

            starts = these_tts[3] #+1
            ends = these_tts[3] + branch_lengths #+1

            logging.debug("starts")
            logging.debug(starts)
            logging.debug("ends")
            logging.debug(ends)

            paths = calculate_BP_paths(branch_lengths, starts, ends, path)

        tree, labelled_tree, count, epochs_created, parents = these_tts

        all_structures += [{
            "pre": pre,
            "mid": mid,
            "post": post,
            "path": path,
            "tree": tree,
            "parents": parents,
            "labelled_tree": labelled_tree,
            "count": count,
            "epochs_created": epochs_created,
            "CNs": CNs,
            "branch_lengths": branch_lengths,
            "unique_CNs": unique_CNs,
            "stacked_branch_lengths": stacked_branch_lengths,
            "starts":starts,
            "ends":ends,
            "paths":paths
        }]

    return all_structures