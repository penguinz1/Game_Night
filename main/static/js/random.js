const length = deltas.length // number of observations
const adj = 0.04683533 // adjusted 0-value to make heads-tails ratio about 50-50
const update_ratio = 1.5;

// generates either heads (true) or tails (false)
const heads_tails = (rand_ind) => {
    rand_ind %= length;
    return(deltas[rand_ind] > adj);
}

// creates random numbers in the interval [0, n_random]
const make_randoms = (n_random, rand_ind, n_pick, make_updates_conditionally) => {
    var numbers = []
    // pushes numbers to an array
    for (let i = 0; i <= n_random; i++) {
        numbers.push(i)
    }

    while (true) {
        let picks = []
        for (let i = 0; i < numbers.length; i++) {
            // keep only numbers that are heads
            if (heads_tails(rand_ind)) {
                picks.push(numbers[i]);
            }
            rand_ind++;
        }

        // if numbers remaining = n_pick, seletion is finished
        if (picks.length == n_pick) {
            return [picks, rand_ind];
        }

        // if numbers remaining < n_pick, dump results and try again
        if (picks.length < n_pick) {
            continue;
        }

        // update remaining numbers
        if (!make_updates_conditionally || picks.length > update_ratio * n_pick) {
            numbers = picks;
        }
    }
}

// creates a single random number in the interval [0, n_random]
const make_random = (n_random, rand_ind) => {
    let rand = make_randoms(n_random, rand_ind, 1, false);
    return [rand[0][0], rand[1]];
}

// makes nearly-uniform n_groups number of groups from the group_list recursively
const make_groups = (group_list, rand_ind, n_groups) => {
    if (n_groups == 1) {
        return [[group_list], rand_ind];
    }

    let n_split = Math.round(group_list.length / n_groups); // number of members in the group
    let split   = make_randoms(group_list.length - 1, rand_ind, n_split, true); // index of members in the group
    let in_group = []; // members in the group
    let out_group = []; // members outside of the group
    let pos = 0;
    for (let i = 0; i < group_list.length; i++) {
        if (pos < split[0].length && split[0][pos] == i) {
            in_group.push(group_list[i]);
            pos++;
        } else {
            out_group.push(group_list[i]);
        }
    }

    // generate other groups recursively
    other_groups = make_groups(out_group, split[1], n_groups - 1);
    // add current group to the other groups
    other_groups[0].push(in_group);

    return other_groups;
}
