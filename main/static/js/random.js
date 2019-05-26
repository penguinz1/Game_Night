const length = deltas.length
const adj = 0.04683533

const heads_tails = (rand_ind) => {
    rand_ind %= length;
    return(deltas[rand_ind] > adj);
}

const make_random = (n_random, rand_ind) => {
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

        if (picks.length == 1) {
            return [picks[0], rand_ind];
        }

        if (picks.length == 0) {
            continue;
        }

        numbers = picks
    }
}
