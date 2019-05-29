const length = deltas.length
const adj = 0.04683533

const heads_tails = (rand_ind) => {
    rand_ind %= length;
    return(deltas[rand_ind] > adj);
}

const make_randoms = (n_random, rand_ind, n_pick) => {
    var numbers = []
    for (let i = 0; i <= n_random; i++) {
        numbers.push(i)
    }

    while (true) {
        let picks = []
        for (let i = 0; i < numbers.length; i++) {
            if (heads_tails(rand_ind)) {
                picks.push(numbers[i]);
            }
            rand_ind++;
        }

        if (picks.length == n_pick) {
            return [picks, rand_ind];
        }

        if (picks.length < n_pick) {
            continue;
        }

        numbers = picks;
    }
}

const make_random = (n_random, rand_ind) => {
    let rand = make_randoms(n_random, rand_ind, 1);
    return [rand[0][0], rand[1]];
}

const make_groups = (group_list, rand_ind, n_groups) => {
    if (n_groups == 1) {
        return [[group_list], rand_ind];
    }

    let n_split = Math.round(group_list.length / n_groups);
    let split   = make_randoms(group_list.length - 1, rand_ind, n_split);
    let in_group = [];
    let out_group = [];
    let pos = 0;
    for (let i = 0; i < group_list.length; i++) {
        if (pos < split[0].length && split[0][pos] == i) {
            in_group.push(group_list[i]);
            pos++;
        } else {
            out_group.push(group_list[i]);
        }
    }

    other_groups = make_groups(out_group, split[1], n_groups - 1);
    other_groups[0].push(in_group);

    return other_groups;
}
